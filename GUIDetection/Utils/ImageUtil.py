
import numpy as np
from GUIDetection.RectUtils.Rect import Rect
import cv2
import GUIDetection.Utils.ColorUtil as ColorUtil
from GUIDetection.Utils.ColorUtil import *
import copy
import GUIDetection.RectUtils.RectUtil as RectUtil


def	 getImageFromRect(original, rect) :
    newImage = copy.deepcopy(original[int(rect.y):int(rect.y+rect.height),int(rect.x):int(rect.x+rect.width)])
    return newImage

def	getImageFromContour(original, contour) :
    rect = Rect(cv2.boundingRect(contour))
    return getImageFromRect(original, rect)

def fillRect(image, rect, dominantColor) :
    r = dominantColor & 255
    g = dominantColor >> 8 & 255
    b = dominantColor >> 16 & 255
    cv2.rectangle(image, rect.tl(), rect.br(), (r, g, b), -1)
	

def	 drawRect(image,  rect, color, thickness=2) :
    a = np.right_shift(color, 24)  & 255
    r = (color >> 16) & 255
    g = (color >> 8) & 255
    b = color & 255
    cv2.rectangle(image, rect.tl(), rect.br(), (b, g, r),thickness)
    return image
	

def drawWindow(_id, image):
    width = 0
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width,channels = image.shape
    cv2.namedWindow(_id, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(_id, int(width/3), int(height/3))
    cv2.imshow(_id,image)

def drawRectViewList(image, rectViews, color, thickness=2):
    for rectView in rectViews:
        drawRect(image, rectView.bound(), color, thickness)

def showGUIComponent(image, _id):
    width = 0
    height = 0

    if len(image.shape) == 2:
        height, width = image.shape
    else:
        height, width, channels = image.shape
    cv2.namedWindow(_id, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(_id, int(width*2), int(height*2))
    cv2.imshow(_id, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showImageId(img, id):
    drawWindow(id, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showImage(img):
    drawWindow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def drawBoundingRect(img, rectView, color = CColor.Red):
    img_c = copy.deepcopy(img)
    drawBoundingRectIntern(img_c, rectView, color)
    showImage(img_c)
    return img_c

def drawBoundingRectList(img, rectViews, color = CColor.Red):
    img_c = copy.deepcopy(img)
    drawRectViewList(img_c, rectViews, ColorUtil.cColortoInt(color))
    showImage(img_c)
    return img_c


def fillBoundingRect(img, rectView):
    img_c = copy.deepcopy(img)
    fillBoundingRectIntern(img_c, rectView)
    showImage(img_c)

def fillBoundingRectIntern(img, rectView):
    child = rectView.mChildren
    for view in child:
        fillRect(img, view.bound(), ColorUtil.cColortoInt(ColorUtil.randomColor()))
        fillBoundingRectIntern(img, view)

def drawBoundingRectIntern(img, rectView, color):
    child = rectView.mChildren

    for view in child:
        drawRect(img, view.bound(), ColorUtil.cColortoInt(color))
        drawBoundingRectIntern(img, view, color)