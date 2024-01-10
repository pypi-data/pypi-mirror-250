import argparse


parser = argparse.ArgumentParser(description='Train the Net on images and target masks')
parser.add_argument('--model_type',      type=list,  default=["MultiResUnet"])
parser.add_argument('--backbone',        type=list,  default=['resnet18'])
parser.add_argument('--aux_loss',        type=bool,  default=False)
parser.add_argument('--mode',            type=str,   default='train',
                    help='train, val, test')
# --------------------------------------------------------------------------------------------
parser.add_argument('--data_dir',        type=str,   default=f'data/regular/trainvaltest',
                    help='train image dir')
parser.add_argument('--class_list',      type=list,  default=['gts_nii_20220501', 'gts_nii_20220526'],
                    help='train image dir')
parser.add_argument('--img_size',        type=tuple, default=(512, 512),
                    help='input size to network')
# parser.add_argument('--data_txt',        type=str,   default=f'../data/regular/trainvaltest/gts_nii_20220501.nii.gz',
#                     help='txt file')
parser.add_argument('--eval_save_dir',   type=str,   default=f'results')
# -------------------------------------------------------------------------------------------
parser.add_argument('--epochs',          type=int,   default=50,
                    help='Number of epochs', dest='epochs')
parser.add_argument('--batch_size',      type=list,  default=[2],
                    help='Batch size')
parser.add_argument('--learning_rate',   type=float, default=0.01,
                    help='Learning rate')
parser.add_argument('--load',            type=str,   default='results/MultiResUnet/202208311342_batch1/1/MultiResUnet_128_128_epoch2.pth',
                    help='')
parser.add_argument('--loss',            type=str,   default=['BinaryDiceLoss'],
                    help='BinaryDiceLoss, BCEWithLogitsLoss, MSEWithLogitsLoss')
args = parser.parse_args()
