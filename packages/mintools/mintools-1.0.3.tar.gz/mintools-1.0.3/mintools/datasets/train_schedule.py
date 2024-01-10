import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import logging
import time
import copy
import glob
import shutil
import numpy as np
from pathlib import Path
from tqdm import tqdm
from collections import OrderedDict
import torch
from torch.utils.data import DataLoader

from .segmentation import SegmentationDataset
from .metrics import MultiClassEval
from .output_record import ModelOutputRecord
# from models import getModel
# from utils.loss import getLoss


class ModelTraining(object):
    def __init__(self, net, net_name, num_class, batch_size, eval_save_dir, use_argmax=False):
        self.net = net
        self.net_name = net_name
        self.eval_save_dir = eval_save_dir
        self.num_class = num_class
        self.batch_size = batch_size
        self.use_argmax = use_argmax
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logging.info(f'Using device {self.device}')
        self.net.to(device=self.device)

    def load_weight(self, pretrain_weight):
        self.net.load_state_dict(
            torch.load(pretrain_weight, map_location=self.device)
        )
        logging.info(f'initialing weight from {pretrain_weight}')

    def set_output_param(self, label_vis_merge=False, cal_avg=False, ranking_class=0, ranking_metric='DSC'):
        self.label_vis_merge = label_vis_merge
        self.cal_avg = cal_avg
        self.ranking_class = ranking_class
        self.ranking_metric = ranking_metric

    def set_optimizer(self, init_lr=0.01):
        self.init_lr = init_lr
        # optimizer
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=self.init_lr)
        # learning strategy
        self.lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(self.optimizer, milestones=[20, 40], gamma=0.1)

    def set_loss(self, loss_type):
        self.loss_type = loss_type
        self.criterion = getLoss(self.loss_type)

    def set_dataset(self, data_root, img_szie, data_aug, class_list, CV=None, use_test_data=False):
        # whole_set = SegmentationDataset(img_dir=img_dir, gt_dir=gt_dir, choice='train',
        #                               img_size=self.img_size, data_augment=False)
        # length = len(whole_set)
        # train_size, val_size, test_size = int(0.6 * length), int(0.2 * length), int(0.2 * length)
        # self.train_dataset, self.val_dataset, self.test_dataset = random_split(whole_set, [train_size, val_size, test_size])
        self.CV = CV
        self.img_size = img_szie
        self.class_list = class_list
        self.use_test_data = use_test_data
        if CV is not None:
            self.train_dataset = SegmentationDataset(data_root=data_root, choice='train',
                                          img_size=self.img_size, data_augment=data_aug, class_list=self.class_list,
                                          CV=(CV[0], CV[1], 'train'))
            self.val_dataset = SegmentationDataset(data_root=data_root, choice='train',
                                        img_size=self.img_size, data_augment=False, class_list=self.class_list,
                                        CV=(CV[0], CV[1], 'val'))
        else:
            self.train_dataset = SegmentationDataset(data_root=data_root, choice='train',
                                          img_size=self.img_size, data_augment=data_aug, class_list=self.class_list)
            self.val_dataset = SegmentationDataset(data_root=data_root, choice='val',
                                        img_size=self.img_size, data_augment=False, class_list=self.class_list)
            if use_test_data:
                self.test_dataset = SegmentationDataset(data_root=data_root, choice='test',
                                             img_size=self.img_size, data_augment=False, class_list=self.class_list)

    def set_output_path(self, time_dir):
        if self.use_test_data:
            self.root_dir = os.path.join(self.eval_save_dir, f"{self.net_name}", f"{time_dir}_batch{self.batch_size}")
        else:
            if self.CV is None:
                self.root_dir = os.path.join(self.eval_save_dir, f"{self.net_name}", f"{time_dir}_batch{self.batch_size}")
            else:
                self.root_dir = os.path.join(self.eval_save_dir, f"{self.net_name}", f"{time_dir}_batch{self.batch_size}", f"{self.CV[0]}")

        self.val_txt = os.path.join(self.root_dir, f"trainval_{self.net_name}_{self.loss_type[0]}_{self.img_size[0]}_{self.img_size[1]}.txt")
        self.test_txt = os.path.join(self.root_dir, f"traintest_{self.net_name}_{self.loss_type[0]}_{self.img_size[0]}_{self.img_size[1]}.txt")

        self.best_val_res = os.path.join(self.eval_save_dir, 'val.txt')
        self.best_test_res = os.path.join(self.eval_save_dir, 'test.txt')

    def print_info(self):
        logging.info(f'''Starting training:
            Net:                    {self.net_name}
            img_size:               {self.img_size}
            class list:             {self.class_list}
            num class:              {self.num_class}
            Epochs:                 {self.epochs}
            loss:                   {self.loss_type}
            Batch size:             {self.batch_size}
            init learning rate:     {self.init_lr}
            Device:                 {self.device.type}
            Cross Validation Phase: {self.CV}
            root dir:               {self.root_dir}
            label_vis_merge:        {self.label_vis_merge}
            use_argmax:             {self.use_argmax}
        ''')

    def train(self, epochs):
        self.epochs = epochs
        self.print_info()
        # faster convolutions, but more memory
        # cudnn.benchmark = True
        train_loader = DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True,
                                  num_workers=1, pin_memory=True, drop_last=True)
        acc_val_list = []
        acc_test_list = []
        for epoch in range(1, epochs + 1):
            self.net.train()
            with tqdm(total=len(self.train_dataset), desc=f'Epoch {epoch}/{epochs}', unit='img') as pbar:
                for imgs, gts in train_loader:
                    imgs = imgs.to(device=self.device, dtype=torch.float32)
                    gts = gts.to(device=self.device, dtype=torch.float32)
                    preds = self.net(imgs)
                    if type(preds) == OrderedDict:
                        preds = preds['out']

                    if type(preds) is tuple:
                        loss = 0.0
                        for pp in preds:
                            temp = self.criterion(pp, gts)
                            loss = loss + temp
                    else:
                        loss = self.criterion(preds, gts)
                    pbar.set_postfix(**{'loss (batch)': loss.item()})
                    self.optimizer.zero_grad()
                    loss.backward()
                    # nn.utils.clip_grad_value_(net.parameters(), 0.1)
                    self.optimizer.step()
                    pbar.update(imgs.shape[0])

            acc_val_list.append(
                (epoch, self.valid(self.val_dataset, gen_img=False, epoch=epoch, choice='trainval'))
            )
            if self.use_test_data:
                acc_test_list.append(
                    (epoch, self.valid(self.test_dataset, gen_img=False, epoch=epoch, choice='traintest'))
                )

            self.lr_scheduler.step()
            current_lr = self.optimizer.state_dict()['param_groups'][0]['lr']
            print('Current lr', current_lr)

            if not os.path.exists(self.root_dir):
                os.makedirs(self.root_dir)
                logging.info(f'Created {self.root_dir}')

            self.ck_name = os.path.join(self.root_dir,
                                        f'{self.net_name}_{self.img_size[0]}_{self.img_size[1]}_epoch{epoch}.pth')

            torch.save(self.net.state_dict(), self.ck_name)
            logging.info(f'Checkpoint {epoch} saved !')

        best_epoch_val_list = self.printRes(acc_val_list, self.val_txt)
        if self.use_test_data:
            _ = self.printRes(acc_test_list, self.test_txt)

        cks = self.remove_cks(best_epoch_val_list, epochs)
        self.vis_best_res_and_get_best_xlsx(cks, best_epoch_val_list[0])

    def printRes(self, accDict, txt_name, keep_cks_max=2):
        accDict = sorted(accDict, reverse=True,
                         key=lambda x: x[1].eval_res[self.ranking_class][self.ranking_metric]["mean"])
        with open(txt_name, "a") as file:
            for one_epoch in accDict:
                for line in one_epoch[1].txt_res:
                    file.write(line + '\n')
        best_epoch_list = [accDict[i][0] for i in range(keep_cks_max)]
        return best_epoch_list

    def vis_best_res_and_get_best_xlsx(self, checkpoint, best_id):
        for ck in checkpoint:
            if f'_epoch{best_id}.pth' in ck:
                self.net.load_state_dict(torch.load(ck, map_location=self.device))
                self.val_res = self.valid(self.val_dataset, gen_img=True, epoch=best_id, choice='trainval')
                with open(self.best_val_res, "a") as file:
                    file.write(self.val_txt + '\n')
                    for line in self.val_res.txt_res:
                        file.write(line + '\n')
                if self.use_test_data:
                    self.test_res = self.valid(self.test_dataset, gen_img=True, epoch=best_id, choice='traintest')
                    with open(self.best_test_res, "a") as file:
                        file.write(self.test_txt + '\n')
                        for line in self.test_res.txt_res:
                            file.write(line + '\n')
                continue

    def remove_cks(self, best_epoch_list, all_epoch):
        cks_path = glob.escape(self.root_dir)
        cks = os.path.join(cks_path, '*.pth')
        cks = glob.glob(cks)

        all_epoch_list = [x for x in range(1, all_epoch + 1)]
        remove_list = [x for x in all_epoch_list if x not in best_epoch_list]
        for ck in cks:
            for x in remove_list:
                if f'_{x}.pth' in ck:
                    os.remove(ck)
                    continue
        return cks

    def valid(self, dataset, gen_img=False, epoch=-1, choice=None):
        self.net.eval()  # for Batch Normalization and Dropout
        data_loader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=1, pin_memory=True, drop_last=False)
        res_dict = ModelOutputRecord(self.num_class)
        res_metric = ModelOutputRecord(self.num_class)
        with tqdm(total=len(dataset), unit='img') as pbar:
            for i, (imgs, gts) in enumerate(data_loader):
                imgs = imgs.to(device=self.device, dtype=torch.float32)
                gts = gts.to(device=self.device, dtype=torch.float32)

                preds = self.net(imgs)
                if type(preds) == tuple:
                    preds = preds[0]
                elif type(preds) == OrderedDict:
                    preds = preds['out']

                preds = torch.sigmoid(preds)
                preds = preds.detach().cpu().numpy()
                res_dict.add_prob(preds)
                res_metric.add_prob(preds)

                gts = gts.detach().cpu().numpy().astype(np.uint8)
                res_dict.add_label(gts, merge=self.label_vis_merge, use_argmax=self.use_argmax)
                res_metric.add_label(gts, merge=False, use_argmax=self.use_argmax)

                imgs = imgs.cpu().numpy()
                imgs = np.array(imgs * 255, dtype=np.uint8)
                res_dict.add_img(imgs)
                save_dir = os.path.join(self.root_dir, f"{choice}_{self.net_name}_{self.img_size[0]}_{self.img_size[1]}_epoch{epoch}")
                img_name = dataset.data_path['img'][i].stem + '.png'
                save_dir = Path(os.path.join(save_dir, img_name))
                res_dict.add_img_name(save_dir)

                res_dict.add_mask(preds, merge=self.label_vis_merge, use_argmax=self.use_argmax)
                res_metric.add_mask(preds, merge=False, use_argmax=self.use_argmax)

                pbar.update(imgs.shape[0])

        valMetric = MultiClassEval(res_metric.num_class, ['DSC', 'IoU', 'Sen', 'Pre', 'Spe', 'sDSC', 'acc'])
        for i in range(res_metric.num_class):
            valMetric.cal_metrics(i, res_metric.infer_dict[i]["labels"], res_metric.infer_dict[i]["masks"],
                                  prob_array_list=res_metric.infer_dict[i]["probs"])
        if self.cal_avg:
            valMetric.cal_avg()
        print(f"{choice}:")
        valMetric.print_res(epoch)
        if gen_img:
            colors = [[0, 0, 255], [0, 255, 0], [255, 0, 0], [0, 97, 255], [255, 255, 0]]
            # res_dict.metrics_from_external(valMetric)
            res_dict.save_img(colors)
        return valMetric

    def evaluate(self, weights, choice):
        self.load_weight(weights)
        # faster convolutions, but more memory
        # cudnn.benchmark = True
        weights = Path(weights)
        self.root_dir = weights.parent
        # self.root_dir = os.path.split(weights)[0]
        epoch_eval = weights.stem.split('_')[-1][5:]
        # epoch_eval = int(weights.split('.pth')[0][-2:])
        if choice == 'val':
            _ = self.valid(self.val_dataset, gen_img=True, epoch=int(epoch_eval), choice=choice)
        elif choice == 'test':
            _ = self.valid(self.test_dataset, gen_img=True, epoch=int(epoch_eval), choice=choice)


def getmetricfromCrossValid(acc_list, best_val_res):
    """
    Current only support single class
    :param acc_list:
    :param best_val_res:
    :return:
    """
    acc_CV = copy.deepcopy(acc_list[0])
    for acc in acc_list[1:]:
        for m in acc.metrics:
            acc_CV.eval_res[0][m]['data'] += acc.eval_res[0][m]['data']
    for m in acc_CV.metrics:
        acc_CV.eval_res[0][m]['mean'] = (100 * np.nanmean(acc_CV.eval_res[0][m]['data'])).round(2)
        acc_CV.eval_res[0][m]['std'] = (100 * np.nanstd(acc_CV.eval_res[0][m]['data'])).round(2)
    acc_CV.print_res(epoch="Cross Valid")
    with open(best_val_res, "a") as file:
        for line in acc_CV.txt_res:
            file.write(line + '\n')


def run():
    logging.basicConfig(level=logging.INFO, format='%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    args = config.args
    time_dir = time.strftime("%Y%m%d%H%M", time.localtime())
    for net_name in args.model_type:
        for batch in args.batch_size:
            for backbone in args.backbone:
                net = getModel(net_name, img_channel=3, n_classes=len(args.class_list), backbone=backbone,
                               aux_loss=args.aux_loss)
                # out_net_name = f"{net_name}_{backbone}_auxloss_{args.aux_loss}"
                # out_net_name = net_name
                cross_validation_res = []
                for ki in [1]:
                    model = ModelTraining(net=net, net_name=net_name, num_class=len(args.class_list),
                                     batch_size=batch, eval_save_dir=args.eval_save_dir, use_argmax=False)

                    model.set_dataset(data_root=args.data_dir, img_szie=args.img_size, data_aug=False,
                                      class_list=args.class_list, CV=(ki, 2), use_test_data=False)
                    model.set_output_param(label_vis_merge=False, cal_avg=False, ranking_class=0, ranking_metric='DSC')
                    # if args.mode in ['val', 'test']:
                    #     model.evaluate(args.load, args.mode)
                    # else:
                    model.set_loss(loss_type=args.loss)

                    model.set_optimizer(init_lr=args.learning_rate)
                    model.set_output_path(time_dir=time_dir)
                    model.train(epochs=args.epochs)
                    cross_validation_res.append(model.val_res)
                getmetricfromCrossValid(cross_validation_res, best_val_res=os.path.join(args.eval_save_dir, 'val.txt'))
                shutil.copyfile('config.py', 'utils/cofig.py')


if __name__ == '__main__':
    run()
