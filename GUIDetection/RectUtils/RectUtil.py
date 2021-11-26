
import sys

from functools import cmp_to_key

import GUIDetection.Utils.ColorUtil as ColorUtil
from GUIDetection.Utils.ColorUtil import *



def contains(t, r, thresHold=-1):
    if (thresHold == -1):
        rx = r.x
        ry = r.y
        rh = r.height
        rw = r.width
        tw = t.width
        th = t.height
        if (tw < 0 or th < 0 or rw < 0 or rh < 0):

            return False

        tx = t.x
        ty = t.y
        if (rx < tx or ry < ty):
            return False

        tw += tx
        rw += rx
        if (rw <= rx):

            if (tw >= tx or rw > tw):
                return False
        else:

            if (tw >= tx and rw > tw):
                return False
        th += ty
        rh += ry
        if (rh <= ry):
            if (th >= ty or rh > th):
                return False

        else:
            if (th >= ty and rh > th):
                return False

        return True

    else:
        if (intersects(t, r)):
            intersection = interection(t, r)
            ratio = float(intersection.area()) / r.area()
            if (ratio >= thresHold):
                return True
        return False


def intersects(t, r):
    tw = t.width
    th = t.height
    rw = r.width
    rh = r.height
    if (rw <= 0 or rh <= 0 or tw <= 0 or th <= 0):
        return False

    tx = t.x
    ty = t.y
    rx = r.x
    ry = r.y
    rw += rx
    rh += ry
    tw += tx
    th += ty
    # overflow or intersect
    return (rw < rx or rw > tx) and (rh < ry or rh > ty) and (tw < tx or tw > rx) and (th < ty or th > ry)


def interection(t, r):
    tx1 = t.x
    ty1 = t.y
    rx1 = r.x
    ry1 = r.y
    tx2 = tx1
    tx2 += t.width
    ty2 = ty1
    ty2 += t.height
    rx2 = rx1
    rx2 += r.width
    ry2 = ry1
    ry2 += r.height
    if (tx1 < rx1):
        tx1 = rx1

    if (ty1 < ry1):
        ty1 = ry1

    if (tx2 > rx2):
        tx2 = rx2

    if (ty2 > ry2):
        ty2 = ry2

    tx2 -= tx1
    ty2 -= ty1

    if (tx2 < - sys.maxsize):
        tx2 = - sys.maxsize

    if (ty2 < - sys.maxsize):
        ty2 = - sys.maxsize

    return Rect(tx1, ty1, tx2, ty2)


def union(t, r):
    tx2 = t.width
    ty2 = t.height
    if ((tx2 | ty2) < 0):
        return Rect(r.x, r.y, r.width, r.height)

    rx2 = r.width
    ry2 = r.height
    if (rx2 < 0 or ry2 < 0):
        return Rect(t.x, t.y, t.width, t.height)

    tx1 = t.x
    ty1 = t.y
    tx2 += tx1
    ty2 += ty1
    rx1 = r.x
    ry1 = r.y
    rx2 += rx1
    ry2 += ry1
    if (tx1 > rx1):
        tx1 = rx1

    if (ty1 > ry1):
        ty1 = ry1

    if (tx2 < rx2):
        tx2 = rx2

    if (ty2 < ry2):
        ty2 = ry2

    tx2 -= tx1
    ty2 -= ty1
    if (tx2 > sys.maxsize):
        tx2 = sys.maxsize

    if (ty2 > sys.maxsize):
        ty2 = sys.maxsize

    return Rect(tx1, ty1, tx2, ty2)


def add(t, newx, newy):
    if (t.width < 0 or t.height < 0):
        t.x = newx
        t.y = newy
        t.width = t.height = 0
        return

    x1 = t.x
    y1 = t.y
    x2 = t.width
    y2 = t.height
    x2 += x1
    y2 += y1
    if (x1 > newx):
        x1 = newx

    if (y1 > newy):
        y1 = newy

    if (x2 < newx):
        x2 = newx

    if (y2 < newy):
        y2 = newy

    x2 -= x1
    y2 -= y1
    if (x2 > sys.maxsize):
        x2 = sys.maxsize

    if (y2 > sys.maxsize):
        y2 = sys.maxsize

    t.reshape(x1, y1, x2, y2)




def add(t, r):
    tx2 = t.width
    ty2 = t.height
    if (tx2 < 0 or ty2 < 0):
        t.reshape(r.x, r.y, r.width, r.height)
    rx2 = r.width
    ry2 = r.height
    if (rx2 < 0 or ry2 < 0):
        return
    tx1 = t.x
    ty1 = t.y
    tx2 += tx1
    ty2 += ty1
    rx1 = r.x
    ry1 = r.y
    rx2 += rx1
    ry2 += ry1
    if (tx1 > rx1):
        tx1 = rx1

    if (ty1 > ry1):
        ty1 = ry1

    if (tx2 < rx2):
        tx2 = rx2

    if (ty2 < ry2):
        ty2 = ry2

    tx2 -= tx1
    ty2 -= ty1
    # tx2,ty2 will never underflow since both original
    # Rects were non-empty
    # they might overflow, though...
    if (tx2 > sys.maxsize):
        tx2 = sys.maxsize

    if (ty2 > sys.maxsize):
        ty2 = sys.maxsize

    t.reshape(tx1, ty1, tx2, ty2)


def reshape(t, x, y, width, height):
    t.x = x
    t.y = y
    t.width = width
    t.height = height


def findBoundOfRects(iRects):
    rect = Rect()
    if (len(iRects) == 0):
        return rect
    top = sys.maxsize
    left = sys.maxsize
    right = - sys.maxsize
    bottom = - sys.maxsize
    for e in iRects:
        left = min(left, e.x)
        top = min(top, e.y)
        right = max(right, e.x + e.width)
        bottom = max(bottom, e.y + e.height)

    rect.x = left
    rect.y = top
    rect.width = right - left
    rect.height = bottom - top
    return rect



def overlap(t, r, threadHold):
    if (intersects(t, r)):
        intersection = interection(t, r)
        ratioR = float(intersection.area()) / r.area()
        ratioT = float(intersection.area()) / t.area()
        if (ratioR >= threadHold and ratioT >= threadHold):
            return True
    return False

def left(t, r):
    return t.x < r.x


def right(t, r):
    return r.x < t.x


def above(t, r):
    return t.y < r.y


def below(t, r):
    return r.y < t.y


def closerLeft(t, r):
    return t.x >= r.x


def closerTop(t, r):
    return t.y >= r.y


def closerRight(t, r):
    return t.x >= r.x


def closerBottom(t, r):
    return t.y >= r.y



def containAll(rect, rects):
    if (len(rects) == 0):
        return False
    containAll = True
    for r in rects:
        if (not contains(rect, r)):
            return False
    return containAll


def contain(rect, rects):
    children = []
    if (len(rects) == 0):
        return children

    for r in rects:
        if (r != rect and contains(rect, r)):
            children.append(r)

    return children


def getLeafNodes(view):
    rectViews = []
    getLeafNodesInternal(None, view, rectViews)
    return rectViews


def getLeafNodesInternal(parent, view, rectViews):
    if (view != None):
        if (parent != None and (view.mChildren == None or len(view.mChildren) == 0)):
            rectViews.append((parent, view))
        else:
            for child in view.mChildren:
                getLeafNodesInternal(view, child, rectViews)


def expandPx(rect, px = 1):
    return Rect(rect.x-px, rect.y-px, rect.width+2*px, rect.height+2*px)