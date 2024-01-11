import numpy as np
import torch
from torch.utils.data import Dataset
import logging
import os
import cv2
from sklearn.utils import shuffle
from pathlib import Path
# from torch.utils.data import DataLoader
import albumentations as A


class SegmentationDataset(Dataset):
    def __init__(self, data_root, choice='train', img_size=(512, 512), data_augment=False, class_list=None,
                 use_shuffle=False, CV=None):
        data_path = dict()
        txt = os.path.join(data_root, 'meta', f'{choice}.txt')
        root_dir = os.path.join(data_root, choice)
        data_path['img'] = self.read_img(txt, root_dir, fold='imgs')
        if use_shuffle:
            data_path['img'] = shuffle(data_path['img'], random_state=100)
        for cls in class_list:
            data_path[cls] = []
            for p in data_path['img']:
                temp = os.path.join(str(p.parent.parent), str(cls), p.stem + '.png')
                temp = Path(temp)
                if temp.exists():
                    data_path[cls].append(temp)
                else:
                    assert temp.parent.exists()
                    data_path[cls].append(None)
        if CV is not None:
            data_path = self.get_cross_valid_data_path(CV, data_path)

        self.data_path = data_path
        self.img_size = img_size
        self.data_augment = data_augment
        self.class_list = class_list
        logging.info(f"Creating {choice} {CV} dataset with {len(self.data_path['img'])} examples")

    def __len__(self):
        return len(self.data_path['img'])

    def __getitem__(self, i):
        img_path = self.data_path['img'][i]
        assert img_path.exists()
        img = cv2.imread(str(img_path), -1)
        H, W = img.shape[:2]

        gt = []
        for cls in self.class_list:
            gt_path = self.data_path[cls][i]
            if gt_path is None:
                temp = np.zeros((H, W), np.uint8)
            else:
                temp = cv2.imread(str(gt_path), -1)
            gt.append(temp)

        if self.data_augment:
            img, gt = self.img_transform(img, gt)
            # plt_imshow([img] + [g for g in gt])

        img, gt = self.img2input(img, gt, self.img_size)
        gt = np.array(gt, np.uint8)

        if img.ndim == 2:
            img = np.expand_dims(img, axis=2)
        if gt.ndim == 2:
            gt = np.expand_dims(gt, axis=2)

        img = torch.from_numpy(img)
        gt = torch.from_numpy(gt)
        # gt = torch.nn.functional.one_hot(gt)
        return img.permute(2, 0, 1), gt

    @staticmethod
    def get_cross_valid_data_path(CV, data_path):
        # interval
        ki, K, flag = CV
        itv = len(data_path['img']) // K
        if flag == 'train':
            for key in data_path.keys():
                data_path[key] = data_path[key][:itv * (ki - 1)] + data_path[key][itv * ki:]
        elif flag == 'val':
            for key in data_path.keys():
                data_path[key] = data_path[key][itv * (ki - 1):itv * ki]
        return data_path

    @staticmethod
    def img2input(img, gt, img_size):
        img = cv2.resize(img, img_size)
        img = img.astype(np.float32) / 255

        gt_list = []
        for temp in gt:
            temp = cv2.resize(temp, img_size, interpolation=cv2.INTER_NEAREST)
            temp[temp != 0] = 1
            gt_list.append(temp)
        return img, gt_list

    @staticmethod
    def read_img(txt, root, fold):
        with open(txt, mode='r') as f:
            lines = f.readlines()
        img_list = [os.path.join(root, fold, line.strip()) for line in lines if line.strip() != '']
        img_list = [Path(line) for line in img_list]
        return img_list

    @staticmethod
    def sort_key(x):
        return x.stem

    @staticmethod
    def img_transform(image, masks):
        transform = A.Compose([
            # A.RandomCrop(width=512, height=512),
            A.HorizontalFlip(p=0.5),
            # A.VerticalFlip(p=0.5),
            # A.RandomBrightnessContrast(p=0.5),
        ])
        transformed = transform(image=image, masks=masks)
        transformed_image = transformed['image']
        transformed_masks = transformed['masks']
        return transformed_image, transformed_masks

    @staticmethod
    def gen_txt(root_dir, paths=None, custom_key=None):
        if paths is None:
            paths = ['train', 'val', 'test']
        meta_dir = os.path.join(root_dir, 'meta')
        for choice in paths:
            path = Path(os.path.join(root_dir, choice, 'imgs'))
            if path.exists():
                filename_list = [filename for filename in path.glob("*")]
                if custom_key is not None:
                    filename_list = sorted(filename_list, reverse=False, key=custom_key)
                txt = os.path.join(meta_dir, f'{choice}.txt')
                file = open(txt, mode='w')
                for filename in filename_list:
                    file.write(f"{filename.name}\n")
                file.close()


if __name__ == "__main__":
    SegmentationDataset.gen_txt('data/hard_data')
    # train_dataset = SegmentationDataset(data_root='../data/regular/trainvaltest', choice='train', class_list=['gts_nii_20220501', 'gts_nii_20220526'], CV=None, use_shuffle=False)
    # data_loader = DataLoader(train_dataset, batch_size=1, shuffle=False, num_workers=1, pin_memory=True, drop_last=False)
    # for i, (imgs, gts) in enumerate(data_loader):
    #     print(i)
    #     aa = 0


    # img = cv2.imread("../data/regular/trainvaltest/train/imgs/2020102803_20201028_140220_Color_R_001.jpg", -1)
    # mask_1 = cv2.imread("../data/regular/trainvaltest/train/gts_nii_20220501/2020102803_20201028_140220_Color_R_001.png", -1)
    # mask_2 = cv2.imread("../data/regular/trainvaltest/train/gts_nii_20220501/2020102803_20201028_140220_Color_R_001.png", -1)
    #
    # transformed_image, transformed_masks = SegmentationDataset.img_transform(image=img, masks=[mask_1, mask_2])
    #
    # plt_imshow([img[:,:,::-1], mask_1, mask_2, transformed_image[:,:,::-1], transformed_masks[0], transformed_masks[1]])
