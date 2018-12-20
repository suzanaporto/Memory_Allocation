from tkinter import *
from First_Fit import First_fit
from Best_Fit import Best_fit
from Worst_Fit import Worst_fit

def __main__():

    #create frame
    animation = Tk()

    #title for the frame
    animation.title("Memory Allocation Simulator")

    #put window upfront every window
    animation.lift()
    animation.attributes('-topmost', True)
    animation.after_idle(animation.attributes, '-topmost', False)

    ##Position window in middle
    # Gets the requested values of the height and width.
    windowWidth = animation.winfo_reqwidth()
    windowHeight = animation.winfo_reqheight()
    print("Width", windowWidth, "Height", windowHeight)
    # Gets both half the screen width/height and window width/height
    positionRight = int(animation.winfo_screenwidth()/4 - windowWidth / 2)
    positionDown = int(animation.winfo_screenheight()/4 - windowHeight / 2)
    # Positions the window in the center of the page.
    animation.geometry("+{}+{}".format(positionRight, positionDown))

    #create two containers/ first one is buttons/ second one is canvas
    container1 = Frame(animation)
    container2 = Frame(animation)

    #pack both containters
    container1.pack()
    container2.pack()

    font_settings = ('Arial', '45', 'bold')

    Label(container1, text='MEMORY ALLOCATION SIMULATOR',
          font=font_settings).pack(side=TOP)

    #create canvas passing frame, width and height
    canvas = Canvas(container2, width=850, height=250)
    canvas.pack()

    #creating first_fit/best_fit/worst_fit instances
    ff = First_fit()
    bf = Best_fit()
    wf = Worst_fit()

    #create buttons
    btn_first = Button(container1, text="First Fit", fg='red', bg='green')
    btn_first.pack(side=LEFT)
    btn_best = Button(container1, text="Best Fit", fg='red', bg='green')
    btn_best.pack(side=LEFT)
    btn_worst = Button(container1, text="Worst Fit", fg='red', bg='green')
    btn_worst.pack(side=LEFT)

    #create button events methods to run algorithms
    def first_run_event():
        ff.First_fit_run(canvas)

    def best_run_event():
        bf.Best_fit_run(canvas)

    def worst_run_event():
        wf.Worst_fit_run(canvas)

    #bind click-event to button
    btn_first.config(command=first_run_event)
    # bind click-event to button
    btn_best.config(command=best_run_event)
    # bind click-event to button
    btn_worst.config(command=worst_run_event)

    #standart method
    animation.mainloop()

#run main
if __name__ == '__main__':
    __main__()