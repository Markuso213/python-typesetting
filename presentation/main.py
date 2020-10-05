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

#Global_variables
w, h = 1920, 1080
W, H = 1920, 1080

folder = '/home/markus/archive/pypres/'
L = []
I = []
current_frame = None
# Global_counters
slide_counter = 0
frames = []
slides = []


for root, folders, files in os.walk(folder):
    for f in files:
        L.append(root+'/'+f)
    for l in L:
        l.replace('//','/')
    for l in L:
        if l.split('.')[-1] in ['png', 'jpg']:
            I.append(l)
I = [l.replace('//','/') for l in I]
I = [i.split('/') for i in I]


c = canvas.Canvas("presentation.pdf", pagesize=(1920, 1080))

def update_time():
    return str(datetime.datetime.now())

class bullets:
    def __init__(self, **kwargs):
        self.func = 'bullet'
        self.p0 = (800, 200)
        self.loc = None 
        self.offset = 10
        self.S = ['', '']
        self.fontSize=30
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])
         
        self.px = self.p0[0]
        self.py = self.p0[1]

    def execute(self):
        c.saveState()
        c.setFont('Helvetica', self.fontSize)
        self.offset = self.fontSize*1.5
        overhead = c.drawString(self.px+self.fontSize*0.8, self.py, self.S[0])
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h']
        for s,a in zip(self.S[1:], alphabet):
            self.px = self.px
            self.py += -self.offset
            s = a+') ' + s
            c.drawString(self.px,self.py, s)

        c.restoreState()
    


def image(c,  url, p0 = (800,200), scale=1, caption = None,loc=None, offset=None, **kwargs):
    global fig
    fig += 1
    im = Image.open(url)
    w, h = (i*scale for i in im.size)

    if loc:
        if loc=='nw':
            p0 = W - w, H - h
            if offset:
                p0 = W-w*(1+offset), H-h*(1+offset)
                fig += -1

    c.drawImage(url, *p0, width=w, height=h, **kwargs)
    styleSheet = getSampleStyleSheet()
    style = styleSheet['BodyText']

    style.fontSize = 30
    style.spaceBefore = 20
    style.spaceAfter = 20

    if caption:
        P = Paragraph('Fig {}.{}.     '.format(1,fig) + caption, style)
        P.wrap(w, 200)
        P.drawOn(c, p0[0], p0[1]-100)
    
    return {'w' : w, 'h' : h, 'fig': fig, }

i=0
page_counter = 0
frame_counter = 0

class append_string:
    def __init__(self, **kwargs):
        self.func ='str'
        self.center = False
        self.p0 = (800, 200)
        self.str = 'I am a banana'
        self.fontSize = 30
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    def execute(self):
        
        c.setFont('Helvetica', self.fontSize)
        if self.center == True:
            c.drawCentredString(self.p0[0], self.p0[1], self.str)
        else:
            c.drawString(self.p0[0], self.p0[1], self.str)

class append_image:
    def __init__(self, **kwargs):

        self.func = 'im'
        self.url = None
        self.p0 = (800, 200)
        self.scale = 1
        self.caption = None
        self.loc = None 
        self.offset = None
        self.W = W-15-150 
        self.mask = None

        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])
         
        for i in I:
            if '/'.join(i) == self.url:
                self.url = self.url
            elif i[-1] == self.url:
                self.url = '/'.join(i)
                break
            else:
                continue

        self.image = Image.open(self.url)
        self.w = self.image.size[0]*self.scale
        self.h = self.image.size[1]*self.scale

        del self.image

    def execute(self):
        c.drawImage(self.url, *self.p0, width=self.w, height=self.h, mask=self.mask)

        styleSheet = getSampleStyleSheet()
        style = styleSheet['BodyText']
        style.fontSize = 30
        style.spaceBefore = 20
        style.spaceAfter = 20

        if self.caption:
            P = Paragraph('Fig {}.{}.     '.format(1,fig) + selfcaption, style)
            P.wrap(selfw, 200)
            P.drawOn(c, self.p0[0], self.p0[1]-100)

class Frame():
    def __init__(self, **kwargs):
        global page_counter, frame_counter

        if 'titlepage' in kwargs.keys():
            pass
        else:
            page_counter+=1

        self.smart = True
        self.execution = []
        frame_counter +=1
        self.__name__='Frame {}'.format(frame_counter)

        self.frame_counter = frame_counter
        self.page_counter = page_counter
        
        self.pad_x = 88

        self.title = None
        self.W = W-15-150
        self.H = H- 100
        self.slides=[self]

        # Top boxes
        self.title_box_offset = 225 

        self.top_box_height = 75
        self.top_box_width = 800 

        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

        

    def im(self, **kwargs):
        self.execution.append(append_image(**kwargs))
        
    def bullet(self, **kwargs):
        self.execution.append(bullets(**kwargs))

    def string(self, **kwargs):
        self.execution.append(append_string(**kwargs))


    def copy(self, other_frame):
        global frame_counter

        for item in other_frame.execution:
            self.execution.append(item.__class__(**item.__dict__))

        frame_counter += -1

    def draw_title_box(self):
        if self.title:             
            fontSize = 45
            height = 1.2*fontSize
            width = fontSize*len(self.title)+10*fontSize


            temp_w = self.top_box_width/frame_counter

            px = self.title_box_offset + temp_w*(self.frame_counter-1)
            py = H-height-85
            
            SS = 400
            bg_color = Color(12/SS,160/SS,97/SS,alpha=1)

            c.setFillColor(bg_color)
            c.setStrokeColor(bg_color)
            c.rect(px, py, width, height, fill=1)
            
            px_string, py_string = px+1.2*fontSize, py +fontSize*0.2
            c.setFont('Helvetica', fontSize) 
            c.setFillColor('white')
            c.drawString(px_string,py_string, self.title)
        

    def draw_counter(self):

        c.saveState()
        SS = 12 + 160 + 97
        SS = SS*1.3

        counter_background_color = Color(12/SS,160/SS,97/SS,alpha=1)
        SS = SS*0.5
        counter_string_color = Color(12/SS,160/SS,97/SS,alpha=1)

        c.setFillColor(counter_background_color)
        pad_x, pad_y = 15, 15
        width_x, width_y = 150,150
        c.rect(pad_x,H-width_y-pad_y,width_x,width_y, fill=1)

        c.setFillColor(counter_string_color)
        fontSize = 140
        c.setFont('Helvetica', fontSize)
        if self.frame_counter < 10:
            c.drawString(pad_x+fontSize/4,H-width_x/2-fontSize/2, str(self.frame_counter))
        else: 
            c.drawString(pad_x,H-width_x/2-fontSize/2, str(self.frame_counter))
        c.restoreState()

    def triangle(self, p1,p2,p3):
        c.setFillColor('lime')
        c.setStrokeColor('lime')
        p = c.beginPath()

        p.moveTo(*p1)
        p.lineTo(*p2)
        p.lineTo(*p3)
        p.lineTo(*p1)

        c.drawPath(p, fill=1)

    def draw_page_marker(self):
        if self.title:
            temp_w = self.top_box_width/frame_counter

            px = self.title_box_offset + (self.frame_counter-1)*temp_w
            py = H-self.top_box_height
            
            c.setStrokeColor('black')
            c.setFillColor('black')

            size = 30

            p1, p2, p3 = (px, py), (px+size, py), (px+size/2, py-size)
            self.triangle(p1,p2,p3)

    def rectangles_top(self):
        SS = 300
        counter_background_color = Color(12/SS,160/SS,97/SS,alpha=1)
        SS = SS*0.5
        counter_string_color = Color(12/SS,160/SS,97/SS,alpha=1)

        c.setFillColor(counter_background_color)
        pad_x, pad_y = 225, 15

        width_x, width_y = self.top_box_width, self.top_box_height
            
        temp_w = self.top_box_width/frame_counter

        Px = [self.title_box_offset + temp_w*i for i in range(frame_counter+1)]
        Py = [H-width_y for i in range(frame_counter+1)] 
        c.setStrokeColor('lime')

        for px, py, fnum in zip(Px,Py, range(frame_counter+1)):
            if fnum == self.frame_counter-1:
                c.setFillColor('lime')
            else:
                c.setFillColor(counter_background_color)

            c.rect(px, py, temp_w, 50, fill=1)

    def rectangles_bot(self):
        SS = 300
        counter_background_color = Color(12/SS,160/SS,97/SS,alpha=1)
        SS = SS*0.5
        counter_string_color = Color(12/SS,160/SS,97/SS,alpha=1)

        c.setFillColor(counter_background_color)
        pad_x, pad_y = 75, 15
        width_x, width_y = W-2*pad_x, 25
        c.rect(pad_x,pad_y,width_x,width_y, fill=1)
        c.setFont('Helvetica', 30)
        c.drawString(pad_x+10, pad_y+40, update_time())

    def center_image(self, p0, w_im, h_im, w_max, h_max):
        w_ratio, h_ratio = w_max/w_im, h_max/h_im

        if w_ratio < h_ratio:
            scale = w_ratio
        else:
            scale = h_ratio
        
        w = w_im *scale
        h = h_im * scale

        px = p0[0]+w_max-w_im*scale

        py = p0[1]+h_max/2-h_im*scale/2
        
        return w, h, (px, py)



    def end(self):
        self.N = len(self.slides)
        self.w_max = self.W/self.N
        self.h_max = self.H

        self.P0 = [(self.pad_x+self.w_max*i, 0) for i in range(self.N)]
        if self.smart == True: 
            for item, p0 in zip(self.execution, self.P0):
                #print(p0)
                if item.func == 'im':
                    #print(item.w, item.h)
                    item.w, item.h, item.p0 = self.center_image(p0, item.w, item.h, self.w_max, self.h_max)
        

        for item in self.execution:
            if item:
                item.execute()

        self.draw_counter()
        self.rectangles_top()
        self.rectangles_bot()
        self.draw_title_box()
        self.draw_page_marker()
        c.showPage()
        
def frame(reset_slides = True, **kwargs):
    global current_frame, slides, slide_counter

    # Finish up previous slides
    if current_frame:
        current_frame.slides = slides

    frames.append(Frame(**kwargs))
    current_frame = frames[-1]


    # Generate new Frame-object

    if reset_slides != False: 
        slides = []
        slides.append(current_frame)
        slide_counter = 0

    slide_counter += 1
    current_frame.slide_counter = slide_counter


def slide(**kwargs):
    global frame_counter, slide_counter, slides

    slide_to_copy = frames[-1]

    # Generate new frame
    frame(reset_slides = False, slide=True, **kwargs)

    slides.append(current_frame)

    # Copy __dict__ from previous frame
    current_frame.copy(slide_to_copy)

    # Counters
    current_frame.slide_counter = slide_counter
    current_frame.title = frames[-2].title 


def title(s):
    current_frame.title = s

def im(**kwargs):
    current_frame.im(**kwargs)

def add_string(**kwargs):
    current_frame.string(**kwargs)

def add_bullet(**kwargs):
    current_frame.bullet(**kwargs)

for i in range(1):    
    c = canvas.Canvas("presentation.pdf", pagesize=(1920, 1080))
    w, h = 1920, 1080
    W, H = 1920, 1080

    folder = '/home/markus/pypres/'

    # Global_counters
    slide_counter = 0
    frame_counter = 0
    slides = []
    frames = []

    frame()
    current_frame.frame_counter = 0
    title('')
    frame_counter += -1

    add_string(**{'p0' : (W/2,650), 'center':True, 'str' : "Lund University", 'fontSize':90})
    add_string(**{'p0' : (W/2,550), 'center':True, 'str' : 'Characterization of InAs-Al semiconductor-superconductor hybrid devices', 'fontSize': 40})
    add_string(**{'p0' : (W/2,500), 'center':True, 'str' : '30 credits', 'fontSize':25})
    add_string(**{'p0' : (200,375), 'str' : 'Markus Aspegren', 'fontSize':40})
    add_string(**{'p0' : (200,275), 'str' : 'Supervisor: Claes Thelander', 'fontSize':30})
    add_string(**{'p0' : (200,225), 'str' : 'Supervisor: Heidi Potts', 'fontSize':30})

    add_string(**{'p0' : (1200,375), 'str' : 'Defence for title of Master of Science', 'fontSize':30})
    add_string(**{'p0' : (1600,100), 'str' : '2020-06-24', 'fontSize':40})


    frame()
    title('A very short introduction to superconductors')
    im(**{'url' : '1d_dos.png'})

    slide()
    current_frame.frame_counter = 1
    title('A very short introduction to superconductors')
    im(**{'url' : 'hctc.png'})
    add_string(**{'str': 'Wikipedia Commons', 'p0' : (1200,50)})

    frame()
    title('Superconductor hybrids for quantum computing')
    #TODO Append bulletlist
    add_bullet(**{'p0': (500,600), 'S' : ['In short: quantum computers', 'Hybrids show promise as future qubits', 'E.g majorana fermions in S-NW-S/N systems']})

    frame()
    title('The SC proximity effect')
    im(**{'url' : 'proximity1.png'})

    slide()
    current_frame.frame_counter = 3
    im(**{'url' : 'proximity2.png', 'title' : 'Josephson junction'})
    add_string(**{'p0' : (1200,675), 'str' : 'Josephson Junction'})

    frame()
    title('Schematics of the Andreev process')
    im(**{'url' : 'all_doss.png'})

    add_string(**{'p0' : (W/2-100, 770), 'str' : 'Current drive', 'center':True, 'fontSize' : 30})
    add_string(**{'p0' : (W/2+500, 770), 'str' : 'Voltage drive', 'center':True, 'fontSize' : 30})

    frame()
    title('Surviving Josephson junction devices')
    im(**{'url' : 'sem_jj2.png'})


    frame()
    title('Device design: Ti/Al (5/70 nm) contacts')
    im(**{'url' : 'criticalcurrentsweep2.png'})

    slide()
    current_frame.frame_counter = 6
    im(**{'url' : 'critical_currents.png'}, )


    frame()
    title('Voltage driven Josephson junction')
    im(**{'url' : 'vdriveHfield.png'})


    f11 = frame()
    title('Close-up on multiple Andreev reflections')
    im(**{'url' : 'longVDsweep.png'})

    slide()
    current_frame.frame_counter += -1 
    im(**{'url' : 'vdrivemars.png'}, )
    add_string(**{'str': 'On ', 'p0' : (1800,600)})
    add_string(**{'str': 'Off ', 'p0' : (1800,400)})


    f115 = frame()
    title('From excess current to normal barrier')
    im(**{'url' : 'iexc1.png'})
    slide()

    current_frame.frame_counter += -1 
    im(**{'url' : 'excessZ.png'})
    add_string(**{'str': '(Barrier strength)', 'p0' : (1300,175)})
    add_string(**{'str': 'Nieblert. et al (2009)', 'p0' : (1490,675)})

    #TODO add reference



    f135 = frame()
    title('Real devices: Ti/Al and Ti/Au contacts')

    im(**{'url' : 'MA11_16.png'})
    slide()
    current_frame.frame_counter += -1 
    im(**{'url' : 'MA10_18.png'})
    im(**{'url' : 'zbwz.png', 'p0':(700,100), 'scale':0.8})



    f12 = frame()
    title('Transport through a quantum dot.')
    im(**{'url' : 'quantumdotschematic.png'})


    f13 = frame()
    title('Yu-Shiba-Rusinov state')
    im(**{'url' : 'schematicqddos.png'})


    slide()
    current_frame.frame_counter += -1 
    #im(**{'url' : 'ysrbinding.png'})

    frame()
    title('Hardness of the gap')
    im(**{'url' : 'boringsubgaps_all.png'})


    frame()
    title('Sub-gap states')
    im(**{'url' : 'niceSubGaps.png'})



    f16 = frame()
    title('Device 2B, medium degree of proximitisation')
    im(**{'url' : 'subGaps2.png'})



    frame()

    title('Some phase transitions')
    current_frame.smart=False
    im(**{'url' : 'phasetransitions.png', 'p0' : (650,0), 'scale': 1})
    im(**{'url' : 'excitations.png', 'p0' : (0,600), 'scale': 1})


    frame()

    title('Very large proximitisation')
    im(**{'url' : 'device2c.png', 'p0' : (650,0), 'scale': 1})
    im(**{'url' : 'MA11_24.png', 'p0' : (650,0), 'scale': 1})


    for f in frames:
        f.end()

    frame()
    title('Conclusion & outlook')
    current_frame.smart=False
    im(**{'url' : 'sem_jj2.png', 'p0' : (350,700)})
    im(**{'url' : 'longVDsweep.png', 'p0': (200,700), 'scale' : 1})

    im(**{'url' : 'MA11_16.png', 'p0':(650,400)})
    im(**{'url' : 'niceSubGaps.png', 'p0': (200,400)})
    im(**{'url' : 'phasetransitions.png', 'p0': (200,100),'scale' : 0.3})

    add_bullet(**{'S' : [' Future experiment', 'Study molecule (2 QDs) coupled to SC']})

    current_frame.end()


    frame()
    title('Opening up the floor to')
    add_string(**{'p0' : (W/2, 600), 'str' : 'questions!', 'center':True, 'fontSize' : 100})
    current_frame.end()
    c.save()

