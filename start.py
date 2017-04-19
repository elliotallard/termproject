# mode-demo.py

from tkinter import *

####################################
# init
####################################

BARHEIGHT = 10
STAFFSPACE = 50


#keeps all compose variables  

def init(data, compose):
    # DATA
    data.mode = "compose"
    data.score = 0
    #COMPOSE
    compose.notes = []   
    compose.topStaff = data.height//20 * 2
    compose.bottomStaff = data.height//20 * 19       
    compose.leftStaff = data.width//20
    compose.rightStaff = data.width//20 * 19  
    compose.bars = []    #keeps locations of lines when drawing bars, can ref back to notes 
    compose.noteXPlace = compose.rightStaff //20 + compose.leftStaff
    compose.noteXLimit = compose.rightStaff - 20  
    compose.noteSpace = 20
    compose.noteCurrStaff = 0

####################################
# mode dispatcher
####################################

def mousePressed(event, data, compose):
    if (data.mode == "compose"): composeMousePressed(event, data, compose)
    elif (data.mode == "play"):   playMousePressed(event, data,)
    elif (data.mode == "hear"):       hearMousePressed(event, data)

def keyPressed(event, data, compose):
    if (data.mode == "compose"): composeKeyPressed(event, data,compose)
    elif (data.mode == "play"):   playKeyPressed(event, data)
    elif (data.mode == "hear"):       hearKeyPressed(event, data)

def timerFired(data, compose):
    if (data.mode == "compose"): composeTimerFired(data,compose)
    elif (data.mode == "play"):   playTimerFired(data)
    elif (data.mode == "hear"):       hearTimerFired(data)

def redrawAll(canvas, data,compose):
    if (data.mode == "compose"): composeRedrawAll(canvas, data,compose)
    elif (data.mode == "play"):   playRedrawAll(canvas, data)
    elif (data.mode == "hear"):       hearRedrawAll(canvas, data)

####################################
# compose mode
####################################

def addNote(n, compose, start):
    # print (n)
    num = n - start
    if num == 0: note = "F0"
    if num == 5: note = "E0"
    if num == 10: note = "D0"
    if num == 15: note = "C0"
    if num == 20: note = "B0"
    if num == 25: note = "A0"
    if num == 30: note = "G0"
    if num == 35: note = "F1"
    if num == 40: note = "E1"
    if num == 45: note = "D1"
    if num == 50: note = "C1"
    compose.notes.append((note, "1/4", n))
    return
    # print (compose.notes)

import time

def composeMousePressed(event, data,compose):
    for staff in compose.bars:
        start = staff[0] #getting first and last values of each bar
        end = staff[-1]
        # print (staff)
        for step in range(start, end + 5, 5): #going through the staff, bar by bar
            if step - 2 < event.y < step + 2:
                addNote(step, compose, start)
                return


def composeKeyPressed(event, data,compose):
    pass

def composeTimerFired(data,compose):
    pass

def composeRedrawAll(canvas, data,compose):
    x0,y0 = compose.leftStaff, compose.topStaff
    x1,y1 = compose.rightStaff, compose.bottomStaff
    drawStaff(canvas, compose, data)
    drawNotes(canvas, compose, data)

def drawQuarterNote(canvas, x,y):
    radius = 5 #arbitrary for now
    canvas.create_oval(x-radius,y-radius, x+radius,y+radius, fill = "black")

def drawNotes(canvas, compose, data):
    for note in compose.notes:
        x = compose.noteXPlace
        if x > compose.noteXLimit:
            x = compose.rightStaff //20 + compose.leftStaff
            compose.notexPlace = x
            print (compose.notexPlace)
            compose.noteCurrStaff += 1     #fix later so that music does not go over 6 staffs
        y = note[2]
        if note[1] == '1/4':
            drawQuarterNote(canvas,x,y)
        compose.noteXPlace += compose.noteSpace
        # print (compose.noteXPlace)
    compose.noteXPlace = compose.rightStaff //20 + compose.leftStaff

def drawStaff(canvas, compose, data):
    x0,y0 = compose.leftStaff, compose.topStaff
    x1,y1 = compose.rightStaff, compose.bottomStaff
    currY = y0    #keeps track of where we are on canvas
    while currY < (y1 - 5 * BARHEIGHT + STAFFSPACE):
        currY = drawIndivStaff(canvas, compose, currY)

def drawIndivStaff(canvas, compose, currY):
    y0 = currY
    ys = [] # temp list that collects all y's then adds to compose.bars at the end
    for i in range(5):
        ys.append(y0)
        canvas.create_line(compose.leftStaff, y0, compose.rightStaff, y0)
        y0 += BARHEIGHT
    compose.bars.append(tuple(ys))
    return y0 + STAFFSPACE


             




####################################
# hear mode
####################################

def hearMousePressed(event, data):
    pass

def hearKeyPressed(event, data):
    data.mode = "play"

def hearTimerFired(data):
    pass

def hearRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2-40,
                       text="This is hear mode!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2-10,
                       text="How to play:", font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+15,
                       text="Do nothing and score points!", font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+40,
                       text="Press any key to keep playing!", font="Arial 20")

####################################
# play mode
####################################

def playMousePressed(event, data):
    data.score = 0

def playKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.mode = "hear"

def playTimerFired(data):
    data.score += 1

def playRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2-40,
                       text="This is a fun game!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2-10,
                       text="Score = " + str(data.score), font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+15,
                       text="Click anywhere to reset score", font="Arial 20")
    canvas.create_text(data.width/2, data.height/2+40,
                       text="Press 'h' for hear!", font="Arial 20")

####################################
# use the run function as-is
####################################



def run(width=300, height=300):
    def redrawAllWrapper(canvas, data, compose):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data,compose)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data, compose):
        mousePressed(event, data,compose)
        redrawAllWrapper(canvas, data,compose)

    def keyPressedWrapper(event, canvas, data, compose):
        keyPressed(event, data,compose)
        redrawAllWrapper(canvas, data,compose)

    def timerFiredWrapper(canvas, data, compose):
        timerFired(data,compose)
        redrawAllWrapper(canvas, data, compose)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, compose)
    # Set up data and call init
    class Struct(object): pass
    class Compose(object): pass
    data = Struct()
    compose = Compose()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data, compose)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data, compose))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data, compose))
    timerFiredWrapper(canvas, data, compose)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800,600)


####CITE
# course website, Mode Demo, David Kosbie