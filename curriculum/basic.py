from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('ubuntu-mono', 'Ubuntu-M.ttf'))
pdfmetrics.registerFont(TTFont('league', 'LeagueMono-UltraLight.ttf'))
pdfmetrics.registerFont(TTFont('league-bold', 'LeagueMono-Bold.ttf'))

styles = getSampleStyleSheet()
style = styles['Normal']

class page:
    def __init__(self, 
            canvas, 
            font = 'league',
            W = 595.27, 
            H = 841.89, 
            tm = 25, 
            lm = 25, 
            rm = 25, 
            bm = 25,
            style = getSampleStyleSheet()['Normal']):
        '''
        Basic container for items (figure, section, header...).
        Sets canvas, width (W), height (H) and margins (tm, lm, rm, bm).
        Keeps track of filled verticalSpace.
        '''

        self.canvas = canvas

        self.W = W
        self.H = H
        self.tm = tm
        self.lm = lm
        self.rm = rm
        self.bm = bm

        self.verticalSpace = H - tm
        self.style = style
        
        self.colPos = { 1 : (tm+20),
                        2 : (tm+20, 300),
                        3 : (tm+20, 300, 450),
                        4 : (tm+20, 200, 300, 450)
                        }

    def vfill(self, dy=0):
        '''
        Moves cursor down by dy, and returns new position
        '''
        self.verticalSpace += -dy
        return self.verticalSpace

class items:
    def __init__(self):
        pass

    def addParagrah(self, tC, 
            text = 'default string :-)', 
            lm = 20,
            ):
        # TODO: add check for verticalSpace first, if fail call canvas.showPage()
        # and instance a new page(), as of 2020-09 newPage() is still called 
        # manually x-)

        '''
        Adds paragraph to tC (target container, e.g page-object),
        text formats basic XML (<b></b>) thanks to reportlab.
        Calls appropriate functions ( tC.vill(dy), ) to allocate space
        '''
        # Get cursor position from tC
        x, y = tC.lm + lm, tC.vfill() 
        
        # Define available width and height (aW, aH)
        aW, aH = tC.W-x - tC.rm, tC.H-tC.vfill()

        # Generate Paragraph object from reportgen and wrap()
        P = Paragraph(text, tC.style)
        w, h = P.wrap(aW, aH)
        P.drawOn(tC.canvas, x, y-h)

        # Finally we update cursor position (vertical) on tC
        tC.vfill(dy = h + tC.style.fontSize)

    def hline(self, tC, fill=0, allocateSpace = False):
        '''
        Draws a straight horizontal line from lm to W-rm on tC (target container)
        Does nothing to tC.verticalSpace
        '''

        # Get canvas from tC
        c = tC.canvas
        if allocateSpace == False:
            y = tC.vfill()
        else:
            y = tC.vfill(dy = allocateSpace)

        p = c.beginPath()
        p.moveTo(tC.lm, y)
        p.lineTo(tC.W-tC.rm, y)
        c.saveState()
        c.setStrokeGray(fill)
        c.drawPath(p, stroke=1, fill=1)
        c.restoreState()

        tC.vfill(dy = 10)

    def drawShape(self, tC, points, setFillGray = 0.4):
        '''
        draws arbitrary shape (list of points [(x0,y0), (x1,y1),..])
        on tC
        '''
        p0 = points[0]

        p = tC.canvas.beginPath()
        p.moveTo(*p0)

        for point in points[1:]:
            p.lineTo(*point)

        #close the loop
        p.lineTo(*p0)

        tC.canvas.saveState()
        tC.canvas.setFillGray(setFillGray)
        tC.canvas.drawPath(p, stroke=1, fill=1)
        tC.canvas.restoreState()

    def headerPoints(self, tC, text, fontsize = 10):
        '''
        Calculates corners to be used in self.drawHeader.
        By changing this function the header shape can be altered
        '''

        y0 = tC.vfill()
        x0 = tC.lm
        dy = fontsize*1.2
        length = tC.canvas.stringWidth(text, 'league', fontsize)+dy

        points = (
        (x0, y0), 
        (x0+length, y0),
        (x0+length+dy, y0-dy),
        (x0, y0-dy),
        )
        tC.vfill(dy = dy)

        return points

    def drawHeader(self, tC, text, fontsize=10):
        '''
        1) Draws header on tC according to points determined in 
        self.headerPoints.
        2) Draws string 'text' on top of shape drawn in 1)
        '''
        tC.canvas.saveState()
        self.drawShape(tC, self.headerPoints(tC, text, fontsize))

        string_y0 = tC.vfill() + fontsize*0.2
        tC.canvas.setFillGray(1)
        tC.canvas.setFont('league', fontsize)
        tC.canvas.drawString(tC.lm, string_y0,' ' + text.upper())
        tC.canvas.restoreState()

        self.hline(tC)
        tC.vfill(dy = 3)


    def drawSquare(self, tC, x, y, setFillGray = 0.8, size=5):
        '''
        Draws a basic square
        '''
        self.drawShape(tC, points = [
            (x, y),
            (x+size, y),
            (x+size, y+size),
            (x, y+size)
            ], setFillGray = setFillGray)

    def subHeaderPoints(self, tC, items, fontsize = 10):
        '''
        Function to set positions of subheader bullets according
        to predetermined positions defined in __init__
        '''
        N = len(items)

        # Points are already set in __init__
        points = tC.colPos[N]
        y = tC.vfill()

        if N > 1:
            return points
        else:
            return [points]

    def drawSubHeader(self, tC, items, fontsize = 10):
        '''
        Draws subheader. Default is that each item in items gets a grayscale 
        square as a bullet. Positions are calculated by self.subHeaderPoints
        '''
        # Use corners defined in self.subHeaderPoints
        points = self.subHeaderPoints(tC, items, fontsize = 10) 
        y = tC.vfill()

        # Shading of bullet points
        shades = [1/i for i in range(1, len(points)+1)][::-1]

        for text, x, shade in zip(items, points, shades):
            tC.canvas.drawString(x, y, text)
            self.drawSquare(tC, x-10, y+fontsize/4, setFillGray = shade)





class header:
    def addFigure(self, tC, url, scale=1, **kwargs):
        '''
        Appends a figure in northwest, maintains aspect ratio, can be scaled with
        scale.
        '''
        im = Image.open(url)
        w, h = (i*scale for i in im.size)
        tC.canvas.drawImage(url, tC.lm , tC.H-tC.tm-h, width=w, height=h, **kwargs)
        tC.vfill(dy = h)

        self.fig = {'w' : w, 'h' : h, 'p0' : ( tC.lm, tC.H-tC.tm-h )}


    def addLargeName(self, tC, name='Fake', lastname='Person', fontsize=60, font='league'):
        '''
        Draws your name in capital letters in northeast
        '''
        tC.canvas.saveState()
        tC.canvas.setFont(font, fontsize) 
        tC.canvas.setFillGray(0.4)
        tC.canvas.drawRightString(tC.W-tC.rm,tC.H-tC.tm-fontsize, name.upper())
        tC.canvas.setFillGray(0.8)
        tC.canvas.drawRightString(tC.W-tC.rm,tC.H-tC.tm-fontsize*2, lastname.upper())
        tC.canvas.restoreState()

    def addCurriculum(self, tC, name='Curriculum', lastname='Vitae', fontsize=60, font='league'):
        '''
        Draws your name in capital letters in northeast
        '''
        tC.canvas.saveState()
        tC.canvas.setFont(font, fontsize)
        tC.canvas.setFillGray(0.8)
        tC.canvas.drawString(self.fig['p0'][0]+self.fig['w']+10,tC.H-tC.tm-fontsize, name.upper())
        tC.canvas.setFillGray(0.4)
        tC.canvas.drawString(self.fig['p0'][0]+self.fig['w']+10,tC.H-tC.tm-fontsize*2, lastname.upper())

        tC.canvas.restoreState()
    def addContact(self, tC, items = ['+123456', 'fake@email.com', 'fakeperson.com'], fontsize=10, font='Courier'):
        '''
        Draws a narrow banner incorporating strings in 'items'
        '''

        sep = '           '
        items = [item.upper() for item in items]
        s = sep.join(items)
        tC.canvas.saveState()

        tC.vfill( fontsize )

        tC.canvas.setFont(font, fontsize)
        tC.canvas.drawCentredString(tC.W/2, tC.vfill(), s)
    
        tC.vfill( 4 )
        tC.canvas.restoreState()


