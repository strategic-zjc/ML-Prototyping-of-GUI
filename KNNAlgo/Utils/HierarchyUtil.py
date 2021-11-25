
from KNNAlgo.Aggregate import *

def drawHierarchy(img, rootNode):
    imgC = copy.deepcopy(img)
    for child in rootNode.children:
        drawGUIBoundingRect(imgC, child)
    showImageId(imgC, 'hierarchy')
def drawGUIBoundingRect(img, node):
    children = node.children
    if len(children) == 0:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(CColor.Red))
    else:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(CColor.Green))
    for child in children:
        drawGUIBoundingRect(img, child)