import xml.etree.ElementTree as ET
from GUIDetection.RectUtils.RectUtil import  *
import GUIDetection.RectUtils.RectUtil as RectUtil


from GUIDetection.RectUtils.Rect import *




class GUIHierarchy:
    def __init__(self, xml_node):
        self.rootNode = GUINode(xml_node)
        self.leafNodes = []


class GUINode:
    def __init__(self, xml_node = None, rect = Rect()):
        self.classType = ""
        self.rect = rect
        self.children = []
        self.dep = 0
        self.parent = None
        self.text = ""
        self.img = None
        self.x, self.y, self.height, self.width = rect.x, rect.y, rect.height, rect.width
        if xml_node != None:
            self.parseTreeRoot(xml_node)


    def parseTreeRoot(self, xml_node):
        self.classType = xml_node.tag
        assert xml_node.tag == 'hierarchy'
        for child_node in xml_node:
            self.children.append(self.parseTreeInternal(child_node, self, 1))

    def parseTreeInternal(self, xml_node, parent,dep):
        node = GUINode()
        node.dep = dep
        node.parent = parent
        attr = xml_node.attrib
        bound = attr['bounds'] # [0,0][12,12] like
        node.x , node.y = list(map(int,bound[1:bound.find(']')].split(',')))
        x_br, y_br = list(map(int, bound[bound.find(']',)+2:-1].split(',')))
        node.height, node.width = y_br - node.y, x_br - node.x
        node.classType = attr['class']
        node.rect = Rect(node.x, node.y, node.width, node.height)
        for child_node in xml_node:
            node.children.append(self.parseTreeInternal(child_node, node, dep+1))
        return node
    def setRect(self, rect):
        self.rect = rect
        self.x, self.y, self.height, self.width = rect.x, rect.y, rect.height, rect.width

    def contains(self, another):
        return RectUtil.contains(self.rect, another.rect)

class XmlParser:

    def __init__(self, xmlLocation):
        self.tree = ET.parse(xmlLocation)
        self.rootNode = GUINode(self.tree.getroot())

    def getHierarchy(self):
        return self.rootNode


