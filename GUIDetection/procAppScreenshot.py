from GUIDetection.ViewProcess.Canny import Canny
from GUIDetection.ViewProcess.ContourAnalysis import *
from GUIDetection.ViewProcess.HierarchyInfo import *
import os
import cv2
import copy
from GUIDetection.Utils import ImageUtil
from GUIDetection.Utils import ColorUtil



def showImageId(img, id):
    ImageUtil.drawWindow(id, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showImage(img):
    ImageUtil.drawWindow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def drawBoundingRect(img, rectView, color = CColor.Red):
    img_c = copy.deepcopy(img)
    drawBoundingRectIntern(img_c, rectView, color)
    showImage(img_c)
    return img_c

def drawBoundingRectList(img, rectViews, color = CColor.Red):
    img_c = copy.deepcopy(img)
    ImageUtil.drawRectViewList(img_c, rectViews, ColorUtil.cColortoInt(color))
    showImage(img_c)
    return img_c


def fillBoundingRect(img, rectView):
    img_c = copy.deepcopy(img)
    fillBoundingRectIntern(img_c, rectView)
    showImage(img_c)

def fillBoundingRectIntern(img, rectView):
    child = rectView.mChildren
    for view in child:
        ImageUtil.fillRect(img, view.bound(), ColorUtil.cColortoInt(ColorUtil.randomColor()))
        fillBoundingRectIntern(img, view)

def drawBoundingRectIntern(img, rectView, color):
    child = rectView.mChildren

    for view in child:
        ImageUtil.drawRect(img, view.bound(), ColorUtil.cColortoInt(color))
        drawBoundingRectIntern(img, view, color)


HIERARCHY_DEPTH = 3
def getAtomicGUICompon(rootView):
    atomicCompon = []
    searchHierarchyToGetAtomicGUICompon(rootView, 1, atomicCompon)
    return atomicCompon

def searchHierarchyToGetAtomicGUICompon(rectView, dep, compon):
    if(dep == HIERARCHY_DEPTH):
        compon.append(rectView)
        return
    # leaf component
    children = rectView.mChildren
    if len(children) == 0:
        compon.append(rectView)
        return


    for child in children:
        searchHierarchyToGetAtomicGUICompon(child, dep+1, compon)


def processScreenshot(imageLocation):
    fileExitst = os.path.isfile(imageLocation)
    if (not fileExitst):
        return "Can't access the file"
    img_color = cv2.imread(imageLocation)
    img_gray = copy.deepcopy(img_color) # a copy of origin img
    if (len(img_color.shape)==3):
        # multi channel picture, convert to gray
        img_gray  = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    if len(img_color.shape) == 2 :
        height, width = img_color.shape
    elif len(img_color.shape) == 3:
        height, width,channels = img_color.shape

    # dst_denoised = cv2.fastNlMeansDenoising(img_gray)
    canny = Canny()
    dst_edge = canny.findEdge(img_gray)

    showImageId(dst_edge, 'canny contour')
    dst_edge_dilate = canny.addDilate(dst_edge)
    showImageId(dst_edge_dilate, 'dilated contour')

    contourAnalysis = ContourAnalysis()
    contours = contourAnalysis.findContoursWithCanny(dst_edge_dilate)
    # handle contour and return rootView of shot, forming a tree like DS
    contoursOutput = contourAnalysis.analyze(dst_edge_dilate, contours)

    # drawBoundingRect(img_color, contoursOutput.rootView)


    hierarchyProcessor = ViewHierarchyProcessor(contoursOutput.rootView, img_color, canny)
    hierarchyInfo = hierarchyProcessor.process()


    fillBoundingRect(img_color, hierarchyProcessor.hierarchyInfo.rootView)


    atomicGUICompon = getAtomicGUICompon(hierarchyProcessor.hierarchyInfo.rootView)

    drawBoundingRectList(img_color, atomicGUICompon, CColor.Red)
    return atomicGUICompon

