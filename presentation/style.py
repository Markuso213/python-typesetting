


class color:
    black = '#000000'

def drawBoundary(c, p0 = (0,0), ):
    pass

class column:
    def __init__(self, p0 = (20,20), w=100, h=600, **kwargs):
        self.p0 = p0
        self.w = w 
        self.h = h

        self.execution = []

        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def setWidth(self, w):
        self.w = w

    def setHeight(self, h):
        self.h = h

    def setOrigin(self, p0):
        self.p0 = p0 

    def splitColumn(self, h):
        self.p0 = 1

    def execute(self, canvas):
        pass

m = column(p0 = 3, **{'banana' : 1, 'oranges' : 20})

print('Outside: ', m.__dict__)
