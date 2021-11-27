import os
import os.path

import torch
import numpy as np
from torch import nn
from d2l import torch as d2l
from CNNClassifier.DataLoader import MyDataset, trans_fig_func, TRAIN_TXT_PATH, TEST_TXT_PATH, VAL_TXT_PATH, get_type_num, \
        LABEL_TO_GUI_TYPE_DICT, show_type_num, GUI_TYPE_LABEL_LIST
from torch.utils import data
import matplotlib.pyplot as plt

GNET_PATH = r'C:\Users\86134\Desktop\autotest_tool\ML_GUI_Prototype\CNNClassifier\gnet.pth'




gnet = nn.Sequential(
    nn.Conv2d(3, 64, kernel_size=7, padding=3, stride=2),nn.ReLU(),
    nn.Conv2d(64, 64, kernel_size=7, padding=3, stride=2),nn.ReLU(),
    nn.MaxPool2d(kernel_size=3,stride=1),
    nn.Conv2d(64, 96, kernel_size=3, stride=2), nn.ReLU(), # in paper stride is not defined
    nn.MaxPool2d(kernel_size=2, stride=1),
    nn.Dropout(0.5),
    nn.Flatten(),
    nn.Linear(60000, 1024), nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(1024, 1024), nn.ReLU(),
    nn.Linear(1024, 15), nn.ReLU(),
)

def accuracy(y_hat, y):
    """计算预测正确的数量。"""
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp = y_hat.type(y.dtype) == y
    return float(cmp.type(y.dtype).sum())

def evaluate_accuracy_gpu(net, data_iter, device=None):
    """使用GPU计算模型在数据集上的精度。"""
    if isinstance(net, torch.nn.Module):
        net.eval()  # 设置为评估模式
        if not device:
            device = next(iter(net.parameters())).device
    # 正确预测的数量，总预测的数量
    metric = d2l.Accumulator(2)
    for X, y in data_iter:
        if isinstance(X, list):
            # BERT微调所需的（之后将介绍）
            X = [x.to(device) for x in X]
        else:
            X = X.to(device)
        y = y.to(device)
        metric.add(d2l.accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]


def train_net(net, train_iter, test_iter, num_epochs, lr, device, start_epoch = 0):
    print('training on', device)
    net.to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=lr, momentum=0.9)
    loss = nn.CrossEntropyLoss()
    timer, num_batches = d2l.Timer(), len(train_iter)
    for epoch in range(start_epoch, num_epochs + start_epoch):
        # 训练损失之和，训练准确率之和，范例数
        print(f'epoch {epoch + 1}',end="")
        metric = d2l.Accumulator(3)
        net.train()
        for i, (X, y) in enumerate(train_iter):
            timer.start()
            optimizer.zero_grad()
            X, y = X.to(device), y.to(device)
            y_hat = net(X)
            l = loss(y_hat, y)
            l.backward()
            optimizer.step()
            with torch.no_grad():
                metric.add(l * X.shape[0], d2l.accuracy(y_hat, y), X.shape[0])
            timer.stop()
            print('=', end="")
        print('>')
        train_l = metric[0] / metric[2]
        train_acc = metric[1] / metric[2]
        test_acc = evaluate_accuracy_gpu(net, test_iter,device)
        print(f'train loss {train_l:.3f}, train acc {train_acc:.3f}, test acc {test_acc:.3f}')
        if((epoch+1) % 2 == 0):
            torch.save({"net":net.state_dict(),
                    "epoch": epoch+1,
                    "learning rate":lr},  GNET_PATH)
            print(f'model saved in epoch: {epoch+1}')

    torch.save({"net": net.state_dict(),
                "epoch": start_epoch + num_epochs,
                "learning rate": lr}, GNET_PATH)
    print(f'model saved in epoch: {start_epoch + num_epochs}')
    print(f'final: train loss {train_l:.3f}, train acc {train_acc:.3f}, '
          f'test acc {test_acc:.3f}')
    print(f'{metric[2] * num_epochs / timer.sum():.1f} examples/sec '
          f'on {str(device)}')

def init_weights(m):
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.xavier_uniform_(m.weight)
def init_net():
    gnet.apply(init_weights)
    torch.save({"net": gnet.state_dict(),
                "epoch": 0,
                "learning rate": 0.01}, GNET_PATH)
    print("initial network done.")

resize = 224
batch_size = 64
num_workers = 4


def get_confusion_mat(net, txt_path):
    show_type_num(txt_path)
    type_cnt, total = get_type_num(txt_path)
    all_pred = torch.zeros([len(type_cnt)]*2, dtype=torch.int64)
    type_cnt = torch.tensor(type_cnt, dtype=torch.float64)
    test_dataset = MyDataset(txt_path, transform=trans_fig_func(resize))
    test_iter = data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    device = d2l.try_gpu()
    net.to(device)
    net.train()
    metric = d2l.Accumulator(2)
    for i, (X, y) in enumerate(test_iter):
        X, y= X.to(device), y.to(device)
        y_hat = net(X)
        if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
            y_hat = y_hat.argmax(axis=1)
        for j in range(len(y_hat)):
            all_pred[y.cpu().numpy()[j]][y_hat.cpu().numpy()[j]] += 1
        metric.add(d2l.accuracy(net(X), y), y.numel())

    type_cnt = type_cnt.reshape((-1, 1))
    conf_mat = all_pred / type_cnt
    for i in range(len(type_cnt)):
        type = LABEL_TO_GUI_TYPE_DICT.get(i)
        print(f'GUI type: {type}, test acc: {conf_mat[i][i]:.3f}')
    print(f'total acc: {metric[0]/metric[1]:.3f}')



    display = torch.cat((type_cnt, conf_mat), dim=1)
    display_np = display.numpy()
    display_np = np.around(display_np, 4)
    plt.figure(figsize=(32, 16))
    colLabel = ['total']
    colLabel.extend(GUI_TYPE_LABEL_LIST)
    rowLabel = GUI_TYPE_LABEL_LIST
    plt.table(cellText=display_np,  # 简单理解为表示表格里的数据
              colLabels=colLabel,  # 每列的名称
              rowLabels=rowLabel,  # 每行的名称（从列名称的下一行开始）
              loc='center',
              cellLoc='center',
              rowLoc='center'  # 行名称的对齐方式
              )
    plt.axis('off')
    plt.figure(dpi=160)
    plt.show()

    return conf_mat


def train(model_path, epoch, lr):
    net_info = torch.load(model_path)
    stat_dict = net_info['net']
    lst_epoch = net_info['epoch']
    lst_lr = net_info['learning rate']
    gnet.load_state_dict(stat_dict)
    gnet.eval()
    train_dataset = MyDataset(TRAIN_TXT_PATH, transform=trans_fig_func(resize))
    val_dataset = MyDataset(VAL_TXT_PATH, transform=trans_fig_func(resize))

    train_iter = data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_iter = data.DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    train_net(gnet, train_iter, val_iter, epoch, lr, d2l.try_gpu(), lst_epoch)
def getNet():
    net_info = torch.load(GNET_PATH)
    stat_dict = net_info['net']
    lst_epoch = net_info['epoch']
    lst_lr = net_info['learning rate']
    gnet.load_state_dict(stat_dict)
    gnet.eval()
    return gnet

def get_confusion_mat_test(txt_path):
    show_type_num(txt_path)
    type_cnt, total = get_type_num(txt_path)
    all_pred = torch.zeros([len(type_cnt)] * 2, dtype=torch.int64)
    type_cnt = torch.tensor(type_cnt, dtype=torch.float64)
    conf_mat = torch.zeros_like(all_pred, dtype = torch.float64)
    type_cnt = type_cnt.reshape((-1, 1))
    print(type_cnt)
    print(type_cnt.shape)

    display = torch.cat((type_cnt, conf_mat), dim = 1)
    display_np = display.numpy()
    display_np = np.around(display_np, 4)

    plt.figure(figsize=(20,8))
    colLabel = ['total']
    colLabel.extend(GUI_TYPE_LABEL_LIST)
    rowLabel = GUI_TYPE_LABEL_LIST
    plt.table(cellText=display_np,  # 简单理解为表示表格里的数据
              colLabels=colLabel,  # 每列的名称
              rowLabels=rowLabel,  # 每行的名称（从列名称的下一行开始）
              loc='center',
              cellLoc='center',
              rowLoc='center'  # 行名称的对齐方式
    )
    plt.axis('tight')
    plt.axis('off')
    plt.figure(dpi=80)
    plt.show()
    # print(display)









if __name__ =="__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = '0'
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    net = getNet()
    get_confusion_mat(net, TEST_TXT_PATH)
