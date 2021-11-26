from GUIDetection.ViewProcess.Canny import Canny
from GUIDetection.ViewProcess.ContourAnalysis import *
from GUIDetection.ViewProcess.HierarchyInfo import *
import os
import cv2
import copy
from GUIDetection.Utils import ImageUtil
from GUIDetection.Utils.ImageUtil import *

from GUIDetection.Utils.ColorUtil import *


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
