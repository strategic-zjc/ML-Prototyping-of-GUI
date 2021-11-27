from CNNClassifier.GNet import *
from CNNClassifier.DataLoader import *
from PIL import Image
import cv2

def predict(img):
    net = getNet()
    device = d2l.try_gpu()
    net.to(device)
    # opencv 2 PIL.image
    image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    transform = trans_fig_func(resize)
    image = transform(image)
    X = image.to(device)
    X = X.reshape((1,3,224,224))
    pred = net(X)

    y_hat = pred.argmax(axis = 1)
    y_hat = y_hat.cpu().numpy()
    return LABEL_TO_GUI_TYPE_DICT.get(y_hat[0])

