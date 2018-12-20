class Memory(object):

    def create_grid(self, canvas):

        ##create rectangle
        #horizontal line up
        canvas.create_line(50, 20, 800, 20)
        #horizontal line down
        canvas.create_line(50, 70, 800, 70)
        #vertical line right
        canvas.create_line(800, 20, 800, 70)
        # vertical line left
        canvas.create_line(50, 20, 50, 70)