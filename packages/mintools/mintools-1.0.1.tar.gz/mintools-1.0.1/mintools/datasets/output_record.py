import cv2
import logging
import numpy as np


class ModelOutputRecord(object):
    def __init__(self, num_class):
        self.num_class = num_class
        self.init_dict()
        # self.infer_dict = self.init_dict()

    def init_dict(self):
        self.infer_dict = {
            "imgs": [],
            "imgs_name": []
        }
        for c in range(self.num_class):
            self.infer_dict[c] = {
                "probs": [],
                "labels": [],
                "masks": []
            }
        # return out_dict

    def add_img(self, value):
        N = value.shape[0]
        for n in range(N):
            temp = value[n, :, :, :].transpose(1, 2, 0)
            temp = np.squeeze(temp)
            if temp.ndim == 2:
                temp = cv2.cvtColor(temp, cv2.COLOR_GRAY2BGR)
            self.infer_dict['imgs'].append(temp)

    def add_img_name(self, value):
        self.infer_dict['imgs_name'].append(value)

    def add_prob(self, value):
        N, C = value.shape[0], value.shape[1]
        for n in range(N):
            for c in range(C):
                temp = value[n, c, :, :]
                self.infer_dict[c]['probs'].append(temp)

    def add_label(self, value, merge=False, use_argmax=False):
        self.merge = merge
        N, C = value.shape[0], value.shape[1]
        if self.merge:
            if use_argmax:
                for n in range(N):
                    temp = value[n, :, :, :]
                    temp = np.argmax(temp, axis=0)
                    temp = temp.astype(np.uint8) + 1
                    self.infer_dict[0]['labels'].append(temp)
            else:
                H, W = value.shape[2], value.shape[3]
                for n in range(N):
                    label = np.zeros((H, W), np.uint8)
                    for c in range(C):
                        temp = value[n, c, :, :]
                        temp = temp.astype(np.uint8)
                        label[temp == 1] = (c + 1)
                    self.infer_dict[0]['labels'].append(label)
        else:
            if use_argmax:
                for n in range(N):
                    temp = value[n, :, :, :]
                    temp = np.argmax(temp, axis=0)
                    temp = temp.astype(np.uint8) + 1
                    for c in range(C):
                        save_label = np.zeros_like(temp, np.uint8)
                        save_label[temp == (c + 1)] = 1
                        self.infer_dict[c]['masks'].append(save_label)
            else:
                for n in range(N):
                    for c in range(C):
                        temp = value[n, c, :, :]
                        temp = temp.astype(np.uint8)
                        self.infer_dict[c]['labels'].append(temp)

    def add_mask(self, preds, threshold=0.5, merge=False, use_argmax=False):
        self.merge = merge
        N, C = preds.shape[0], preds.shape[1]
        if self.merge:
            if use_argmax:
                for n in range(N):
                    temp = preds[n, :, :, :]
                    temp = np.argmax(temp, axis=0)
                    temp = temp.astype(np.uint8) + 1
                    self.infer_dict[0]['masks'].append(temp)
            else:
                H, W = preds.shape[2], preds.shape[3]
                for n in range(N):
                    mask = np.zeros((H, W), np.uint8)
                    for c in range(C):
                        temp = preds[n, c, :, :]
                        temp = np.array(temp > threshold, dtype=np.uint8)
                        mask[temp == 1] = (c + 1)
                    self.infer_dict[0]['masks'].append(mask)
        else:
            if use_argmax:
                for n in range(N):
                    temp = preds[n, :, :, :]
                    temp = np.argmax(temp, axis=0)
                    temp = temp.astype(np.uint8) + 1
                    for c in range(C):
                        save_mask = np.zeros_like(temp, np.uint8)
                        save_mask[temp == (c + 1)] = 1
                        self.infer_dict[c]['masks'].append(save_mask)
            else:
                for n in range(N):
                    for c in range(C):
                        temp = preds[n, c, :, :]
                        temp = np.array(temp > threshold, dtype=np.uint8)
                        self.infer_dict[c]['masks'].append(temp)

    @staticmethod
    def mask_coloring(src, color):
        max_value = np.max(src)
        src_color = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
        for i in range(1, 1 + max_value):
            src_color[np.where(src == i)] = color[i-1]
        return src_color

    def visualize(self, colors):
        self.infer_dict['vis'] = []
        imgs_list = self.infer_dict['imgs']
        for i in range(len(imgs_list)):
            img = imgs_list[i]
            # gt_list = []
            # mask_list = []
            temp = np.ones((img.shape[0], 6, 3), np.uint8) * 255
            C = 1 if self.merge else self.num_class
            save_img = img.copy()
            for c in range(C):
                gt = self.infer_dict[c]["labels"][i]
                gt = ModelOutputRecord.mask_coloring(gt, colors[c:])
                save_img = np.hstack([save_img, temp, gt])
                # gt_list.append(gt)

                mask = self.infer_dict[c]["masks"][i]
                mask = ModelOutputRecord.mask_coloring(mask, colors[c:])
                save_img = np.hstack([save_img, temp, mask])
                # mask_list.append(mask)
            self.infer_dict['vis'].append(save_img)

    def metrics_from_external(self, metrics_dict):
        metrics = metrics_dict.eval_res[0].keys()
        H, W = self.infer_dict['vis'][0].shape[:2]
        for i, vis_img in enumerate(self.infer_dict['vis']):
            txt_img = np.ones((H, H, 3), np.uint8) * 255
            for c in range(self.num_class):
                acc_dict = metrics_dict.eval_res[c]
                # txt = f"{c} "
                for nn, m in enumerate(metrics):
                    data = np.around(100*acc_dict[m]['data'][i], 2)
                    txt = f" {m}: {data}"
                    # txt += '\n'
                    txt_img = cv2.putText(txt_img, txt, (10, 30+30*nn), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                # vis_img = cv2.putText(vis_img, txt, (528, ), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)
            vis_img = np.hstack((vis_img, txt_img))
            self.infer_dict['vis'][i] = vis_img
            # cv2.imshow("vis_img", vis_img)
            # cv2.waitKey(0)

    def save_img(self, colors):
        self.visualize(colors)
        for i, img in enumerate(self.infer_dict['vis']):
            img_name = self.infer_dict['imgs_name'][i]
            if i == 0:
                save_path = img_name.parent
                save_path.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(img_name), img)
        logging.info("Successfully saving imgs")