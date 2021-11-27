import GUIDetection.RectUtils.RectUtil as RectUtil
from KNNAlgo.Utils.Node import *
from CNNClassifier import classifier
from GUIDetection.Utils.ImageUtil import showGUIComponent


def rectViewsToNodes(rectViews, image):
    showCnt = 0
    nodeList = []
    for rectView in rectViews:
        node = GUINode(rect=rectView.rect)
        node.dep = 1   # init dep
        node_image = image[rectView.y: rectView.y+rectView.height, rectView.x : rectView.x + rectView.width]
        node.img = node_image
        node.classType = classifier.predict(node_image)
        print(f'GUI Component type {node.classType}')
        if showCnt < 5:
            showGUIComponent(node.img,node.classType)
            showCnt+=1
        nodeList.append(node)
    return nodeList


def areaNodes(nodes):
    sum = 0
    for node in nodes:
        sum += node.rect.area()
    return sum


def TreeDepth(GUINode, dep):
    max = dep
    children = GUINode.children
    if(len(children) == 0):
        return dep
    for child in children:
        child_dep = TreeDepth(child, dep+1)
        if(max < child_dep):
            max = child_dep
    return max




def leafNodeIntern(Node, leafNode):
    if len(Node.children) == 0:
        leafNode.append(Node)
        return

    children = Node.children
    for child in children:
        leafNodeIntern(child, leafNode)

def leafNode(targerNode):
    children = targerNode.children
    leafNode = []
    for child in children:
        leafNodeIntern(child, leafNode)
    return leafNode

def containerNode(targetNode):
    children = targetNode.children
    containerNode = []
    for child in children:
        containerNodeIntern(child, containerNode)
    return containerNode

def containerNodeIntern(Node, containerNode):
    children = Node.children
    if(len(children) != 0):
        containerNode.append(Node)
    else:
        return
    for child in children:
        containerNodeIntern(child, containerNode)

def findBoundOfNode(nodes):
    rects = [node.rect for node in nodes]
    return RectUtil.findBoundOfRects(rects)


