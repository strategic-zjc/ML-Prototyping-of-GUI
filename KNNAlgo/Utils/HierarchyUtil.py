
from KNNAlgo.Aggregate import *


from GUIDetection.Utils import ImageUtil
from GUIDetection.Utils.ImageUtil import *

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

def drawNodeRectList(img, nodes, color = CColor.Red, thickness = 2):
    for node in nodes:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(color), thickness=thickness)

def showSelectedScreenLeafNodesAndTargetLayout(img, rootNode, matchedContainer):
    imgC = copy.deepcopy(img)
    leafNodes = leafNode(rootNode)
    drawNodeRectList(imgC, leafNodes)
    drawNodeRectList(imgC, [matchedContainer], CColor.Green, thickness= 4)
    ImageUtil.showImageId(imgC, 'matched screen')


def drawHierarchy(img, rootNode):
    imgC = copy.deepcopy(img)
    for child in rootNode.children:
        drawGUIBoundingRectLeaf(imgC, child)
    for child in rootNode.children:
        drawGUIBoundingRectContainer(imgC,child)
    showImageId(imgC, 'hierarchy')



def drawGUIBoundingRectLeaf(img, node):
    children = node.children
    if len(children) == 0:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(CColor.Red))
    for child in children:
        drawGUIBoundingRectLeaf(img, child)


def drawGUIBoundingRectContainer(img, node):
    children = node.children
    if len(children) != 0:
        ImageUtil.drawRect(img, node.rect, ColorUtil.cColortoInt(CColor.Green), thickness= 3)
    for child in children:
        drawGUIBoundingRectContainer(img, child)