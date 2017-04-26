# mode-demo.py

from tkinter import *
#import pyaudio  
import wave 

####################################
# init
####################################

BARHEIGHT = 10
STAFFSPACE = 50


#keeps all compose variables  

def init(data, compose, play):
    # DATA
    data.mode = "compose"
    data.score = 0
    data.tempo = 60
    data.tempoCoords = (400, 35/2)
    data.timerTrack = 0 # if this is odd or even, tells when to switch notes
    data.pause = False
    #COMPOSE
    compose.redoNotes = []
    compose.notes = []   
    compose.topStaff = data.height//20 * 2
    compose.bottomStaff = data.height//2       
    compose.leftStaff = data.width//20 + 50
    compose.rightStaff = data.width//20 * 19  
    compose.bars = []    #keeps locations of lines when drawing bars, can ref back to notes 
    compose.noteXPlace = compose.rightStaff //20 + compose.leftStaff
    compose.noteXLimit = compose.rightStaff - 20  
    compose.noteSpace = 30
    compose.noteCurrStaff = 0
    compose.playButtonCoords = (5,5,100,40)
    compose.playButtonCenter = ((95)/2, 35/2)
    compose.hearButtonCoords = (data.width - 105, 5, data.width - 5, 40)
    compose.hearButtonCenter = (745, 35/2)
    compose.YPlace = compose.topStaff
    compose.count = 0
    timeStr = input("Input a time signature: \n")
    if timeStr == "4/4":
        compose.timeSig = 1
    if timeStr == "2/4":
        compose.timeSig = .5
    if timeStr == "3/4":
        compose.timeSig = .75
    #HEAR
    play.rightStaff, play.leftStaff = compose.rightStaff, compose.leftStaff
    play.topStaff = data.height // 5
    play.bottomStaff = data.height // 5 + 75
    play.note = ""



####################################
# mode dispatcher
####################################

def mousePressed(event, data, compose, play):
    if (data.mode == "compose"): composeMousePressed(event, data, compose)
    elif (data.mode == "play"):   playMousePressed(event, data, play)
    elif (data.mode == "hear"):       hearMousePressed(event, data)

def keyPressed(event, data, compose, play):
    if (data.mode == "compose"): composeKeyPressed(event, data,compose)
    elif (data.mode == "play"):   playKeyPressed(event, data, play)
    elif (data.mode == "hear"):       hearKeyPressed(event, data, compose)

def timerFired(data, compose, play):
    if (data.mode == "compose"): composeTimerFired(data,compose)
    elif (data.mode == "play"):   playTimerFired(data, play, compose)
    elif (data.mode == "hear"):       hearTimerFired(data)

def redrawAll(canvas, data,compose, play):
    if (data.mode == "compose"): composeRedrawAll(canvas, data,compose)
    elif (data.mode == "play"):   playRedrawAll(canvas, data,compose, play)
    elif (data.mode == "hear"):       hearRedrawAll(canvas, data, compose, play)

####################################
# compose mode
####################################

def addNote(n, compose, start):
    compose.redoNotes = []
    lines = 0 #whether or not to draw lines above or below staff for reference
    note = ""
    # print (n)
    num = n - start
    if num == 0: note = "D0"
    if num == 5: note = "C1"
    if num == 10: note = "B1"
    if num == 15: note = "A1"
    if num == 20: note = "G1"
    if num == 25: note = "F1"
    if num == 30: note = "E1"
    if num == 35: note = "D1"
    if num == 40: note = "C2"
    if num == 45: note = "B2"
    if num == 50: note = "A2"
    if num == 55: note = "G2"
    if num == 60: note = "F2"
    if num == 65: note = "E2"
    if num == 70: note = "D2"
    if num == 75: note = "C3"
    if num == 0:
        lines = 4
    if num == 5:
        lines = 3
    if num == 10:
        lines = 2
    if num == 15:
        lines = 1
    if num == 75:
        lines = -1
    compose.notes.append([note, "1/4", n, lines])
    compose.redoNotes.append([note, "1/4",n, lines])


def composeMousePressed(event, data,compose):
    if (compose.playButtonCoords[0] < event.x < compose.playButtonCoords[2] and
        compose.playButtonCoords[1] < event.y < compose.playButtonCoords[3]):
        data.mode = "play"
    if (compose.hearButtonCoords[0] < event.x < compose.hearButtonCoords[2] and
        compose.hearButtonCoords[1] < event.y < compose.hearButtonCoords[3]):
        data.mode = "hear"
    for staff in compose.bars:
        start = staff[0] - 2*BARHEIGHT - 5 #getting first and last values of each bar
        end = staff[-1] + 2*BARHEIGHT - 5
        # print (staff)
        for step in range(start, end + 5, 5): #going through the staff, bar by bar
            if step - 3 < event.y < step + 3:
                addNote(step, compose, start)
                return

def undoNote(compose):
	if compose.notes != []:
		compose.redoNotes.append(compose.notes.pop(-1))

def redoNote(compose):
	if compose.redoNotes != []:
		compose.notes.append(compose.redoNotes.pop(-1))


def composeKeyPressed(event, data,compose):
    if event.keysym == "u":
        undoNote(compose)
    if event.keysym == "r":
        redoNote(compose)
    if event.keysym == "Up": 
        if data.tempo < 225: data.tempo += 1
    if event.keysym == "Down":
        if data.tempo > 0: data.tempo -= 1 

def composeTimerFired(data,compose):
    pass

def composeRedrawAll(canvas, data,compose):
    x0,y0 = compose.leftStaff, compose.topStaff
    x1,y1 = compose.rightStaff, compose.bottomStaff
    drawStaff(canvas, compose, data)
    drawNotes(canvas, compose, data)
    drawPlayButton(canvas, compose, data)
    drawHearButton(canvas, compose, data)
    drawTempoMsg(canvas, compose, data)
    canvas.create_text(data.width/2, data.height - 20, text = "Press 'u' to undo note,'r'to redo")

def drawTempoMsg(canvas, compose, data):
    tempoMsg = "Press up and down arrows to change tempo. Tempo = %d" % (data.tempo)
    canvas.create_text(data.tempoCoords, text = tempoMsg)

def drawPlayButton(canvas, compose, data):
    play = "Play!"
    canvas.create_rectangle(compose.playButtonCoords, fill = "red")
    canvas.create_text(compose.playButtonCenter, text = play)

def drawHearButton(canvas, compose, data):
    play = "Hear It!"
    canvas.create_rectangle(compose.hearButtonCoords, fill = "red")
    canvas.create_text(compose.hearButtonCenter, text = play)

def drawQuarterNote(canvas, x,y, color, lines):
    radius = 5 #arbitrary for now
    noteHeight = 20
    lineRadius = 8
    canvas.create_oval(x-radius,y-radius, x+radius,y+radius, fill = color)
    canvas.create_line(x+radius, y, x+radius, y-noteHeight)
    if lines != None and lines!= 0:
        if lines == 4: #high D
            canvas.create_line(x - lineRadius, y+.5*BARHEIGHT, x+lineRadius,y+BARHEIGHT*(.5))
            canvas.create_line(x - lineRadius, y+(3/2)*BARHEIGHT, x+lineRadius,y+BARHEIGHT*(3/2))
        if lines == 3: #high C
            canvas.create_line(x - lineRadius, y, x+lineRadius,y)
            canvas.create_line(x - lineRadius, y+BARHEIGHT, x+lineRadius,y+BARHEIGHT)
        if lines == 2: #high B
            canvas.create_line(x - lineRadius, y+.5*BARHEIGHT, x+lineRadius,y+BARHEIGHT*(.5))
        if lines == 1: #high A
            canvas.create_line(x - lineRadius, y, x+lineRadius,y)
        if lines == -1: #low C
            canvas.create_line(x - lineRadius, y, x+lineRadius,y)

def drawNotes(canvas, compose, data):
    if compose.notes != []:
        compose.count = 0
        for i in range(len(compose.notes)):
            x = compose.noteXPlace
            print ('x=',x)
            if x >= compose.noteXLimit:
                if compose.notes[i][2] > compose.notes[i-1][2] + STAFFSPACE:
                    x = compose.rightStaff //20 + compose.leftStaff
                    compose.noteXPlace = x
                else:
                    if compose.noteCurrStaff > 3: return 
                    x = compose.rightStaff //20 + compose.leftStaff
                    compose.noteXPlace = x
                    compose.YPlace = compose.notes[i][2] 
                    compose.YPlace += 100
                    compose.notes[i][2] = compose.YPlace
                    # print (compose.notexPlace)
                    compose.noteCurrStaff += 1     #fix later so that music does not go over 6 staffs
            y = compose.notes[i][2]
            if compose.notes[i][1] == '1/4':
                if compose.notes[i][3] != 0:
                    drawQuarterNote(canvas, x, y, "black", compose.notes[i][3])
                else:
                    drawQuarterNote(canvas,x,y, "black", None)
                    
            compose.noteXPlace += compose.noteSpace
            if compose.notes[i][1] == "1/4":
                compose.count += .25
            if almostEqual(compose.count, compose.timeSig):
                compose.count = 0
                print (compose.noteCurrStaff, 'currStaff' )
                drawBarline(canvas, compose,compose.noteXPlace-(.5*compose.noteSpace), compose.noteCurrStaff) 
        compose.noteYPlace = compose.notes[-1][2]
        compose.noteXPlace = compose.rightStaff //20 + compose.leftStaff
        return
        #there has to be some sort of compose.yplace to keep track, otherwise 
        # just moves off the staff (downwards)

def drawStaff(canvas, compose, data):
    x0,y0 = compose.leftStaff, compose.topStaff
    x1,y1 = compose.rightStaff, compose.bottomStaff
    currY = y0    #keeps track of where we are on canvas
    while currY < (y1 - 5 * BARHEIGHT + STAFFSPACE):
        print(currY)
        currY = drawIndivStaff(canvas, compose, currY)

def drawIndivStaff(canvas, compose, currY):
    y0 = currY
    ys = [] # temp list that collects all y's then adds to compose.bars at the end
    for i in range(5):
        ys.append(y0)
        canvas.create_line(compose.leftStaff, y0, compose.rightStaff, y0)
        y0 += BARHEIGHT
    canvas.create_line(compose.leftStaff, currY, compose.leftStaff, y0 - BARHEIGHT) #drawing left barline
    canvas.create_line(compose.rightStaff, currY, compose.rightStaff, y0 - BARHEIGHT) #drawing left barline
    compose.bars.append(tuple(ys))
    return y0 + STAFFSPACE

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


def drawBarline(canvas, compose, x, staff):
    canvas.create_line(x, compose.bars[staff][0], x, compose.bars[staff][-1])



             




####################################
# hear mode
####################################

def hearMousePressed(event, data):
    pass

def hearKeyPressed(event, data, compose):
    if event.keysym == "p":
        for note in compose.notes:
           # playNote(note[0])
            data.timerTrack += 1

def hearTimerFired(data):
    pass

def hearRedrawAll(canvas, data, compose, play):
    canvas.create_text(data.width/2, data.height/4 * 3-40,
                       text="This is hear mode!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/4*3, 
                        text = "press 'p' to hear your composition")
    drawStaff(canvas, compose, data)
    drawMovingNotes(canvas, compose, data, play)

#def playNote(note):
    #define stream chunk   
    chunk = 1024  
    #open a wav format music  
    f = wave.open(r"notes/" + note + ".wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  

    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate() 


####################################
# play mode
####################################

def playMousePressed(event, data, play):
    data.score = 0

def playKeyPressed(event, data,play):
    if event.keysym == "Up": 
        if data.tempo < 225: data.tempo += 1
    if event.keysym == "Down":
        if data.tempo > 0: data.tempo -= 1 

def playTimerFired(data,play, compose):
    data.timerTrack += 1

def playRedrawAll(canvas, data, compose, play):
    drawStaff(canvas, compose, data)
    drawTempoMsg(canvas, compose, data)
    drawMovingNotes(canvas, compose, data, play)
    drawFingerings(canvas,compose, data, play)

def drawMovingNotes(canvas, compose, data, play):
    if not data.pause: 
        for i in range(len(compose.notes)):
            x = compose.noteXPlace
            if x > compose.noteXLimit:
                x = compose.rightStaff //20 + compose.leftStaff
                compose.notexPlace = x
                compose.noteCurrStaff += 1     #fix later so that music does not go over 6 staffs
            y = compose.notes[i][2]
            if compose.notes[i][1] == '1/4':
                if i == data.timerTrack:
                    play.note = compose.notes[i][0]
                    drawQuarterNote(canvas,x,y, "red", compose.notes[i][3])
                else:
                    drawQuarterNote(canvas, x, y, "black", compose.notes[i][3])
            compose.noteXPlace += compose.noteSpace
            # print (compose.noteXPlace)
        compose.noteXPlace = compose.rightStaff //20 + compose.leftStaff

def drawFingerings(canvas, compose, data, play):
    canvas.create_rectangle(0,data.height/2, data.width/2, data.height, fill = "white")
    if play.note == "":
        noteList = [0,0,0,0,0,0,0] #(octave key, 1,2,3,4,5,6)
    elif play.note == "F1":noteList = [1,1,1,1,1,0,0]
    elif play.note == "E1":noteList = [1,1,1,1,1,1,0]
    elif play.note == "D1":noteList = [1,1,1,1,1,1,1]
    elif play.note == "C2":noteList = [0,0,1,0,0,0,0]
    elif play.note == "B2":noteList = [0,1,0,0,0,0,0]
    elif play.note == "A2":noteList = [0,1,1,0,0,0,0]
    elif play.note == "G2":noteList = [0,1,1,1,0,0,0]
    elif play.note == "F2":noteList = [0,1,1,1,1,0,0]
    elif play.note == "E2":noteList = [0,1,1,1,1,1,0]
    elif play.note == "D2": noteList = [0,1,1,1,1,1,1]
    for i in range(len(noteList)):
        print (i)
        if noteList[0] == 1: #octave key:
            print ('hi')
            drawOctaveKey(canvas, "red", data)
        else: drawOctaveKey(canvas, "white", data)
        if i in range(1, 7):
            if noteList[i] == 0:
                drawDigitKey(canvas, "white", i, data)
            else: drawDigitKey(canvas, "red", i, data)

def drawOctaveKey(canvas, color, data):
    distFromStaff = 25
    cx, cy = data.width/8 * 3 / 2, data.height/2 + distFromStaff
    radius = 12
    canvas.create_oval(cx - radius, cy-radius, cx+radius, cy+radius, fill = color)
    canvas.create_text(cx, cy - 16, text = "Octave Key", font = "Arial 7 bold") 

def drawDigitKey(canvas, color, index, data):
    distFromStaff = 50
    radius = 15
    if index <= 3:
        cx1, cy1 = data.width/4, data.height/2 + distFromStaff
        canvas.create_oval(cx1-radius, cy1-radius + (40 * (index-1)), cx1+radius, cy1+radius+ (40 * (index-1)), fill = color)
    else:
        cx2, cy2 = data.width/4, data.height/4 * 3
        canvas.create_oval(cx2-radius, cy2-radius + (40 * (index-3)), cx2+radius, cy2+radius+ (40 * (index-3)), fill = color)

####################################
# use the run function as-is
####################################



def run(width=300, height=300):
    def redrawAllWrapper(canvas, data, compose,play):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data,compose,play)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data, compose,play):
        mousePressed(event, data,compose,play)
        redrawAllWrapper(canvas, data,compose,play)

    def keyPressedWrapper(event, canvas, data, compose,play):
        keyPressed(event, data,compose,play)
        redrawAllWrapper(canvas, data,compose,play)

    def timerFiredWrapper(canvas, data, compose, play):
        timerFired(data,compose, play)
        redrawAllWrapper(canvas, data, compose,play)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, compose, play)
    # Set up data and call init
    class Struct(object): pass
    class Compose(object): pass
    class Play(object): pass
    data = Struct()
    compose = Compose()
    play = Play()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data, compose, play)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data, compose, play))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data, compose, play))
    timerFiredWrapper(canvas, data, compose, play)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800,600) 


####CITE
# course website, Mode Demo, David Kosbie
# wave file playing code: Jean-Francois Fabre
# course website, almostEqual, David Kosbie
