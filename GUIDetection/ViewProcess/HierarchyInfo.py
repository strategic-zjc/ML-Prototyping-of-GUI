
import GUIDetection.RectUtils.RectUtil as RectUtil
from GUIDetection.RectUtils.RectView import RectView

from GUIDetection.RectUtils.Rect import Rect
from GUIDetection.Utils import ImageUtil
import GUIDetection.Utils.ColorUtil as ColorUtil


class HierarchyInfo:
    rootView = RectView()
    biMapViewRect = {}


class OrderViewWraper:
    otherView = None

    def __init__(self, view, ranking):
        self.view = view
        self.ranking = ranking

    def getRank(self):
        if (self.otherView == None):
            return self.ranking
        else:
            return self.otherView.getRank() + 0.1


class ViewHierarchyProcessor:
    counter_value = 0

    def __init__(self, rootView, image, canny):
        self.mRootView = rootView
        self.mImage = image
        self.mCanny = canny
        self.hierarchyInfo = HierarchyInfo()

    def countViews(self, view):
        counter = 0
        self.countViewsInternal(view, counter)
        return counter

    def countViewsInternal(self, view, counter):
        counter = counter + 1
        children = view.getChildren()
        for rawView in children:
            self.countViewsInternal(rawView, counter)

    def delFullOverlapViews(self, view):
        rects = set()
        self.delFullOverlapViewsIntenal(view, rects)

    def delFullOverlapViewsIntenal(self, view, rects):
        rects.add(view.bound())
        children = view.mChildren
        removeViews = []
        for rectView in children:
            if (rectView.bound() in rects):
                removeViews.append(rectView)
            else:
                self.delFullOverlapViewsIntenal(rectView, rects)

        view.mChildren = [x for x in view.mChildren if x not in removeViews]

    def delOverlapViews(self, view):
        overlapIndexes = []

        children = view.mChildren
        for rawView in children:
            self.delOverlapViews(rawView)

        removingChildrenIndexes = [False] * len(children)
        for i in range(len(children)):
            rectView = children[i]
            for j in range(i + 1, len(children)):
                otherRectView = children[j]
                if rectView != otherRectView:
                    # Check if Intersects only
                    if (not RectUtil.contains(rectView.bound(), otherRectView.bound()) and not RectUtil.contains(
                            otherRectView.bound(), rectView.bound()) and RectUtil.intersects(rectView.bound(),
                                                                                             otherRectView.bound())):
                        added = False
                        # Check if already in the overlapIndexes
                        for overlapIndex in overlapIndexes:
                            if (i in overlapIndex and j in overlapIndex):
                                added = True
                                break
                            elif i in overlapIndex:
                                overlapIndex.append(j)
                                added = True
                                break
                            elif j in overlapIndex:
                                overlapIndex.append(i)
                                added = True
                                break

                        if (not added):
                            rectViews = []
                            rectViews.append(i)
                            rectViews.append(j)
                            overlapIndexes.append(rectViews)
                        removingChildrenIndexes[i] = True
                        removingChildrenIndexes[j] = True

        newRectViews = []

        # process overlap rect
        for rectViewIndexes in overlapIndexes:
            # find bound
            rectView = children[rectViewIndexes[0]]
            unionRect = rectView.bound()
            for i in range(1, len(rectViewIndexes)):
                r = children[rectViewIndexes[i]]
                unionRect = RectUtil.union(unionRect, r.bound())

            newRectViewParent = RectView(Rect(unionRect.x, unionRect.y, unionRect.width, unionRect.height), None)
            for index in rectViewIndexes:
                newRectViewParent.addChild(children[index])

            removingChildrenIndexes[rectViewIndexes[0]] = False
            view.mChildren[rectViewIndexes[0]] = newRectViewParent
            newRectViews.append(newRectViewParent)

        # now we make sure all other children of the parent inside union rect
        # go under this view too.
        for rectView in newRectViews:
            for i in range(len(removingChildrenIndexes)):
                rawView = children[i]
                if rawView != rectView and not removingChildrenIndexes[i]:
                    bound = children[i].bound()
                    if (RectUtil.contains(rectView.bound(), bound)):
                        rectView.addChild(children[i])
                        removingChildrenIndexes[i] = True

                        # now update the children
        rawViews = []
        for i in range(len(removingChildrenIndexes)):
            if (not removingChildrenIndexes[i]):
                rawViews.append(children[i])

        view.mChildren = [x for x in children if x in rawViews]

    def process(self):
        self.basicProcess()

        self.mBiMapViewRect = {} # from RectView to Rect
        self.creatMap(self.mBiMapViewRect, self.mRootView)
        self.hierarchyInfo.rootView = self.mRootView
        self.hierarchyInfo.biMapViewRect = self.mBiMapViewRect

        return self.hierarchyInfo

    def creatMap(self, biMap, view):
        children = view.mChildren
        for rawView in children:
            biMap[rawView] = rawView.bound()
            self.creatMap(biMap, rawView)

    def basicProcess(self):
        # de-overlap views
        self.delOverlapViews(self.mRootView)

        # we reorganize rectangles so that it has the right children
        # sometimes, one rectangle belong to one or the other
        self.reorganizeParentChildHierachyInternal(self.mRootView)
        # de-full-overlap views
        self.delFullOverlapViews(self.mRootView)


    def getSmallestBoundRect(self, mRectBoundOfTexts, rect):
        smalledRect = Rect()
        # check if there is any rectangle contains with this rect
        for erRect in mRectBoundOfTexts:
            if (RectUtil.contains(erRect, rect)):
                if (smalledRect.area() == 0):
                    smalledRect = erRect
                elif (RectUtil.contains(smalledRect, erRect)):
                    smalledRect = erRect

        return smalledRect

    def reorganizeParentChildHierachyInternal(self, view):
        children = view.mChildren
        for childView in view.mChildren:
            self.reorganizeParentChildHierachyInternal(childView)

        hierachy = {}
        len(children)

        for i in range(len(children)):
            rectView = children[i]
            for j in range(i + 1, len(children)):
                otherRectView = children[j]
                if (rectView != otherRectView):
                    if (RectUtil.contains(rectView.bound(), otherRectView.bound())):
                        if j in hierachy and i in hierachy[j]:
                            pass
                        else:
                            childrenIndexes = []

                            if (not i in hierachy):
                                childrenIndexes = []
                                hierachy[i] = childrenIndexes
                            else:
                                childrenIndexes = hierachy[i]

                            if (not j in childrenIndexes):
                                childrenIndexes.append(j)


                    elif (RectUtil.contains(otherRectView.bound(), rectView.bound())):
                        if i in hierachy and j in hierachy[i]:
                            # "This is wrong: " + i+ "  already is parents of " + j);
                            pass
                        else:
                            childrenIndexes = []

                            if (not j in hierachy):
                                childrenIndexes = []
                                hierachy[j] = childrenIndexes
                            else:
                                childrenIndexes = hierachy[j]

                            if (not i in childrenIndexes):
                                childrenIndexes.append(i);

        # remove view if it children claim that its contain that view
        optinmizedHierarchy = {}
        parentIndexes = []
        for i in hierachy:
            childrenIndexes = hierachy[i]
            newChildrenIndexes = []
            for childrenIndex in childrenIndexes:
                # remove grandchildren belong to its children

                if childrenIndex in hierachy:
                    grandChildrenIndexes = hierachy[childrenIndex]
                    newChildrenIndexes = [x for x in newChildrenIndexes if x not in grandChildrenIndexes]

            optinmizedHierarchy[i] = newChildrenIndexes
            parentIndexes.append(i)

        # remove duplication of children        
        includedChildrenIndexes = set()
        for parentIndex in parentIndexes:
            childrenIndexes = optinmizedHierarchy[parentIndex]
            includedChildrenIndexes.update(childrenIndexes)
            childrenIndexes.clear()
            childrenIndexes.extend(includedChildrenIndexes)

        # now we reordering the hierarchy
        for i in optinmizedHierarchy:
            childrenIndexes = optinmizedHierarchy[i]
            childrenIndexes.sort()
            rawView = children[i]
            for childIndex in childrenIndexes:
                rawView.addChild(children[childIndex]);

        removingChildrenIndexes = [False] * len(children)
        # all children value of this hierarchy map will be removed
        for i in optinmizedHierarchy:
            childrenIndexes = optinmizedHierarchy[i]
            for childIndex in childrenIndexes:
                removingChildrenIndexes[childrenIndex] = True

        # now we add parent according to order
        rawViews = []
        indexes = []
        for i in range(len(removingChildrenIndexes)):
            if (not removingChildrenIndexes[i]):
                indexes.append(i)

        indexes.sort()
        for index in indexes:
            rawViews.append(children[index])

        view.mChildren = [x for x in children if x in rawViews]

    def reorganizeOrder(self, view):
        children = view.getChildren()
        orderViewWrapers = {}
        for childView in children:
            orderViewWraper = OrderViewWraper(childView, children.index(childView))
            orderViewWrapers[childView] = orderViewWraper

        for childView in children:
            for otherChildView in children:
                # we want compare reference here!
                # check if we need to move the rectangle to lower level
                if (otherChildView != childView):
                    childBound = childView.bound()
                    otherChildBound = otherChildView.bound()
                    if (RectUtil.intersects(childBound, otherChildBound)):
                        otherGrandChildren = otherChildView.getChildren()
                        # this child did not overlap any children of the
                        # other child overlap
                        overlap = False
                        for rawView in otherGrandChildren:
                            if (RectUtil.intersects(childBound, rawView.bound())):
                                overlap = True
                                break

                        if (not overlap and children.index(childView) < children.index(otherChildView)):
                            orderViewWraper = orderViewWrapers[childView]
                            otherOrderViewWraper = orderViewWrapers[otherChildView]
                            orderViewWraper.otherView = otherOrderViewWraper

        sortedOrderViewWrapers = orderViewWrapers.values()
        sortedOrderViewWrapers.sort(self.OrderViewWrapers)
        children = []
        for orderViewWraper in sortedOrderViewWrapers:
            children.append(orderViewWraper.view)

    def OrderViewWrapers(self, a, b):
        return a.getRank() > b.getRank()
