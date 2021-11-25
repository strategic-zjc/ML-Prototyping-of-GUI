from GUIDetection.RectUtils.Rect import Rect
import GUIDetection.RectUtils.RectUtil as RectUtil
import GUIDetection.RectUtils.RectViewUtil as RecViewUtil



class RectView:

    def __init__(self, rect=Rect(), contour=None):
        self.rect = rect
        self.contour = contour
        self.mChildren = []
        self.mType = RecViewUtil.VIEW_TYPE_DEFAULT
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.mColor = None

    def area(self):
        return self.height * self.width

    def includes(self, bound):
        return RectUtil.contains(self.rect, bound)

    def getOverlapRatio(self):
        overlapRatio = 0.0
        for rawView in self.mChildren:
            overlapRatio += rawView.area()

        return overlapRatio / self.rect.area()

    def addAllChild(self, child):
        self.mChildren.extend(child)

    def addChild(self, rawView):
        self.mChildren.append(rawView)


    def bound(self):
        return self.rect






