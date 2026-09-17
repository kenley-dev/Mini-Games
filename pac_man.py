from cmu_graphics import *

# Fill me in!
app.background = 'black'
app.stepsPerSecond = 1

##Instructions
instructions = Group(
    Label("a, s, w, d, for movement", 200, 115, font='orbitron', fill = 'white', bold = True),
    Label("white food is worth 1 point", 200, 130, font='orbitron', fill = 'white', bold = True),
    Label("cyan food is worth 3 points", 200, 145, font='orbitron', fill = 'white', bold = True),
    Label("tap SPACEBAR to escape", 200, 160, font='orbitron', fill = 'white', bold = True),
    Label("Hitting walls decreases HP!", 200, 175, font='orbitron', fill = 'white', bold = True)
    )

###Time remaining
Label('Time:', 310, 20, size=20, font='orbitron', fill = 'white', bold = True)
timer = Label(30, 365, 21, size=20, font='orbitron', fill = 'white', bold = True)
def onStep():
    timer.value -= 1
    
###Scoring display
Label('Score:', 50, 20, size=20, font='orbitron', fill = 'white', bold = True)
score = Label(0, 110, 21, size=20, font='orbitron', fill = 'white', bold = True)

###PacMan
pacMan = Group(
    Arc(200, 210, 28, 28, 120, 300, fill='yellow'),
    Oval(197, 205, 8, 10, fill='white'),
    Oval(197, 205, 4, 8, fill='black')
    )

###Health points property
pacMan.healthPoints = 0
Label('HP:', 185, 20, size=20, font='orbitron', fill = 'white', bold = True)
HP = Label(5, 225, 21, size=20, font='orbitron', fill = 'white', bold = True)

#Gate
gate = Line(145, 245, 255, 245, fill='white', lineWidth = 3)

###This helper function checks for a collision between PacMan and the food items
###If tehre is contact the player's points will increase by 1 or 3 base on the colour of food
###and then the food will diappear by moving its centerX and centerY off the screen
def checkFoodCollision():
    for food, points in foodItems:
        if pacMan.hitsShape(food):
            score.value += points
            food.centerY = 500
            food.centerX = 500

###OnKeyPress Events
def onKeyPress(key):
    if (key == 'd'):
        ##Rotate to face the right way
        pacMan.rotateAngle = 0
        ##Move pacman in the correct direction
        pacMan.centerX += 10
        ##This second if statement ensures that if pacMan collides with walls it does not move
        if (pacMan.hitsShape(field)):
            pacMan.centerX -= 10
            pacMan.centerY += 0
            ###Take away healthPoints
            pacMan.healthPoints -=1
            if pacMan.healthPoints != 0:
                HP.value -=1
    elif (key == 'a'):
        pacMan.rotateAngle = 180
        pacMan.centerX -= 10
        if (pacMan.hitsShape(field)):
                pacMan.centerX += 10
                pacMan.centerY += 0
                pacMan.healthPoints -=1
                if pacMan.healthPoints != 0:
                    HP.value -=1
    elif (key == 'w'):
        pacMan.rotateAngle = 270
        pacMan.centerY -= 10
        if (pacMan.hitsShape(field)):
                pacMan.centerX += 0
                pacMan.centerY += 10
                pacMan.healthPoints -=1
                if pacMan.healthPoints != 0:
                    HP.value -=1
    elif (key == 's'):
        pacMan.rotateAngle = 90
        pacMan.centerY += 10
        if (pacMan.hitsShape(field)):
                pacMan.centerX += 0
                pacMan.centerY -= 10
                pacMan.healthPoints -=1
                if pacMan.healthPoints != 0:
                    HP.value -=1
    ##This else statement ensures that if any other key is pressed excpet for the ones permissable, pacMan will not move
    else:
        pacMan.centerX += 0
        pacMan.centerY += 0
        
    ##Wrap-around feature
    if (pacMan.centerX <= 0):
        pacMan.centerX = 399
    if (pacMan.centerX >= 400):
        pacMan.centerX = 1
    if (pacMan.centerY <= 40):
        pacMan.centerY = 399
    if (pacMan.centerY >= 400):
        pacMan.centerY = 70
    
    #Open gate & Remove instructions
    if (key == 'space'):
        gate.visible = False
        instructions.visible = False
    
    ##GAMEOVER!
    if timer.value <= 0:
        timer.value = 0
    if timer.value == 0 or pacMan.healthPoints == -5:
        Label('GAME OVER!', 200, 140, size=40, font='orbitron', fill = 'white')
        app.stop()
        
def onKeyRelease(key):
    ## Ensuring that after the kney is released the food item is cleared from the screen, and that collisions are checked
    pacMan.toFront()
    checkFoodCollision()

###Field
field = Group(Polygon(0, 40, 400, 40, 400, 100, 360, 100, 360, 240, 400, 240, 400, 250, 350, 250, 350, 90, 390, 90, 390, 50, 10, 50,
                10, 90, 50, 90, 50, 250, 0, 250, 0, 240, 40, 240, 40, 100, 0, 100, border='navy', borderWidth = 3),
                Polygon(0, 300, 100, 300, 100, 310, 10, 310, 10, 400, 0, 400, border='navy', borderWidth = 3),
                Polygon(400, 300, 300, 300, 300, 310, 390, 310, 390, 400, 400, 400, border='navy', borderWidth = 3),
                Polygon(50, 350, 100, 350, 100, 400, 50, 400, border='navy', borderWidth = 3),
                Rect(60, 360, 30, 30, border='navy', borderWidth = 3),
                Polygon(350, 350, 300, 350, 300, 400, 350, 400, border='navy', borderWidth = 3),
                Rect(310, 360, 30, 30, border='navy', borderWidth = 3),
                Polygon(145, 300, 255, 300, 255, 400, 145, 400, border='navy', borderWidth = 3),
                Rect(155, 310, 90, 80, border='navy', borderWidth = 3),
                Polygon(90, 90, 90, 250, 145, 250, 145, 240, 100, 240, 100, 100, 
                300, 100, 300, 240, 255, 240, 255, 250, 310, 250, 310, 90, border='navy', borderWidth=3),
                gate
            )

###Creating Food
f1 = Circle(35, 70, 4, border='cyan', borderWidth=4, fill=None)
f2 = Circle(75, 70, 4, border='white', borderWidth=4, fill=None)
f3 = Circle(115, 70, 4, border='white', borderWidth=4, fill=None)
f4 = Circle(155, 70, 4, border='white', borderWidth=4, fill=None)
f5 = Circle(195, 70, 4, border='white', borderWidth=4, fill=None)
f6 = Circle(235, 70, 4, border='cyan', borderWidth=4, fill=None)
f7 = Circle(275, 70, 4, border='white', borderWidth=4, fill=None)
f8 = Circle(315, 70, 4, border='white', borderWidth=4, fill=None)
f9 = Circle(355, 70, 4, border='white', borderWidth=4, fill=None)
f10 = Circle(20,275, 4, border='white', borderWidth=4, fill=None)
f11 = Circle(60, 275, 4, border='white', borderWidth=4, fill=None)
f12 = Circle(100, 275, 4, border='white', borderWidth=4, fill=None)
f13 = Circle(140, 275, 4, border='white', borderWidth=4, fill=None)
f14 = Circle(180, 275, 4, border='white', borderWidth=4, fill=None)
f15 = Circle(220, 275, 4, border='white', borderWidth=4, fill=None)
f16 = Circle(260, 275, 4, border='white', borderWidth=4, fill=None)
f17 = Circle(300, 275, 4, border='white', borderWidth=4, fill=None)
f18 = Circle(340, 275, 4, border='white', borderWidth=4, fill=None)
f19 = Circle(380, 275, 4, border='cyan', borderWidth=4, fill=None)
f20 = Circle(70, 235, 4, border='cyan', borderWidth=4, fill=None)
f21 = Circle(70, 195, 4, border='white', borderWidth=4, fill=None)
f22 = Circle(70, 155, 4, border='white', borderWidth=4, fill=None)
f23 = Circle(70, 115, 4, border='white', borderWidth=4, fill=None)
f24 = Circle(330, 235, 4, border='white', borderWidth=4, fill=None)
f25 = Circle(330, 195, 4, border='white', borderWidth=4, fill=None)
f26 = Circle(330, 155, 4, border='white', borderWidth=4, fill=None)
f27 = Circle(330, 115, 4, border='white', borderWidth=4, fill=None)
f28 = Circle(120, 305, 4, border='cyan', borderWidth=4, fill=None)
f29 = Circle(120, 345, 4, border='white', borderWidth=4, fill=None) 
f30 = Circle(120, 385, 4, border='white', borderWidth=4, fill=None)
f31 = Circle(280, 305, 4, border='white', borderWidth=4, fill=None)
f32 = Circle(280, 345, 4, border='white', borderWidth=4, fill=None)
f33 = Circle(280, 385, 4, border='cyan', borderWidth=4, fill=None)
f34 = Circle(90, 330, 4, border='white', borderWidth=4, fill=None)
f35 = Circle(55, 330, 4, border='white', borderWidth=4, fill=None)
f36 = Circle(30, 345, 4, border='cyan', borderWidth=4, fill=None)
f37 = Circle(30, 385, 4, border='white', borderWidth=4, fill=None)
f38 = Circle(310, 330, 4, border='white', borderWidth=4, fill=None)
f39 = Circle(345, 330, 4, border='white', borderWidth=4, fill=None)
f40 = Circle(370, 345, 4, border='white', borderWidth=4, fill=None)
f41 = Circle(370, 385, 4, border='white', borderWidth=4, fill=None)

## Placing food items in a list so i can iterate over them
foodItems = [
    (f1, 3), (f2, 1), (f3, 1), (f4, 1), (f5, 1), (f6, 3), (f7, 1), (f8, 1), (f9, 1), (f10, 1), (f11, 1), (f12, 1), (f13, 1), (f14, 1), 
    (f15, 1), (f16, 1), (f17, 1), (f18, 1), (f19, 3), (f20, 3), (f21, 1), (f22, 1), (f23, 1), (f24, 1), (f25, 1), (f26, 1), (f27, 1), (f28, 3), 
    (f29, 1), (f30, 1), (f31, 1), (f32, 1), (f33, 3), (f34, 1), (f35, 1), (f36, 3), (f37, 1), (f38, 1), (f39, 1), (f40, 1), (f41, 1)
    ]

cmu_graphics.run()