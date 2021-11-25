

from GUIDetection.RectUtils.RectUtil import *



VIEW_TYPE_DEFAULT = 0
VIEW_TYPE_TEXT = 1
VIEW_TYPE_IMAGE = 2
VIEW_TYPE_LIST_ITEM = 3
VIEW_TYPE_LIST = 4


def isContanerView(rectView):
    if (rectView != None and (
            rectView.mType == VIEW_TYPE_LIST or rectView.mType == VIEW_TYPE_DEFAULT or rectView.mType == VIEW_TYPE_LIST_ITEM)):
        return True
    return False







