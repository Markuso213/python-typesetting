import os
from reportlab.pdfgen import canvas
from itertools import combinations
from PIL import Image
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import Color
import re
import datetime
import time
from itertools import cycle
contColors = ['blue', 'green', 'red', 'yellow']
contColors = cycle(contColors)
#####
class basicShapes:
    def __init__(self):
        'Not much to init here, no?'
        pass

    def rectangle( canvas, item, lineColor='lime', fill=0, alpha=1):

        p0 = item.x0, item.y0
        p1 = item.x1, item.y0
        p2 = item.x1, item.y1
        p3 = item.x0, item.y1
        
        c = canvas
        c.saveState()
        lineColor = next(contColors)
        c.setStrokeColor(lineColor)

        c.setFillColor(lineColor, alpha=alpha)
        c.setLineWidth(5)
        p = c.beginPath()

        p.moveTo(*p0)
        p.lineTo(*p1)
        p.lineTo(*p2)
        p.lineTo(*p3)
        p.lineTo(*p0)

        c.drawPath(p, fill = fill)
        c.restoreState()

class frame:
    def __init__(
            self, 
            W = 1920,
            H = 1080,
            left_margin = 10,
            right_margin = 10,
            top_margin = 10,
            bottom_margin = 10,
            slide_counter = 0,
            frames = [],
            slides = [],
                        ):

            self.W = W
            self.H = H
            self.left_margin = left_margin
            self.right_margin = right_margin
            self.top_margin = top_margin
            self.bottom_margin = bottom_margin
            self.slide_counter = slide_counter
            self.frames = frames
            self.slides = slides

            self.items=[]

class freeBox:
    def __init__(self):
        self.W = 500
        self.H = 800
        self.x0 = 200
        self.y0 = 200
        self.x1 = self.x0 + self.W
        self.y1 = self.y0 + self.H


class container:
    '''
    General object for storing an item ('empty', 'figure', 'table', 'string',
    or 'paragraph').
    
    '''
    def __init__(self, parent=None):

        self.parent = parent
        self.W = self.parent.W
        self.H = self.parent.H

        self.items = []
        self.verticalLayout = True
        self.label = 'container'


        self.x0, self.y0 = 0, 0
        self.x1, self.y1 = self.x0+self.W, self.y0+self.H

        self.parent.items.append(self)

    
    def addItem(self, item):
        self.items.append( item )
        self.adjustSizes()


    def vertLayout(self):
        self.verticalLayout = True
        self.horizontalLayout = False


    def horLayout(self):
        self.verticalLayout = False
        self.horizontalLayout = True 


    def adjustSizes(self):
        N = len(self.items)
        nh = self.H/N
        nw = self.W/N
        i = 1

        if self.verticalLayout == True:
            for item in self.items:
                item.y0 = self.H - i*nh
                item.H = nh
                i+=1
                print('adjusting container size')
        else:
            for item in self.items:
                item.y0 = self.W - i*nw
                item.W = nw
                i+=1
            
    def execute(self):
        pass

class figure:
    '''
    Object containing: url, aspectRatio
    Is stored in 'container'.

    Should autoupdate size (self.W, self.H) and origin (self.p0) when 'container'
    changes size.
    '''

    def __init__(self, url, parentContainer, sizeLocked = False):
        print('Initiating new figure')
        self.label = 'figure'
        self.url = url
        self.sizeLocked = sizeLocked 
        self.alignment = 'center'
        self.container = parentContainer

        # Get image dimensions using PIL without reading image into memory
        im = Image.open(self.url)
        self.w, self.h = im.size
        im.close()

        # Set Figure to maximize available space in 'container', without changing
        # aspect ratio

        self.W, self.H = self.container.W, self.container.H
        self.scale = self.findScale()

        self.adjustSizes()
        self.aSFigure(alignment = self.alignment)

        if self not in self.container.items:
            self.container.addItem(self)


    def aSFigure(self, alignment):
        if alignment == 'center':
            self.x0 = (self.container.x0 + self.container.x1)/2 -self.W/2
            self.x1 = self.x0 + self.W
            self.y0 = (self.container.y0 + self.container.y1)/2 -self.H/2
            self.y1 = self.y0 + self.H


    def adjustSizes(self):
        '''
        Function to update size (self.W, self.H) and origin (self.p0) 
        when corresponding parameters in parent 'container' changes.
        '''

        self.W, self.H = self.container.W*self.scale, self.container.H*self.scale
        
        #TODO add option for center, right & left-alignment
        # -- should perhaps be separate functions to be called upon
        print('adjusting figure size')
        if self.label == 'figure':
            self.aSFigure(alignment = self.alignment)


    def findScale(self):
        '''
        Returns scaling factor, as to maximize 'fig' to available 'container',
        Prevents overflowing 'container', and changing aspect ratio of 'fig'.
        '''

        w_r = self.w/self.W
        h_r = self.h/self.H

        if w_r > h_r:
            return w_r
        else:
            return h_r
    

    def execute(self, canvas):
        '''
        Actually draws figure on relevant page.
        '''
        c = canvas
        c.saveState()
        basicShapes.rectangle(c, self)
        c.setLineWidth(15)
        basicShapes.rectangle(c, self.container, lineColor='blue', fill=1, alpha=0.3)
        c.setFontSize(30)
        c.drawString(self.x0, self.y0, 'x0,y0')
        c.drawString(self.x1, self.y0, 'x1,y0')
        c.drawString(self.x0, self.y1, 'x0,y1')
        c.drawString(self.x1, self.y1, 'x1,y1')
        c.drawImage(
                self.url, 
                self.x0, 
                self.y0, 
                width=self.W, 
                height=self.H, 
                )
        c.restoreState()

if __name__ == '__main__':
    pass
