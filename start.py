# mode-demo.py

from tkinter import *
import pyaudio  
import wave 

####################################
# init
####################################

BARHEIGHT = 10
STAFFSPACE = 50
ALLNOTES = { #fingerings for each note
                 "D0": [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                "Db0":[1,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "C1": [1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                "Bb1":[1,1,0,0,1,0,0,0,0,0,0,0,0,0],
                "B1":[1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                "A1":  [1,1,1,0,0,0,0,0,0,0,0,0,0,0],
                "Ab1": [1,1,1,1,0,0,0,1,0,0,0,0,0,0],
                "G1": [1,1,1,1,0,0,0,0,0,0,0,0,0,0],
                "Gb1": [1,1,1,1,0,1,0,0,0,0,0,0,0,0],
                "F1":[1,1,1,1,1,0,0,0,0,0,0,0,0,0],
                "E1": [1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                "Eb1":[1,1,1,1,1,1,1,0,0,0,0,1,0,0],
                "D1":[1,1,1,1,1,1,1,0,0,0,0,0,0,0],
                "Db1":[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "C2": [0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                "B2": [0,1,0,0,0,0,0,0,0,0,0,0,0,0],
                "Bb2":[0,1,0,0,1,0,0,0,0,0,0,0,0,0],
                "A2": [0,1,1,0,0,0,0,0,0,0,0,0,0,0],
                "Ab2":[0,1,1,1,0,0,0,1,0,0,0,0,0,0],
                "G2": [0,1,1,1,0,0,0,0,0,0,0,0,0,0],
                "Gb2":[0,1,1,1,0,1,0,0,0,0,0,0,0,0],
                "F2": [0,1,1,1,1,0,0,0,0,0,0,0,0,0],
                "E2": [0,1,1,1,1,1,0,0,0,0,0,0,0,0],
                "Eb2":[0,1,1,1,1,1,1,0,0,0,0,1,0,0],
                "D2": [0,1,1,1,1,1,1,0,0,0,0,0,0,0],
                "Db2":[0,1,1,1,1,1,1,0,0,1,0,0,1,0],
                "C3": [0,1,1,1,1,1,1,0,0,0,0,0,1,0],
                "B3": [0,1,1,1,1,1,1,0,1,0,0,0,1,0]
    }

#keeps all compose variables  

def init(data, compose, play):
    # DATA
    data.mode = "compose"
    data.score = 0
    data.tempo = 60
    data.tempoCoords = (400, 35/2)
    data.timerTrack = 0 # if this is odd or even, tells when to switch notes
    data.timeSigString = "Input a Time Signature Here"
    data.timeSigIsPressed = False
    data.timeSigRectCoords = (data.width/3-100, data.height/4*3,data.width/3+100,data.height/4*3 + 40)
    data.timeSigTextCoords = (data.width/3, data.height/4*3 + 20)
    data.timeSigCursorCoords = (data.width/2, data.height/2)
    data.timeSigCursorOn = False
    data.timerCount = 0
    data.timeSig = ""
    data.timeSigs = ["4/4", "3/4", "2/4","5/4","6/4"]
    data.keySigString = "Input a Key Signature Here"
    data.keySigIsPressed = False
    data.keySigRectCoords = (data.width/3*2-100, data.height/4*3,data.width/3*2+100,data.height/4*3 + 40)
    data.keySigTextCoords = (data.width/3*2, data.height/4*3 + 20)
    data.keySigCursorCoords = (data.width/2, data.height/2)
    data.keySigCursorOn = False
    data.timerCount = 0
    data.keySig = ""
    data.keySigs = ["C","Db","D", "Eb", "E", "F","Gb", "G", "Ab", "A", "Bb", "B"]
    data.rightSpecialTopCoords = (data.width/4+20,data.height*3/4-35, data.width/4+50, data.height*3/4-20)
    data.rightSpecialLeftCoords = (data.width/4+20, data.height*3/4-20, data.width/4+35, data.height*3/4-10)
    data.rightSpecialRightCoords = (data.width/4+35,data.height*3/4-20,data.width/4+50,data.height*3/4-10)
    data.rightSpecialBottomCoords = (data.width/4+20, data.height*3/4-10,data.width/4+50,data.height*3/4+5)
    data.bottomSpecialTopCoords = (data.width/4-50, data.height-45,data.width/4-20,data.height-30)
    data.bottomSpecialBottomCoords=(data.width/4-50, data.height-30,data.width/4-20,data.height-15)
    data.isNoteText = None
    data.notePlayButtonCoords = (data.width/2 - 100, 20, data.width/2 + 100, 50)
    data.notePlayTextCoords = (data.width/2, 35)
    data.helpButtonCoords = (data.width/2 - 100, data.height-35, data.width/2+100, data.height-5) 
    data.helpButtonTextCoords = (data.width/2, data.height - 20)
    #COMPOSE
    compose.keySig = "C"
    compose.redoNotes = []
    compose.notes = [] 
    compose.keySigNotes = []  
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
    compose.timeSig = 1
    compose.currStaff = 0
    #HEAR
    play.rightStaff, play.leftStaff = compose.rightStaff, compose.leftStaff
    play.topStaff = data.height // 5
    play.bottomStaff = data.height // 5 + 75
    play.note = ""
    play.noteButtonCoords = (data.width*3/5 - 70, data.height/2 + 90,
                    compose.rightStaff, data.height/2 + 140)
    play.noteTextCoords = ((data.width*3/5 + compose.rightStaff) / 2 - 30, data.height/2 + 115)
    play.playButtonCoords = (data.width*3/5 - 70, data.height/2 + 20,
                    (data.width*3/5 + compose.rightStaff) / 2 - 50, data.height/2 + 70)
    play.playTextCoords= ((((data.width*3/5 + compose.rightStaff) / 2 - 50) + data.width*3/5 - 70)/2,
                        data.height/2 + 45)
    play.pauseButtonCoords = ((data.width*3/5 + compose.rightStaff) / 2 - 10 , data.height/2 + 20, compose.rightStaff, data.height/2 + 70)
    play.pauseTextCoords = ((((data.width*3/5 + compose.rightStaff) / 2 - 10) + compose.rightStaff) /2,
        data.height/2 + 45)
    play.replayButtonCoords =(data.width*3/5 - 70, data.height/2 + 160,
                    compose.rightStaff, data.height/2 + 210)
    play.replayTextCoords = ((data.width*3/5 + compose.rightStaff) / 2 - 30, data.height/2 + 185)
    play.pause = True
    play.noteList = []



####################################
# mode dispatcher
####################################

def mousePressed(event, data, compose, play):
    if (data.mode == "compose"): composeMousePressed(event, data, compose)
    elif (data.mode == "play"):   playMousePressed(event, data, play, compose)
    elif (data.mode == "hear"):       hearMousePressed(event, data)
    elif (data.mode == "note"): noteMousePressed(event, data, compose, play)
    elif (data.mode == "help"): helpMousePressed(event, data)

def keyPressed(event, data, compose, play):
    if (data.mode == "compose"): composeKeyPressed(event, data,compose)
    elif (data.mode == "play"):   playKeyPressed(event, data, play)
    elif (data.mode == "hear"):       hearKeyPressed(event, data, compose,play)
    elif (data.mode == "note"): noteKeyPressed(event, data, compose, play)
    elif (data.mode == "help"): pass

def timerFired(data, compose, play):
    if (data.mode == "compose"): composeTimerFired(data,compose)
    elif (data.mode == "play"):   playTimerFired(data, play, compose)
    elif (data.mode == "hear"):       hearTimerFired(data)
    elif (data.mode == "note"): noteTimerFired()
    elif (data.mode == "help"): pass

def redrawAll(canvas, data,compose, play):
    if (data.mode == "compose"): composeRedrawAll(canvas, data,compose,play)
    elif (data.mode == "play"):   playRedrawAll(canvas, data,compose, play)
    elif (data.mode == "hear"):       hearRedrawAll(canvas, data, compose, play)
    elif (data.mode == "note"): noteRedrawAll(canvas, data, compose, play)
    elif (data.mode == "help"): helpRedrawAll(canvas, data)

####################################
# compose mode
####################################

NOTEPLACEMENTS = {"D0":0,
                "C1":5,
                "B1":10,
                "A1":15,
                "G1":20,
                "F1":25,
                "E1":30,
                "D1":35,
                "C2":40,
                "B2":45,
                "A2":50,
                "G2":55,
                "F2":60,
                "E2":65,
                "D2":70,
                "C3":75,
                "B3":80
}

#SOMEHOW CREATE A Y VALUE FROM JUST A NOTE AND A CURRSTAFF

def addNote(n, compose, start, staff):
    if isinstance(n, str):
        if len(n) == 3: 
            n = n[0]+n[2]
        num = NOTEPLACEMENTS[n]
        n = 60- 25 + num
    else:
        num = n - start
    lines = 0 #whether or not to draw lines above or below staff for reference
    note = ""
    # print (n)
    if num == 0: 
        note = "D0"
        if compose.keySig in ["B", "E"]: compose.keySigNotes.append("Eb1")
        elif compose.keySig in ["Db", "Gb","Ab"]: compose.keySigNotes.append("Db0")
        else: compose.keySigNotes.append("D0")
    if num == 5: 
        note = "C1"
        if compose.keySig in ["C","Db","Eb","F","G","Ab","Bb"]: compose.keySigNotes.append("C1")
        elif compose.keySig == "Gb": compose.keySigNotes.append("B1")
        else: compose.keySigNotes.append("Db0")
    if num == 10: 
        note = "B1"
        if compose.keySig in ["C","D","E","G","A","B"]: compose.keySigNotes.append("B1")
        else: compose.keySigNotes.append("Bb1")
    if num == 15: 
        note = "A1"
        if compose.keySig in "B": compose.keySigNotes.append("Bb1")
        elif compose.keySig in ["Gb", "Ab", "Eb","Db"]: compose.keySigNotes.append("Ab1")
        else: compose.keySigNotes.append("A1") 
    if num == 20: 
        note = "G1"
        if compose.keySig in ["Gb", "Db"]: compose.keySigNotes.append("Gb1")
        elif compose.keySig in ["E", "A", "B"]: compose.keySigNotes.append("Ab1")
        else: compose.keySigNotes.append("G1")
    if num == 25: 
        note = "F1"
        if compose.keySig in ["G", "D","A","E","B"]: compose.keySigNotes.append("Gb1")
        else: compose.keySigNotes.append("F1")
    if num == 30: 
        note = "E1"
        if compose.keySig in ["Db","Eb","Gb","Ab","Bb"]: compose.keySigNotes.append('Eb1')
        else: compose.keySigNotes.append("E1")
    if num == 35: 
        note = "D1"
        if compose.keySig in ["B", "E"]: compose.keySigNotes.append("Eb1")
        elif compose.keySig in ["Db", "Gb","Ab"]: compose.keySigNotes.append("Db1")
        else: compose.keySigNotes.append("D1")
    if num == 40:
        note = "C2"
        if compose.keySig in ["C","Db","Eb","F","G","Ab","Bb"]: compose.keySigNotes.append("C2")
        elif compose.keySig == "Gb": compose.keySigNotes.append("B2")
        else: compose.keySigNotes.append("Db1")
    if num == 45: 
        note = "B2"
        if compose.keySig in ["C","D","E","G","A","B"]: compose.keySigNotes.append("B2")
        else: compose.keySigNotes.append("Bb2")
    if num == 50: 
        note = "A2"
        if compose.keySig in "B": compose.keySigNotes.append("Bb2")
        elif compose.keySig in ["Gb", "Ab", "Eb","Db"]: compose.keySigNotes.append("Ab2")
        else: compose.keySigNotes.append("A2") 
    if num == 55: 
        note = "G2"
        if compose.keySig in ["Gb", "Db"]: compose.keySigNotes.append("Gb2")
        elif compose.keySig in ["E", "A", "B"]: compose.keySigNotes.append("Ab2")
        else: compose.keySigNotes.append("G2")
    if num == 60: 
        note = "F2"
        if compose.keySig in ["G", "D","A","E","B"]: compose.keySigNotes.append("Gb2")
        else: compose.keySigNotes.append("F2")
    if num == 65: 
        note = "E2"
        if compose.keySig in ["Db","Eb","Gb","Ab","Bb"]: compose.keySigNotes.append('Eb2')
        else: compose.keySigNotes.append("E2")
    if num == 70: 
        note = "D2"
        if compose.keySig in ["B", "E"]: compose.keySigNotes.append("Eb2")
        elif compose.keySig in ["Db", "Gb","Ab"]: compose.keySigNotes.append("Db2")
        else: compose.keySigNotes.append("D2")
    if num == 75: 
        note = "C3"
        if compose.keySig in ["C","Db","Eb","F","G","Ab","Bb"]: compose.keySigNotes.append("C3")
        elif compose.keySig == "Gb": compose.keySigNotes.append("B3")
        else: compose.keySigNotes.append("Db2")
    if num == 80: 
        note =  'B3'
        if compose.keySig in ["C","D","E","G","A","B"]: compose.keySigNotes.append("B3")
        else: compose.keySigNotes.append("Bb2")
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
    if num == 80:
        lines = -2
    compose.notes.append([note, "1/4", n, lines, staff])
    compose.redoNotes = []




def composeMousePressed(event, data,compose):
    if (compose.playButtonCoords[0] < event.x < compose.playButtonCoords[2] and
        compose.playButtonCoords[1] < event.y < compose.playButtonCoords[3]):
        data.timerTrack = 0
        data.mode = "play"
        data.timerTrack = 0
    if (compose.hearButtonCoords[0] < event.x < compose.hearButtonCoords[2] and
        compose.hearButtonCoords[1] < event.y < compose.hearButtonCoords[3]):
        data.mode = "hear"
    # for staff in compose.bars:
    start = compose.bars[compose.noteCurrStaff][0] - 2*BARHEIGHT - 5 #getting first and last values of each bar
    end = compose.bars[compose.noteCurrStaff][-1] + 2*BARHEIGHT - 5
    # print (staff)
    for step in range(start, end + 5, 5): #going through the staff, bar by bar
        if step - 3 < event.y < step + 3:
            addNote(step, compose, start, compose.noteCurrStaff)
            return
    if (data.helpButtonCoords[0] < event.x < data.helpButtonCoords[2] and
        data.helpButtonCoords[1] < event.y < data.helpButtonCoords[3]):
        data.mode = "help"
    timeSigMousePressed(event, data)
    keySigMousePressed(event,data)

def undoNote(compose):
    if compose.notes != []:
        compose.redoNotes.append(compose.notes.pop(-1))
    compose.keySigNotes.pop(-1)


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
    timeSigKeyPressed(event, data, compose)
    keySigKeyPressed(event, data, compose)

def composeTimerFired(data,compose):
    timeSigTimerFired(data)
    keySigTimerFired(data)

def composeRedrawAll(canvas, data,compose, play):
    x0,y0 = compose.leftStaff, compose.topStaff
    x1,y1 = compose.rightStaff, compose.bottomStaff
    drawStaff(canvas, compose, data)
    drawNotes(canvas, compose, data, play)
    drawPlayButton(canvas, compose, data)
    drawHearButton(canvas, compose, data, play)
    drawTempoMsg(canvas, compose, data)
    canvas.create_rectangle(data.helpButtonCoords, fill = "white")
    canvas.create_text(data.helpButtonTextCoords, text = "Help")
    timeSigRedrawAll(canvas, data)
    keySigRedrawAll(canvas, data)
    drawKeyTimeSigMessage(canvas,data)
    canvas.create_text(data.width/2, data.height*3/4 - 100, font = "Arial 30 italic"
            , text = "SaxTutor")

def drawTempoMsg(canvas, compose, data):
    tempoMsg = "Press up and down arrows to change tempo. Tempo = %d" % (data.tempo)
    canvas.create_text(data.tempoCoords, text = tempoMsg)

def drawKeyTimeSigMessage(canvas,data):
    keysig = "Key Signature"
    canvas.create_text(data.keySigTextCoords[0], data.keySigTextCoords[1] - 40, font = "Arial 17 bold",
            text = keysig)
    timesig = "Time Signature"
    canvas.create_text(data.timeSigTextCoords[0],data.keySigTextCoords[1] - 40, font = "Arial 17 bold",
            text = timesig)


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
    if lines!= 0:
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
        if lines == -2: #low B
            canvas.create_line(x-lineRadius, y-(.5*BARHEIGHT),x+lineRadius, y-(.5*BARHEIGHT))

def drawNotes(canvas, compose, data, play):
    if compose.notes != []:
        compose.count = 0
        compose.currStaff = 0
        if len(compose.notes)>60:
            del compose.notes[-1]
        for i in range(len(compose.notes)):
            x = compose.noteXPlace
            if x >= compose.noteXLimit -20:
                if compose.notes[i][2] > compose.notes[i-1][2] + STAFFSPACE:
                    x = compose.rightStaff //20 + compose.leftStaff
                    compose.noteXPlace = x
                else:
                    x = compose.rightStaff //20 + compose.leftStaff
                    compose.noteXPlace = x
                    compose.YPlace = compose.notes[i][2] 
                    compose.YPlace += 100
                    compose.notes[i][2] = compose.YPlace
                    # print (compose.notexPlace)
                    compose.noteCurrStaff += 1     #fix later so that music does not go over 6 staffs
            y = compose.notes[i][2]
            if compose.notes[i][1] == '1/4':
                if data.mode in ["play","hear"] and data.timerTrack == i:
                    play.note = compose.keySigNotes[i]
                    drawQuarterNote(canvas, x, y, "red", compose.notes[i][3])
                else:
                    drawQuarterNote(canvas,x,y, "black", compose.notes[i][3])        
            compose.noteXPlace += compose.noteSpace
            if compose.notes[i][1] == "1/4":
                compose.count += .25
            if almostEqual(compose.count, compose.timeSig):
                compose.count = 0
                drawBarline(canvas, compose,compose.noteXPlace-(.5*compose.noteSpace), compose.notes[i][-1]) 
        compose.noteYPlace = compose.notes[-1][2]
        compose.noteXPlace = compose.rightStaff //20 + compose.leftStaff
        #there has to be some sort of compose.yplace to keep track, otherwise 
        # just moves off the staff (downwards)


def drawStaff(canvas, compose, data):
    x0,y0 = compose.leftStaff, compose.topStaff
    x1,y1 = compose.rightStaff, compose.bottomStaff
    currY = y0    #keeps track of where we are on canvas
    while currY < (y1 - 5 * BARHEIGHT + STAFFSPACE):
        currY = drawIndivStaff(canvas, compose, currY, data)

def drawIndivStaff(canvas, compose, currY, data):
    y0 = currY
    ys = [] # temp list that collects all y's then adds to compose.bars at the end
    for i in range(5):
        ys.append(y0)
        canvas.create_line(compose.leftStaff, y0, compose.rightStaff, y0)
        y0 += BARHEIGHT
    canvas.create_line(compose.leftStaff, currY, compose.leftStaff, y0 - BARHEIGHT) #drawing left barline
    canvas.create_line(compose.rightStaff, currY, compose.rightStaff, y0 - BARHEIGHT) #drawing left barline
    compose.bars.append(tuple(ys))
    top = str(int(compose.timeSig * 4))
    bottom = "4"
    distFromStaffLeft = 10
    f = "Arial 13 bold"
    canvas.create_text(compose.leftStaff - distFromStaffLeft, currY + ((y0-currY)/4),text = top, font=f)
    canvas.create_text(compose.leftStaff - distFromStaffLeft, currY + ((y0-currY-BARHEIGHT)/4*3), text = bottom,font=f)
    drawKeySignature(canvas, compose, currY, y0)
    return y0 + STAFFSPACE

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


def drawBarline(canvas, compose, x, staff):
    canvas.create_line(x, compose.bars[staff][0], x, compose.bars[staff][-1])

def drawKeySignature(canvas, compose, startY, endY):
    startX, endX = compose.leftStaff + 5, compose.leftStaff + 17
    sX, sY = 4, 5 #space between each element's x and y
    f = "Arial 13 bold"
    if compose.keySig == "C": return
    if compose.keySig in ("G", "D","A","E","B"):
        sign = "#"
        if compose.keySig in ["G", "D","A","E","B"]:
            canvas.create_text(startX,startY,text=sign, font=f)
        if compose.keySig in ["D","A","E","B"]:
            canvas.create_text(startX + sX,startY +3*sY, text=sign,font=f)
        if compose.keySig in ["A","E","B"]:
            canvas.create_text(startX + 2 *sX, startY + 6*sY,text=sign,font=f)
        if compose.keySig in ["E","B"]:
            canvas.create_text(startX+3*sX,startY + 2*sY,text=sign,font=f)
        if compose.keySig == "B":
            canvas.create_text(startX + 4*sX,startY+5*sY,text=sign,font=f)
    else: 
        sign = "b"
        if compose.keySig in ["F","Bb","Eb","Ab","Db","Gb"]:
            canvas.create_text(startX, startY + 4*sY, text = sign,font=f)
        if compose.keySig in ["Bb","Eb","Ab","Db","Gb"]:
            canvas.create_text(startX+sX, startY +1*sY, text = sign,font=f)
        if compose.keySig in ["Eb","Ab","Db","Gb"]:
            canvas.create_text(startX+sX*2, startY + 5*sY, text = sign,font=f)
        if compose.keySig in ["Ab","Db","Gb"]:
            canvas.create_text(startX+sX*3, startY + 2*sY, text = sign,font=f)
        if compose.keySig in ["Db","Gb"]:
            canvas.create_text(startX+sX*4, startY + 6*sY, text = sign,font=f)
        if compose.keySig =="Gb":    
            canvas.create_text(startX+sX*5, startY + 3*sY, text = sign,font=f)
######################################
#Time Signature Text Box

def timeSigMousePressed(event, data):
    if (data.timeSigRectCoords[0]<event.x<data.timeSigRectCoords[2] and 
            data.timeSigRectCoords[1]<event.y<data.timeSigRectCoords[3]):
        if data.timeSigIsPressed is False:
            data.timeSigString = ""
        data.timeSigIsPressed = True
    else:
        data.timeSigIsPressed = False

def timeSigKeyPressed(event, data, compose):
    if data.timeSigIsPressed:
        if event.keysym == "BackSpace":
            if len(data.timeSigString) > 0:
                data.timeSigString = data.timeSigString[:-1]
        elif event.keysym == "space":
            data.timeSigString = data.timeSigString + " "
        elif event.keysym == "Return":
            data.timeSigIsPressed = False
            if data.timeSigString in data.timeSigs:
                compose.timeSig = data.timeSigString
                stringToTimeSig(compose)
            else:
                data.timeSigString = "Please input a x/4 time signature"
        else:
            # if len(event.keysym)==1:
            # print ('hi')
            if len(data.timeSigString) > 0 and data.timeSigString[-1] == "|":
                data.timeSigString = data.timeSigString[:-1] + event.keysym
            else:
                if event.keysym.isdigit():
                    data.timeSigString += event.keysym
                if event.keysym == "slash":
                    data.timeSigString += "/" 

def stringToTimeSig(compose):
    if compose.timeSig == "4/4":
        compose.timeSig = 1
    if compose.timeSig == "2/4":
        compose.timeSig = .5
    if compose.timeSig == "3/4":
        compose.timeSig = .75
    if compose.timeSig == "5/4":
        compose.timeSig = 1.25
    if compose.timeSig == "6/4":
        compose.timeSig = 1.5

def timeSigTimerFired(data):
    pass

def timeSigRedrawAll(canvas, data):
    canvas.create_rectangle(data.timeSigRectCoords, fill = "green")
    canvas.create_text(data.timeSigTextCoords, text = data.timeSigString)

             

#########################
#Key Sig Text Box

def keySigMousePressed(event, data):
    if (data.keySigRectCoords[0]<event.x<data.keySigRectCoords[2] and 
            data.keySigRectCoords[1]<event.y<data.keySigRectCoords[3]):
        if data.keySigIsPressed is False:
            data.keySigString = ""
        data.keySigIsPressed = True
    else:
        data.keySigIsPressed = False

def keySigKeyPressed(event, data, compose):
    # print (data.keySigIsPressed)
    if data.keySigIsPressed:
        if event.keysym == "BackSpace":
            if len(data.keySigString) > 0:
                if data.keySigString[-1] == "|":
                    data.keySigString = data.keySigString[:-2]
                else:
                    data.keySigString = data.keySigString[:-1]
        elif event.keysym == "space":
            data.keySigString = data.keySigString + " "
        elif event.keysym == "Return":
            compose.keySigNotes = []
            compose.notes = []
            data.keySigIsPressed = False
            if data.keySigString in data.keySigs:
                compose.keySig = data.keySigString
            else:
                data.keySigString = "Please enter a valid key signature"


        else:
            if len(event.keysym)==1:
                if len(data.keySigString) > 0 and data.keySigString[-1] == "|":
                    data.keySigString = data.keySigString[:-1] + event.keysym
                else:
                    data.keySigString = data.keySigString + event.keysym

def keySigTimerFired(data):
    pass

def keySigRedrawAll(canvas, data):
    canvas.create_rectangle(data.keySigRectCoords, fill = "green")
    canvas.create_text(data.keySigTextCoords, text = data.keySigString)


####################################
# hear mode
####################################

def hearMousePressed(event, data):
    pass

def hearKeyPressed(event, data, compose,play):
    if event.keysym == "p":
        data.timerTrack = 0
        for note in compose.keySigNotes:
           playNote(note)
           data.timerTrack += 1

def hearTimerFired(data):
    pass

def hearRedrawAll(canvas, data, compose, play):
    canvas.create_text(data.width/2, data.height/4 * 3-40,
                       text="This is hear mode!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/4*3, 
                        text = "press 'p' to hear your composition")
    drawStaff(canvas, compose, data)
    drawNotes(canvas, compose, data, play)

def playNote(note):
    # define stream chunk   
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

def playMousePressed(event, data, play, compose):
    if (compose.playButtonCoords[0] < event.x < compose.playButtonCoords[2] and
        compose.playButtonCoords[1] < event.y < compose.playButtonCoords[3]):
        data.mode = "compose"
    if (compose.hearButtonCoords[0] < event.x < compose.hearButtonCoords[2] and
        compose.hearButtonCoords[1] < event.y < compose.hearButtonCoords[3]):
        data.mode = "hear"
    if (play.noteButtonCoords[0] < event.x < play.noteButtonCoords[2] and
        play.noteButtonCoords[1] < event.y < play.noteButtonCoords[3]):
        compose.notes = []
        compose.keySigNotes = []
        play.noteList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        data.isNoteText = None
        data.mode = "note"
    if (play.playButtonCoords[0] < event.x < play.playButtonCoords[2] and
        play.playButtonCoords[1] < event.y < play.playButtonCoords[3]):
        play.pause = False
    if (play.pauseButtonCoords[0] < event.x < play.pauseButtonCoords[2] and
        play.pauseButtonCoords[1] < event.y < play.pauseButtonCoords[3]):
        play.pause = True
    if (play.replayButtonCoords[0] < event.x < play.replayButtonCoords[2] and
        play.replayButtonCoords[1] < event.y < play.replayButtonCoords[3]):
        data.timerTrack = 0

def playKeyPressed(event, data,play):
    if event.keysym == "Up": 
        if data.tempo < 225: data.tempo += 1
    if event.keysym == "Down":
        if data.tempo > 15: data.tempo -= 1
    data.timerDelay = 60000//data.tempo
    print (data.timerDelay)



def playTimerFired(data,play, compose):
    if play.pause == False:
        data.timerTrack += 1


def playRedrawAll(canvas, data, compose, play):
    drawStaff(canvas, compose, data)
    drawTempoMsg(canvas, compose, data)
    drawNotes(canvas, compose, data, play)
    drawFingerings(canvas,compose, data, play)
    drawComposeButton(canvas, compose,data,play)
    drawHearButton(canvas,compose,data,play)
    drawNoteButton(canvas, play)
    drawPlayPlayButton(canvas, play)
    drawPauseButton(canvas, play)
    drawReplayButton(canvas,play)


def drawFingerings(canvas, compose, data, play):
    # canvas.create_rectangle(0,data.height/2, data.width/2, data.height, fill = "white")
    if data.mode != "note":
        if play.note == "":
            play.noteList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0] #(octave key, 1,2,3,4,5,6, left special (top, left, right, bottom), low special (top, bottom), top special)
        else:
            play.noteList  = ALLNOTES[play.note]
    for i in range(len(play.noteList)):
        if play.noteList[0] == 1: #octave key:
            drawOctaveKey(canvas, "red", data)
        else: drawOctaveKey(canvas, "white", data)
        if i in range(1, 7):
            if play.noteList[i] == 0:
                drawDigitKey(canvas, "white", i, data)
            else: drawDigitKey(canvas, "red", i, data)
        if i in range(7, 11):
            if play.noteList[i] == 1:
                drawRightSpecial(canvas, "red", data, i)
            else: drawRightSpecial(canvas, "white", data, i)
        if i in range(11,13):
            if play.noteList[i]==1:
                drawBottomSpecial(canvas, "red", i, data)
            else: drawBottomSpecial(canvas, "white",i,data)
        if i == 13:
            if play.noteList[i]==1:
                drawTopSpecial(canvas, "red",data)
            else:
                drawTopSpecial(canvas, "white", data)


def drawRightSpecial(canvas, color, data, index):
    if index==7: #top
        canvas.create_rectangle(data.rightSpecialTopCoords, fill = color)
    if index == 8: #left
        canvas.create_rectangle(data.rightSpecialLeftCoords, fill = color)
    if index == 9: #right
        canvas.create_rectangle(data.rightSpecialRightCoords, fill = color)
    else: #bottom
        canvas.create_rectangle(data.rightSpecialBottomCoords, fill = color)

def drawBottomSpecial(canvas, color, index, data):
    if index == 11:
        canvas.create_rectangle(data.bottomSpecialTopCoords, fill = color)
    else:
        canvas.create_rectangle(data.bottomSpecialBottomCoords, fill = color)

def drawTopSpecial(canvas, color, data):
    distFromStaff = 50
    data.Tcx, data.Tcy = data.width/8*3/2+ 15, data.height/2 + distFromStaff
    data.Trx, data.Try = 7, 12
    canvas.create_oval(data.Tcx-data.Trx,data.Tcy-data.Try,
        data.Tcx+data.Trx,data.Tcy+data.Try, fill = color)
    canvas.create_text(data.Tcx-30, data.Tcy, 
        text = "D-Key", font = "Arial 7 bold")


def drawOctaveKey(canvas, color, data):
    distFromStaff = 25
    data.OKcx, data.OKcy = data.width/8 * 3 / 2, data.height/2 + distFromStaff
    data.OKradius = 12
    distFromKey = 50
    canvas.create_oval(data.OKcx - data.OKradius, data.OKcy-data.OKradius, 
        data.OKcx+data.OKradius, data.OKcy+data.OKradius, fill = color)
    canvas.create_text(data.OKcx - distFromKey, data.OKcy, 
        text = "Octave Key", font = "Arial 7 bold") 

def drawDigitKey(canvas, color, index, data):
    data.digitDistFromStaff = 50
    data.digitRadius = 15
    if index <= 3:
        cx1, cy1 = data.width/4, data.height/2 + data.digitDistFromStaff
        canvas.create_oval(cx1-data.digitRadius, cy1-data.digitRadius + (
            40 * (index-1)), cx1+data.digitRadius, cy1+data.digitRadius+ (40 * (index-1)), fill = color)
    else:
        cx2, cy2 = data.width/4, data.height/4 * 3
        canvas.create_oval(cx2-data.digitRadius, cy2-data.digitRadius + (40 * (index-3)), cx2+data.digitRadius, 
            cy2+data.digitRadius+ (40 * (index-3)), fill = color)

def drawComposeButton(canvas, compose, data,play):
    words = "Compose!"
    canvas.create_rectangle(compose.playButtonCoords, fill = "red")
    canvas.create_text(compose.playButtonCenter, text = words)

def drawHearButton(canvas, compose, data, play):
    play = "Hear It!"
    canvas.create_rectangle(compose.hearButtonCoords, fill = "red")
    canvas.create_text(compose.hearButtonCenter, text = play)

def drawNoteButton(canvas, play):
    words = "NoteFinder Mode"
    canvas.create_rectangle(play.noteButtonCoords, fill= "green")
    canvas.create_text(play.noteTextCoords, text = words, font = "Helvetica 20 bold" )

def drawPlayPlayButton(canvas, play): #play button for play mode
    words = "Play"
    canvas.create_rectangle(play.playButtonCoords)
    canvas.create_text(play.playTextCoords, text = words, font = "Helvetica 20 bold" )

def drawPauseButton(canvas, play):
    words = "Pause"
    canvas.create_rectangle(play.pauseButtonCoords, fill = "red")
    canvas.create_text(play.pauseTextCoords, text = words, font = "Helvetica 20 bold" )

def drawReplayButton(canvas, play):
    words = "Replay"
    canvas.create_rectangle(play.replayButtonCoords, fill = "green")
    canvas.create_text(play.replayTextCoords, text = words, font = "Helvetica 20 bold" )

####################################
#NOTE MODE
####################################


def noteMousePressed(event, data, compose, play):
    key = clickedIn(event.x, event.y, data, compose, play) #an index in the ALLNOTES list
    if key != None:
        if play.noteList[key] == 0:
            play.noteList[key] = 1
        else:
            play.noteList[key] =0
    if (data.notePlayButtonCoords[0]<event.x<data.notePlayButtonCoords[2] and 
        data.notePlayButtonCoords[1]<event.y<data.notePlayButtonCoords[3]):
        compose.notes = []
        compose.keySigNotes = []
        play.noteList = []
        data.mode = "play"
    if data.isNoteText != "Sorry! This is not a note." and data.isNoteText != "":
        if (play.replayButtonCoords[0]<event.x<play.replayButtonCoords[2] and 
            play.replayButtonCoords[1]+50<event.y<play.replayButtonCoords[3]+50):
            addNote(data.isNote, compose, 0, compose.currStaff)

def clickedIn(x, y, data, compose, play):
    # octave key
    if distance(x, y, data.OKcx,data.OKcy) <= data.OKradius:
        return 0
    #digit keys
    for i in range(1,7):
        if i <= 3:
            cx1, cy1 = data.width/4, data.height/2 + data.digitDistFromStaff + 40 * (i -1)
            if distance(x, y, cx1, cy1) <= data.digitRadius: return i
        else:
            cx2, cy2 = data.width/4, data.height/4 *3 + 40*(i-3)
            if distance(x, y, cx2, cy2) <= data.digitRadius: return i
    #right special
    if (data.rightSpecialTopCoords[0]<x<data.rightSpecialTopCoords[2] and 
        data.rightSpecialTopCoords[1]<y<data.rightSpecialTopCoords[3]):
        return 7
    if (data.rightSpecialLeftCoords[0]<x<data.rightSpecialLeftCoords[2] and 
        data.rightSpecialLeftCoords[1]<y<data.rightSpecialLeftCoords[3]):
        return 8
    if (data.rightSpecialRightCoords[0]<x<data.rightSpecialRightCoords[2] and 
        data.rightSpecialRightCoords[1]<y<data.rightSpecialRightCoords[3]):
        return 9
    if (data.rightSpecialBottomCoords[0]<x<data.rightSpecialBottomCoords[2] and 
        data.rightSpecialBottomCoords[1]<y<data.rightSpecialBottomCoords[3]):
        return 10
    #bottom special
    if (data.bottomSpecialTopCoords[0]<x<data.bottomSpecialTopCoords[2] and 
        data.bottomSpecialTopCoords[1]<y<data.bottomSpecialTopCoords[3]):
        return 11
    if (data.bottomSpecialBottomCoords[0]<x<data.bottomSpecialBottomCoords[2] and 
        data.bottomSpecialBottomCoords[1]<y<data.bottomSpecialBottomCoords[3]):
        return 12
    #top special
    if (x - data.Tcx)**2/(data.Trx)**2 + (y-data.Tcy)**2/(data.Try)**2 <= 1: #ellipse equation
        return 13
    else: return None


def noteKeyPressed(event, data, compose, play):
    if event.keysym == "Return":
        for key in ALLNOTES.keys():
            if ALLNOTES[key] == play.noteList:
                data.isNote = key
                data.isNoteText = key[:-1]
                return 
        data.isNoteText = "Sorry! This is not a note."

def noteRedrawAll(canvas, data, compose, play):
    drawStaff(canvas, compose, data)
    drawFingerings(canvas,compose, data, play)
    drawNoteMessage(canvas, data, compose, play)
    drawNotePlayButton(canvas, play, data)
    drawNotes(canvas, compose, data, play)
    directions = """Click in keys to represent pressed keys, 
    and press enter to see if it's a note!"""
    canvas.create_text(data.width*3/4,data.height/2 + 100,text = directions, font = "Helvetica 12 bold")
    if data.isNoteText != "Sorry! This is not a note." and data.isNoteText != None:
        drawAddNoteButton(canvas, play, data)

def drawNoteMessage(canvas, data, compose, play):
    x, y = data.width/4*3, data.height/4*3
    if data.isNoteText != None:
        canvas.create_text(x,y, text = data.isNoteText, font = "Arial 35 bold")

def noteTimerFired():
    pass

def distance(x0,y0,x1,y1):
    return ((x1-x0)**2 + (y1-y0)**2)**.5

def drawNotePlayButton(canvas, play, data):
    text = "Return to Play Mode"
    canvas.create_rectangle(data.notePlayButtonCoords, fill = "red")
    canvas.create_text(data.notePlayTextCoords,text = text, font = "Arial 12 bold")

def drawAddNoteButton(canvas, play, data):
    words = "See This Note!"
    canvas.create_rectangle(play.replayButtonCoords[0],play.replayButtonCoords[1]+50,
        play.replayButtonCoords[2],play.replayButtonCoords[3]+50, fill = "green")
    canvas.create_text(play.replayTextCoords[0], 
        play.replayTextCoords[1]+50,text = words, font = "Helvetica 20 bold" )

####################################
# HELP MODE
####################################

def helpRedrawAll(canvas, data):
    helpMe = """Welcome to SaxTutor! 
    We hope you find this a very useful tool in learning to play the alto saxophone. 
    Things to know about each mode:

    Compose mode: First, choose a key signature and time signature by entering
    each in their respective boxes, and pressing enter after you have typed
    each in. After completing this, you can start 
    placing notes on the staff by clicking on each space. You can change the tempo
    of your piece here too if you would like. If you accidentally click on 
    a note, you can press "u" to undo the note you just put down, and "r" 
    in order to redo the note you just took away. 

    Hear mode: If you have written something and would like to hear it out loud, 
    click on this mode. If you press play, your composition will be played by an 
    alto saxophone. If you are set, you can return to the compose mode. 

    Play mode: This mode is for practicing your newly composed piece. Press play 
    to visualize going through your piece with a key diagram of the saxophone.
    You can increase tempo here to increase speed, or slow the tempo down 
    to lock down tough jumps between notes. You can also pause in order to 
    practice an individual note. 

    Within play mode, you can see there is a NoteFinder mode.
    
    NoteFinder mode: This is a mode for the curious saxophonist. Many times
    during the learning process, you may find yourself playing a note, but 
    you are not sure what it is. So, click on this mode, click on the keys you
    are pressing, and then press enter to see if what you are playing is a note.
    If it is, you can then press "See this note" to see the note on a staff. 
    """
    text = "Help"
    canvas.create_text(data.width/2, 50, text = text, font = "Arial 35 bold")
    canvas.create_text(data.width/2, data.height/2, text = helpMe)
    canvas.create_text(data.width/2, data.height - 20, text = "Click Anywhere to Return To Compose Mode",
        font = "Arial 25 bold")

def helpMousePressed(event, data):
    data.mode = "compose"


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