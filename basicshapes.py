


class basicShapes:
    ''' Container for frequently used shapes '''

    def drawShape(self, tC, points, setFillGray = 0.4):
        '''
        draws arbitrary shape (list of points [(x0,y0), (x1,y1),..])
        on tC
        '''
        p0 = points[0]

        #start the loop
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

    def drawTriangle(self, tC, p1,p2,p3):
            ''' Draws basic triangle '''

            c.setFillColor('lime')
            c.setStrokeColor('lime')
            p = c.beginPath()

            p.moveTo(*p1)
            p.lineTo(*p2)
            p.lineTo(*p3)
            p.lineTo(*p1)

            c.drawPath(p, fill=1)

