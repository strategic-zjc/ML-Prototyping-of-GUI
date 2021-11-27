import os
from PIL import Image
import torch
import torchvision
from d2l import torch as d2l
from torch.utils import data
from torch.utils.data import Dataset
from torchvision import transforms


train_data_dir = r'C:\Users\86134\Desktop\autotest_tool\CNN-Evaluation\Partitioned-Organic-Data-Split\Training'
test_data_dir = r'C:\Users\86134\Desktop\autotest_tool\CNN-Evaluation\Partitioned-Organic-Data-Split\Test'
val_data_dir = r'C:\Users\86134\Desktop\autotest_tool\CNN-Evaluation\Partitioned-Organic-Data-Split\Validation'
synthetic_train_dir = r'C:\Users\86134\Desktop\autotest_tool\CNN-Evaluation\Synthetic+Organic-Color-Perturbed-Training-Data-Split'

GUI_TYPE_TO_LABEL_DICT={"TextView":0, "ImageView":1, "Button":2, "ImageButton":3, "EditText":4,
               "CheckedTextView":5, "CheckBox":6, "RadioButton":7, "ProgressBar":8, "SeekBar":9,
               "NumberPicker":10, "Switch":11, "ToggleButton":12, "RatingBar":13, "Spinner":14,
                "ProgressBarVertical":8, "ProgressBarHorizontal":8}
GUI_TYPE_LABEL_LIST = ["TextView", "ImageView", "Button", "ImageButton", "EditText",
               "CheckedTextView", "CheckBox", "RadioButton", "ProgressBar", "SeekBar",
               "NumberPicker", "Switch", "ToggleButton", "RatingBar", "Spinner"]

LABEL_TO_GUI_TYPE_DICT={0:"TextView", 1:"ImageView", 2:"Button", 3:"ImageButton", 4:"EditText",
               5:"CheckedTextView", 6:"CheckBox", 7:"RadioButton", 8:"ProgressBar", 9:"SeekBar",
               10:"NumberPicker", 11:"Switch", 12:"ToggleButton", 13:"RatingBar", 14:"Spinner",}

TRAIN_TXT_PATH = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\CNNClassifier\data\train.txt'
TEST_TXT_PATH = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\CNNClassifier\data\test.txt'
VAL_TXT_PATH = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\CNNClassifier\data\validate.txt'


TRAIN_TYPE_MIN = 1000
TRAIN_TYPE_MAX = 10000

TEST_TYPE_MAX = 2000

VAL_TYPE_MAX = 300



def create_train_txt():
    label_cnt = [0 for i in range(15)]
    path_list = []
    label_list = []
    for root, dirs, files in os.walk(train_data_dir):
        for file in files:
            if(file[0]!='.'):
                path = os.path.join(root, file)
                label = file.split('.')[-2]
                label = GUI_TYPE_TO_LABEL_DICT.get(label)

                if(label_cnt[label] < TRAIN_TYPE_MAX):
                    # no more than TYPE_MAX_SUM
                    label_cnt[label] += 1
                    path_list.append(path)
                    label_list.append(label)
    # augment type
    for root, dirs, files in os.walk(synthetic_train_dir):
        for file in files:
            if(file[0]!='.'):
                path = os.path.join(root, file)
                type = file.split('.')[-2]
                # 获取label
                label = GUI_TYPE_TO_LABEL_DICT.get(type)

                if(label_cnt[label] < TRAIN_TYPE_MIN):
                    path_list.append(path)
                    label_list.append(label)
                    label_cnt[label] += 1
    with open(TRAIN_TXT_PATH, 'w') as f:
        for i in range(len(path_list)):
            f.write(path_list[i] + " " + str(label_list[i])+"\n")
def create_test_txt():
    test_cnt = [0 for i in range(15)]
    path_list = []
    label_list = []
    for root, dirs, files in os.walk(test_data_dir):
        for file in files:
            if (file[0] != '.'):
                path = os.path.join(root, file)
                label = file.split('.')[-2]
                label = GUI_TYPE_TO_LABEL_DICT.get(label)
                if(test_cnt[label] < TEST_TYPE_MAX):
                    path_list.append(path)
                    label_list.append(label)
                    test_cnt[label] += 1
    with open(TEST_TXT_PATH, 'w') as f:
        for i in range(len(path_list)):
            f.write(path_list[i] + " " + str(label_list[i])+"\n")

def create_val_txt():
    val_cnt = [0 for i in range(15)]
    path_list = []
    label_list = []
    for root, dirs, files in os.walk(val_data_dir):
        for file in files:
            if (file[0] != '.'):
                path = os.path.join(root, file)
                label = file.split('.')[-2]
                label = GUI_TYPE_TO_LABEL_DICT.get(label)
                if (val_cnt[label] < VAL_TYPE_MAX):
                    path_list.append(path)
                    label_list.append(label)
                    val_cnt[label] += 1
    with open(VAL_TXT_PATH, 'w') as f:
        for i in range(len(path_list)):
            f.write(path_list[i] + " " + str(label_list[i]) + "\n")

class MyDataset(Dataset):
    def __init__(self, txt_path, transform = None, target_transform = None):
        fh = open(txt_path, 'r')
        imgs = []
        for line in fh:
            line = line.rstrip()
            words = line.split()
            # 保存列表 其中有图像的数据 和标签
            # img_ = Image.open(words[0]).convert('RGB')
            # if transform is not None:
            #     img_ = transform(img_)
            imgs.append((words[0], words[1]))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = Image.open(fn).convert('RGB')
        if self.transform is not None:
            img = self.transform(img)
        return img, int(label)
    def __len__(self):
        return len(self.imgs)

def trans_fig_func(resize = None):
    trans = [transforms.ToTensor()]
    if resize:
        trans.insert(0, transforms.Resize([resize, resize]))
    trans = transforms.Compose(trans)
    return trans

def show_type_num(path):
    label_cnt, total = get_type_num(path)
    for i in range(len(label_cnt)):
        print(f'GUI type {LABEL_TO_GUI_TYPE_DICT.get(i)}, {label_cnt[i]}')
    print(f'total: {total}')

def get_type_num(path):
    total = 0
    label_cnt = [0 for i in range(15)]
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            label = int(line.split(" ")[1])
            label_cnt[label] += 1
    for i in range(15):
        total += label_cnt[i]
    return label_cnt, total


    # create_train_txt()
    # show_type_num(TRAIN_TXT_PATH)
    # BATCH_SIZE = 128
    # NUM_WORKERS = 4
    # RESIZE = 224
    # mDataSet = MyDataset(TRAIN_TXT_PATH, transform=trans_fig_func(RESIZE))
    # train_iter = data.DataLoader(dataset=mDataSet, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
    # timer = d2l.Timer()
    # for X, y in train_iter:
    #     print(X.shape, X.dtype, y.shape , y.dtype)
    # print(f'{timer.stop():.2f} sec')