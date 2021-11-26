

from random import *
from GUIDetection.RectUtils.Rect import Rect
import copy
      
MAX_AREA_SCAN = 1000

class CColor:
    White= (255,255,255)         
    Black = (0,0,0)     
    Gray =    (190,190,190)         
    Navy = (0,0,128)     
    Blue = (0,0,255)     
    Sky_Blue = (135,206,250)         
    Cyan = (0,255,255)     
    Dark_Green = (0,100,0)         
    Green_Yellow = (173,255,47) 
    Yellow_Green = (154,205,50)
    Khaki = (240,230,140)         
    Yellow = (255,255,0)         
    Gold = (255,215,0)         
    Brown = (165,42,42)     
    Orange = (255,165,0)
    Red = (255,0,0)     
    Pink = (255,192,203)     
    Violet = (238,130,238)  
    Magenta = (255,0,255)   
    Cyan = (0,255,255)  
    Light_Gray = (211,211,211)
    Dark_gray = (169,169,169)
    Green = (0,255,0)

def	 getImageFromRect(original, rect) :
    newImage = copy.deepcopy(original[int(rect.y):int(rect.y+rect.height),int(rect.x):int(rect.x+rect.width)])
    return newImage

        
def rgbDiff(scaColor1, scaColor2):
    return abs(int(scaColor1[1])-int(scaColor2[1])) + abs(int(scaColor1[2])-int(scaColor2[2])) + abs(int(scaColor1[3])-int(scaColor2[3])) 

def toInt(  a ,   r,   g,   b) :
    return (a & 255) << 24 | (r & 255) << 16 | (g & 255) << 8 | (b & 255) << 0

def alphaColortoInt(cColor):
    return (cColor[0] & 255) << 24 | (cColor[1] & 255) << 16 | (cColor[1] & 255) << 8 | (cColor[2] & 255) << 0

def cColortoInt(cColor):
    a = 255
    return (a & 255) << 24 |(cColor[0] & 255) << 16 | (cColor[1] & 255) << 8 | (cColor[2] & 255) << 0

def getScalar(color):
    r = color and 255
    g = color >> 8 and 255
    b = color >> 16 and 255
    return (r, g, b)
    
    
def randomColor() :
    return (randint(0,255 ), randint(0,255 ), randint(0,255 ),randint(0,255 ))
    
def randomColorInt():
    return toInt(randomColor()[0],randomColor()[1],randomColor()[2],randomColor()[3])

