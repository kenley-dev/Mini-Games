from cmu_graphics import *

app.background = 'black'
## Creating the road
Rect(0, 40, 400, 300)
Line(0, 289, 400, 289, dashes=(20, 15), fill = 'gold')
Line(0, 240, 400, 240, dashes=(20, 15), fill = 'gold')
Line(0, 189, 400, 189, dashes=(20, 15), fill = 'gold')
Line(0, 137, 400, 137, dashes=(20, 15), fill = 'gold')
Line(0, 88, 400, 88, dashes=(20, 15), fill = 'gold')
Line(0, 340, 400, 340, dashes=(20, 15), fill = 'gold')

## Finish Line
finishLine = Group(Rect(0, 0, 400, 40, fill='white'),
Rect(0, 0, 20, 20), Rect(20, 20, 20, 20), Rect(40, 0, 20, 20), Rect(60, 20, 20, 20),
Rect(80, 0, 20, 20), Rect(100, 20, 20, 20), Rect(120, 0, 20, 20), Rect(140, 20, 20, 20),
Rect(160, 0, 20, 20), Rect(180, 20, 20, 20), Rect(200, 0, 20, 20), Rect(220, 20, 20, 20),
Rect(240, 0, 20, 20), Rect(260, 20, 20, 20), Rect(280, 0, 20, 20), Rect(300, 20, 20, 20), 
Rect(320, 0, 20, 20), Rect(340, 20, 20, 20), Rect(360, 0, 20, 20), Rect(380, 20, 20, 20))

##Instrcutions
Label('hold enter and press', 330, 357, size=11, font='orbitron',fill = 'white', bold = True)
Label('a, s, d, or w, to move', 330, 370, size=11, font='orbitron',fill = 'white', bold = True)
Label('Get to the finish line!', 330, 384, size=11, font='orbitron',fill = 'white', bold = True)

## Creating a function that draws cars
def drawCar(centerX, centerY, colour1, colour2, angle, speed = 1):
    car1 = Group(Polygon(0, 1, 3, 0, 12, 0, 15, 1, 30, 1, 33, 0, 45, 0, 48, 10,
    48, 20, 45, 30, 33, 30, 30, 29, 15, 29, 12, 30, 0, 29,
    fill=gradient('royalBlue', 'mediumBlue'), rotateAngle = angle),
    Rect(5, 5, 5, 20, rotateAngle = angle, border='black', borderWidth=20),
    Polygon(40, 5, 42, 15, 40, 25, 30, 24, 30, 6, border='black', borderWidth=20),
    Polygon(10, 5, 30, 6, 30, 24, 10, 25, fill=None, border='black', 
    borderWidth = 2))
    
    ## creating custom properties
    car1.centerX += centerX 
    car1.centerY += centerY
    car1.speed = speed
    car1.fill = gradient(colour1, colour2)
    return car1 ## ensure cars are not of type None

## Npc Cars
npcCar1 = drawCar(22, 300, 'yellow', 'red', 0)
npcCar2 = drawCar(310, 250, 'yellow', 'red', 180)
npcCar3 = drawCar(22, 200, 'yellow', 'red', 180)
npcCar4 = drawCar(310, 150, 'yellow', 'red', 180)
npcCar5 = drawCar(22, 100, 'yellow', 'red', 180)
npcCar6 = drawCar(310, 50, 'yellow', 'red', 180)

## Player's Car
playerCar = Group(
    Polygon(0, 21, 3, 20, 12, 20, 15, 21, 30, 21, 33, 20, 45, 20, 48, 30,
                48, 40, 45, 50, 33, 50, 30, 49, 15, 49, 12, 50, 0, 49,
                fill=gradient('royalBlue', 'mediumBlue'), rotateAngle = -90),
    Rect(20, 40, 5, 20, rotateAngle = - 90),
    Polygon(28, 12, 30, 22, 28, 32, 18, 31, 18, 13, rotateAngle = -90),
    Polygon(33, 48, 13, 48, 15, 27, 32, 27, fill=None, border='black', 
    borderWidth = 2)
    )

playerCar.speed = 5 ## Set defalut speed of players car to 1

## Level
Label('Level:', 35, 370, size=14, font='orbitron',fill = 'white', bold = True)
level = Label(1, 68, 371, size=12, font='orbitron', fill = 'white', bold = True)

## Scoring display
difficulty = Label('Easy', 40, 386, size=14, font='orbitron',fill = 'white', bold = True)

## HP
Label('HP:', 35, 355, size=14, font='orbitron',fill = 'white', bold = True)
hp = Label(5, 55, 355, size=12, font='orbitron',fill = 'white', bold = True)

## Player car Starting position
playerCar.centerX = 200
playerCar.centerY = 370

def onStep():
    ## Making the npc cars move continously according to the value of my custom speed property
    npcCar1.centerX += npcCar1.speed + 1
    npcCar2.centerX -= npcCar1.speed
    npcCar3.centerX += npcCar1.speed + 3
    npcCar4.centerX -= npcCar1.speed + 1
    npcCar5.centerX += npcCar1.speed +2
    npcCar6.centerX -= npcCar1.speed + 3
    
    ##Horizontal Wrap-around feature for npc cars
    if npcCar1.centerX >= 400:
        npcCar1.centerX = 1
    if npcCar3.centerX >= 400:
        npcCar3.centerX = 1
    if npcCar5.centerX >= 400:
        npcCar5.centerX = 1
    if npcCar2.centerX <= 0:
        npcCar2.centerX = 399
    if npcCar4.centerX <= 0:
        npcCar4.centerX = 399
    if npcCar6.centerX <= 0:
        npcCar6.centerX = 399
    
    ## Making a list to check if the player hits an npc car, deduct 1 hp, and reset cars position
    npcCars = [npcCar1, npcCar2, npcCar3, npcCar4, npcCar5, npcCar6]
    for npcCar in npcCars:
        if playerCar.hitsShape(npcCar):
            hp.value -= 1
            playerCar.centerY = 370
            playerCar.centerX = 200
            break

    ##Game over if player has no more hp
    if hp.value == 0:
        Label('GAME OVER', 200, 215, size=50, font='orbitron',fill = 'white', bold = True)
        app.stop()
    app.stepsPerSecond = 25

def onKeyHold(keys):
    ## Making player's car move, and increaisng the score by 1 each time the player moves
    if 'enter' in keys and 'w' in keys:
        playerCar.centerY -= playerCar.speed
        playerCar.rotateAngle = 0
    elif 'enter' in keys and 's' in keys:
        playerCar.centerY += playerCar.speed
        playerCar.rotateAngle = 180
    elif 'enter' in keys and 'd' in keys:
        playerCar.rotateAngle = 90
        playerCar.centerX += playerCar.speed
    elif 'enter' in keys and 'a' in keys:
        playerCar.rotateAngle = -90
        playerCar.centerX -= playerCar.speed
        
    ##Car cannot move out of canvas vertically
    if 'w' in keys or 's' in keys:
        if playerCar.centerY >= 375:
            playerCar.centerY = 375
        
    ##Horizontal Wrap-around feature for player car
    if 'a' in keys or 'd' in keys:
        if playerCar.centerX >= 400:
            playerCar.centerX = 1
        if playerCar.centerX <= 0:
            playerCar.centerX = 399

    ## Increasing levels by 1, points by 5, and the speed of the enemy cars each time the player's car hits the finish line
    if playerCar.hitsShape(finishLine):
        npcCar1.speed += 1
        level.value += 1
        if npcCar1.speed > 4:
            difficulty.value = 'Medium'      #Nested them to avoid multiple checks
            playerCar.speed += 1
            if npcCar1.speed > 8:
                difficulty.value = 'Hard'
                playerCar.speed += 1
                if npcCar1.speed > 12:
                    difficulty.value = 'Extreme'
                    playerCar.speed += 2
                    if npcCar1.speed > 16:
                        difficulty.value = 'Impossible'
                        playerCar.speed += 3

        ## Send players car to the start
        playerCar.centerY = 370

cmu_graphics.run()