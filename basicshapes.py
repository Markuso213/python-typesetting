


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

    def drawBulletSquare(self, tC, x, y, setFillGray = 0.8, size=5):
        '''
        Draws a basic square for bullet lists
        '''
        self.drawShape(tC, points = [
            (x, y),
            (x+size, y),
            (x+size, y+size),
            (x, y+size)
            ], setFillGray = setFillGray)

    def drawMarkerTriangle(self, tC, p1,p2,p3):
            ''' Draws basic triangle used for markers '''
            #TODO update point definitions to match the main style 

            tC.canvas.setFillColor('lime')
            tC.canvas.setStrokeColor('lime')
            p = tC.canvas.beginPath()

            p.moveTo(*p1)
            p.lineTo(*p2)
            p.lineTo(*p3)
            p.lineTo(*p1)

            tC.canvas.drawPath(p, fill=1)

