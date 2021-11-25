

import numpy as np
from GUIDetection.RectUtils.Rect import *
from GUIDetection.RectUtils.RectView import *
import cv2

class ContourInfo:
    def __init__(self):
        self.map_data = {}
        self.imageAfterClearProcessedViewArr= []
        self.imageAfterClearProcessedView = np.array(self.imageAfterClearProcessedViewArr)
        self.rootView = RectView()
        self.rects = []


class ContourAnalysis:
    IDENTICAL_CONTOURS_THRESHOLD = 0.75

    d = 3

    sigmaColor = 50

    sigmaSpace = 50

    def findContoursWithCanny(self,imgData):
        contours,hierarchy = cv2.findContours(imgData,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return {'contours':contours, 'hierarchy':hierarchy}

    def analyze(self, imgData, foundContours):
        imageAfterClearProcessedView = np.empty_like(imgData)
        imageAfterClearProcessedView[:] = imgData
        height, width = imgData.shape
        rect = Rect(0, 0, width, height)
        rootView = RectView(rect, None)
        children = []
        self.findExternalContours(imageAfterClearProcessedView, foundContours['contours'], foundContours['hierarchy'],
                                  0, 0, None, children)

        for rawView in children:
            rootView.addChild(rawView)

        contourInfo = ContourInfo()
        contourInfo.imageAfterClearProcessedView = imageAfterClearProcessedView
        contourInfo.rootView = rootView  # root的view
        map_data = {}
        contourInfo.rects = self.creatRects(rootView, map_data)  # 返回rect对象的列表
        contourInfo.map_data = map_data  # rect对象对应的view
        return contourInfo

    def creatRects(self, rootView, map_data):
        rects = []
        self.creatRectsInternal(rootView, rects, map_data)
        return rects

    def creatRectsInternal(self, rootView, rects, map_data):
        bound = rootView.rect
        rects.append(bound)
        map_data[bound] = rootView

        children = rootView.mChildren
        for rectView in children:
            bound = rectView.rect
            rects.append(bound)
            map_data[bound] = rectView
            self.creatRectsInternal(rectView, rects, map_data)

    def findExternalContours(self, imageAfterClearProcessedView, contours, hierarchy, index, level, parent, sibling):
        i = index
        if i < 0:
            return
        while i >= 0:
            buff = hierarchy[0][i]
            contour = contours[i]
            i = buff[0]  # Get the next id contour
            j = buff[2]  # child index
            children = [] # get the children view of current contour

            if j > 0:
                while j >= 0:
                    internalContoursBuff = hierarchy[0][j]
                    self.findExternalContours(imageAfterClearProcessedView, contours, hierarchy,
                                              internalContoursBuff[2], level + 1, contour, children)
                    j = internalContoursBuff[0]

            currentView = None
            (x1, y1, width, height) = cv2.boundingRect(contour)
            currentView = RectView(Rect(x1, y1, width, height))

            sibling.append(currentView)
            if (currentView != None):
                currentView.addAllChild(children)
