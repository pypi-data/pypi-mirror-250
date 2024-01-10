import numpy as np
import sklearn.metrics as skme
import copy


class MultiClassEval(object):
    dic = {'data': [], 'mean': -1, 'std': -1}

    def __init__(self, num_class, metrics):
        self.num_class = num_class
        self.metrics = metrics
        self.txt_res = None
        self.init_metrics_dict()

    def __add__(self, other):
        self.metrics += other.metrics
        # self.eval_res.update(other.eval_res)
        # new = MultiClassEval(self.num_class, self.metrics + other.metrics)
        for i in [x for x in range(self.num_class)]:
            self.eval_res[i].update(other.eval_res[i])
        # new.eval_res.update(self.eval_res)
        # new.eval_res.update(other.eval_res)
        return self

    def init_metrics_dict(self):
        eval_res = dict()
        # eval_res = {'avg': dict()}
        # for m in self.metrics:
        #     eval_res['avg'][m] = copy.deepcopy(MultiClassEval.dic)

        for c in range(self.num_class):
            eval_res[c] = dict()
            for m in self.metrics:
                eval_res[c][m] = copy.deepcopy(MultiClassEval.dic)
        self.eval_res = eval_res
        # return eval_res

    def cal_metrics(self, which_class, gt_array_list, mask_array_list, prob_array_list=None, target_array_list=None):
        one_class = Evaluation(self.metrics, gt_array_list, mask_array_list, prob_array_list, target_array_list)
        self.eval_res[which_class] = one_class.eval_res

    def cal_avg(self):
        self.eval_res['avg'] = dict()
        for m in self.metrics:
            self.eval_res['avg'][m] = copy.deepcopy(MultiClassEval.dic)

        for c in range(self.num_class):
            for m in self.metrics:
                assert type(self.eval_res[c][m]['data']) is list
                self.eval_res['avg'][m]['data'] += self.eval_res[c][m]['data']

        # 计算average中评价标准的mean和std
        for m in self.metrics:
            temp_data = np.array(self.eval_res['avg'][m]['data'])
            self.eval_res['avg'][m]['mean'] = (100 * np.nanmean(temp_data)).round(2)
            self.eval_res['avg'][m]['std'] = (100 * np.nanstd(temp_data)).round(2)

    def print_res(self, epoch=-1):
        """
        :param accLine: accLine为dict.items()格式，即[(key, value), (key, value)]格式
        :param num_class:
        :return:
        """
        accList = []
        if 'avg' in self.eval_res:
            acc_index = [x for x in range(self.num_class)] + ['avg']
        else:
            acc_index = [x for x in range(self.num_class)]
        accLine = [(f"epoch{epoch}", self.eval_res)]
        for line in accLine:
            # 键，epoch10
            epochxx = line[0]
            acc_dict = line[1]
            one_epoch = [epochxx]
            for i, acc in enumerate(acc_index):
                metricDict = acc_dict[acc]
                oneLine = f'class {acc}'
                for metricName, metricList in metricDict.items():
                    mean = metricList["mean"]
                    std = metricList["std"]
                    meanstd = [f"{mean}({std})"]
                    oneMetric = f" {metricName} {meanstd}"
                    oneLine = oneLine + oneMetric
                # oneLine = f"{epochxx}: {oneLine}" if i == 0 else f"         {oneLine}"
                # oneLine = f"{oneLine}"
                oneLine = oneLine.replace('\'', '')
                # oneLine = oneLine[:-1]
                # oneLine = oneLine.replace(',', '')
                # 每个类别的精确率，输出为一行
                one_epoch.append(oneLine)
            # 每个epoch最后加上空行
            one_epoch[-1] += '\n'
            accList.append(one_epoch)

        self.txt_res = accList[0]
        for line in self.txt_res:
            print(line)


class Evaluation(object):
    def __init__(self, metrics, gt_array_list, mask_array_list, prob_array_list=None, target_array_list=None):
        self.metrics = metrics

        self.gt_array_list = gt_array_list
        self.mask_array_list = mask_array_list
        self.prob_array_list = prob_array_list
        self.target_array_list = target_array_list

        self.eval_res = self.init_metrics_dict()
        self.cal_metrics()

    def init_metrics_dict(self):
        dic = {'data': [], 'mean': -1, 'std': -1}
        eval_res = {}
        for m in self.metrics:
            eval_res[m] = copy.deepcopy(dic)
        return eval_res

    def cal_metrics(self):
        for gt, mask in zip(self.gt_array_list, self.mask_array_list):
            acc = sklearnMetrics(gt=gt, pred=mask)
            if "DSC" in self.metrics:
                self.eval_res["DSC"]['data'].append(acc.compute_dice_mask(classid=1))
            if "IoU" in self.metrics:
                self.eval_res["IoU"]['data'].append(acc.compute_iou(classid=1))
            if "f1" in self.metrics:
                self.eval_res["f1"]['data'].append(acc.compute_f1())
            if "J" in self.metrics:
                self.eval_res["J"]['data'].append(acc.compute_jaccard())
            if "Sen" in self.metrics:
                self.eval_res["Sen"]['data'].append(acc.compute_recall_sen())
            if "Pre" in self.metrics:
                self.eval_res["Pre"]['data'].append(acc.compute_precision())
            if "Spe" in self.metrics:
                self.eval_res["Spe"]['data'].append(acc.compute_specificity())
            if "acc" in self.metrics:
                self.eval_res["acc"]['data'].append(acc.compute_acc())

        if "sDSC" in self.metrics:
            assert self.prob_array_list is not None
            for gt, scores in zip(self.gt_array_list, self.prob_array_list):
                acc = sklearnMetrics(gt=gt, score=scores)
                self.eval_res["sDSC"]['data'].append(acc.compute_dice_prob())

        if "mse" in self.metrics:
            assert self.target_array_list is not None
            assert self.prob_array_list is not None
            for target, scores in zip(self.target_array_list, self.prob_array_list):
                acc = sklearnMetrics(score=scores, targets=target)
                self.eval_res["mse"]['data'].append(acc.compute_mse())

        for m in self.metrics:
            self.eval_res[m]['mean'] = (100 * np.nanmean(self.eval_res[m]['data'])).round(2)
            self.eval_res[m]['std'] = (100 * np.nanstd(self.eval_res[m]['data'])).round(2)


class sklearnMetrics(object):
    def __init__(self, gt=None, pred=None, targets=None, labels=[1], score=None):
        self.gt_noflatten = gt.copy() if gt is not None else None
        self.pred_noflatten = pred.copy() if pred is not None else None
        self.targets = targets.flatten() if targets is not None else None
        self.score = score.flatten() if score is not None else None
        self.gt = gt.flatten() if gt is not None else None
        self.pred = pred.flatten() if pred is not None else None

        self.labels = labels
        self.matrix = skme.confusion_matrix(y_true=self.gt,
                                            y_pred=self.pred) if self.gt is not None and self.pred is not None else None

    def compute_mse(self):
        # mse = self.targets - self.score
        # mse = np.sum(mse)
        mse = skme.mean_squared_error(self.targets, self.score)
        return mse * 100

    def compute_jaccard(self):
        """
        对于分割问题，是分类正确像素点占总像素比例，包括背景像素！！
        :return:
        """
        if (np.sum(self.gt) + np.sum(self.pred)) == 0:
            return 1.0
        else:
            jac = skme.jaccard_score(self.gt, self.pred, labels=self.labels)
            return jac

    def compute_specificity(self):
        if np.sum(self.pred) == 0:
            return 1.0
        else:
            TN = self.matrix[0, 0]
            FP = self.matrix[0, 1]
            spe = TN / float(TN + FP)
            return spe

    def compute_f1(self):
        """
        f1_score = (2 * Recall * Presision) / (Recall + Presision)
        :param prediction: 2d array, int,
                estimated targets as returned by a classifier
        :param target: 2d array, int,
                ground truth
        :return:
            f1: float
        """
        # self.pred.tolist(), self.gt.tolist()
        # img = np.array(self.pred).flatten()
        # target = np.array(self.gt).flatten()
        if (np.sum(self.gt) + np.sum(self.pred)) == 0:
            return np.nan
        else:
            f1 = skme.f1_score(self.gt, self.pred, labels=self.labels)
            return f1

    def compute_dice_prob(self, smooth=1e-5):
        """
        根据分割概率图he标签计算Dice系数
        :param smooth:
        :return:
        """
        if (np.sum(self.gt) + np.sum(self.score)) == 0:
            return 1.0
        else:
            intersection = self.gt * self.score
            # dice_eff = (2. * intersection.sum() + smooth) / (self.gt.sum() + self.score.sum() + smooth)
            dice_eff = (2. * intersection.sum()) / (self.gt.sum() + self.score.sum())
            return dice_eff

    def compute_recall_sen(self):
        """
        查全率，recall = TP / (TP + FN), 与 sensitivity相同
        """
        if np.sum(self.gt) == 0:
            if np.sum(self.pred) == 0:
                return 1.0
            else:
                return 0.0
        else:
            recall = skme.recall_score(self.gt, self.pred, labels=self.labels)
            # recall = np.diag(self.matrix) / self.matrix.sum(axis=0)
            return recall

    def compute_precision(self):
        """
        查准率，精确率，precision = TP / (TP + FP)
        :return:
        """
        if np.sum(self.pred) == 0:
            if np.sum(self.gt) == 0:
                return 1.0
            else:
                return 0.0
        else:
            pre = skme.precision_score(self.gt, self.pred, labels=self.labels)
            return pre

    def compute_acc(self):
        """
        准确率, Accuracy = (TP + TN) / (TP + TN + FP + FN)
        :return:
        """
        acc = skme.accuracy_score(self.gt, self.pred)
        # acc = np.diag(matrix).sum() / matrix.sum()
        return acc

    def auc_score(self):
        auc = skme.roc_auc_score(self.gt, self.score)
        # fpr, tpr, thresholds = skme.roc_curve(self.gt, self.score)
        # plt.plot([0, 1], [0, 1], 'k-')
        # plt.plot(fpr, tpr)
        # plt.xlabel('Sen')
        # plt.ylabel('1-Spe')
        # plt.title('ROC Curve')
        # plt.show()
        return auc

    def compute_dice_mask(self, classid):
        """
        根据分割概率图he标签计算Dice系数
        :param smooth:
        :return:
        """
        if (np.sum(self.gt) + np.sum(self.pred)) == 0:
            return 1.0
        else:
            intersection = np.logical_and(self.gt == classid, self.pred == classid)
            dice_eff = (2. * intersection.sum()) / (self.gt.sum() + self.pred.sum())
            return dice_eff

    def compute_iou(self, classid):
        """  计算IoU
        :param input:  2d array, int, prediction
        :param target: 2d array, int, ground truth
        :param classes: int, the number of class
        :return:
            iou: float, the value of iou
        """
        if (np.sum(self.gt) + np.sum(self.pred)) == 0:
            return 1.0
        else:
            intersection = np.logical_and(self.gt == classid, self.pred == classid)
            # print(intersection.any())
            union = np.logical_or(self.gt == classid, self.pred == classid)
            iou = np.sum(intersection) / np.sum(union)
            return iou


if __name__ == "__main__":
    y_true = [1, 2, 3]
    y_pred = [1, 1, 2]
    b = 0
    # me = sklearnMetrics(y_true, y_pred, 2)
    # print(skme.classification_report(y_true, y_pred, labels=[1, 2]))