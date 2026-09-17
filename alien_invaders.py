from cmu_graphics import *

import random
app.background = gradient(rgb(0, 0, 100), rgb(0, 0, 50), 'black')

## Lowering the frames for a smooth feel
app.stepsPerSecond = 65

instructions1 = Label('Press Spacebar to', 200, 195, size=30, font='orbitron',fill = 'white', bold = True)
instructions2 = Label('Shoot the Alien Ships!', 200, 230, size=30, font='orbitron',fill = 'white', bold = True)
score = Label(0, 240, 240, size=20, font='orbitron',fill = 'white', bold = True, visible = False)
scoreLabel = Label('Score: ', 180, 240, size=20, font='orbitron',fill = 'white', bold = True, visible = False)
wavePoint = Label(0, 285, 200, size=55, font='orbitron',fill = 'white', bold = True, visible = False)
waves = Label('WAVE', 160, 200, size=50, font='orbitron',fill = 'white', bold = True, visible = False)

print('Complete Wave 5 to Win!')
print('First Wave it at 5 points')

## Stars
stars = Group(Star(19, 25, 7, 5, fill='white'),
    Star(33, 114, 7, 5, fill='white'),
    Star(303, 115, 6, 5, fill='white'),
    Star(372, 41, 7, 5, fill='white'),
    Star(376, 185, 6, 5, fill='white'),
    Star(357, 280, 7, 5, fill='white'),
    Star(252, 380, 8, 5, fill='white'),
    Star(159, 368, 5, 5, fill='white'),
    Star(368, 372, 6, 5, fill='white'),
    Star(69, 383, 6, 5, fill='white'),
    Star(14, 334, 5, 5, fill='white'),
    Star(46, 272, 7, 5, fill='white'),
    Star(17, 205, 9, 5, fill='white'),
    Star(77, 139, 5, 5, fill='white'),
    Star(64, 38, 5, 5, fill='white'),
    Star(358, 94, 7, 5, fill='white'),
    Star(278, 27, 6, 5, fill='white'),
    Star(128, 30, 8, 5, fill='white'),
    Star(98, 210, 8, 5, fill='white'),
    Star(146, 100, 6, 5, fill='white'),
    Star(210, 66, 8, 5, fill='white'),
    Star(244, 145, 5, 5, fill='white'),
    Star(118, 311, 7, 5, fill='white'),
    Star(291, 310, 6, 5, fill='white'),
    Star(208, 287, 8, 5, fill='white'),
    Star(170, 173, 6, 5, fill='white'),
    Star(287, 229, 8, 5, fill='white'))

## A groups for the alien ships
alienShips = Group()

## Function that draws alien ships
def spawnAlienShips(centerX, centerY):
    alienShip = Group(
        Oval(30, 30, 60, 40, fill=gradient('crimson', 'white', start='left'), border='white', borderWidth=5),
        Oval(50, 30, 5, 20), Line(25, 20, 50, 25, fill='dimGrey'), Line(25, 40, 50, 35, fill='dimGrey'),
        Oval(30, 30, 20, 30, fill='dimGrey'), 
        Circle(30, 30, 10)
        )
    
    ## Setting the alien ships' defualt values
    alienShip.rotateAngle = 90
    alienShip.height = 25
    alienShip.width = 25
    alienShip.centerX = centerX 
    alienShip.centerY = centerY - 60
    
    ## Adding each alien ship to the groups of alien ships
    alienShips.add(alienShip)

## Setting the alien's ships default change in vertical plan value to 1.2
alienShips.dy = 1.2

## Spawn alien, must hit this alien to start the game
spawnAlienShips(200, 200)

## A group for the player's ship
playerShip = Group(Oval(370, 370, 60, 40, fill=gradient('cornflowerBlue', 'white', start='left'),
    border='white', borderWidth=5),
    Oval(350, 370, 5, 20), 
    Line(375, 380, 350, 375, fill='dimGrey'),
    Line(375, 360, 350, 365, fill='dimGrey'),
    Oval(370, 370, 20, 30, fill='dimGrey'),
    Circle(370, 370, 10)
    )

## Defualt positions
playerShip.rotateAngle = 90
playerShip.width = 40
playerShip.height = 40
playerShip.centerX = 200

## Defining the change in the horizontal and vertical direction value for the player's ship
playerShip.dx = 4
playerShip.dy = 4

## A function that release's projectiles
def releaseProjectile(x1, y1, x2, y2):
    projectile = Line(x1, y1, x2, y2, fill = 'white', lineWidth = 6)
    allProjectiles.add(projectile)

## Checking for collsions of projectiles and alien ships
def checkCollision():
    for projectile in allProjectiles.children:
        if projectile.hitsShape(alienShips):
            allProjectiles.remove(projectile)
            for alienShip in alienShips.children:
                if projectile.hitsShape(alienShip):
                    alienShips.remove(alienShip)
            break
        
## Cretaing a group that all projectiles can be put into, so that they are shapes
allProjectiles = Group()

## Defining the projectile's set chnage in the vertical direction value as 7
allProjectiles.dy = 7

def onKeyHold(keys):
    ## Coding the diagona; movements for the player's ship
    if 's' in keys and 'a' in keys:
        playerShip.centerY += -playerShip.dy + 2
        playerShip.centerX += -playerShip.dx + 7
        
    if 's' in keys and 'd' in keys:
        playerShip.centerY += -playerShip.dy + 2
        playerShip.centerX += playerShip.dx - 7
    
    ## Coding the horizontal and vertical motion of teh player's ship
    if 'w' in keys:
        playerShip.centerY += -playerShip.dy
        
        ## Limit player movement to half the screen
        if playerShip.centerY <= 200:
            playerShip.centerY = 200

    if 's' in keys:
        playerShip.centerY += playerShip.dy
        
        ## Limit player movement so they can't move out of the screen vertically
        if playerShip.centerY >= 370:
            playerShip.centerY = 370

    if 'a' in keys:
        playerShip.centerX += -playerShip.dx
        
        ## Wraparound 
        if playerShip.right <= 0:
            playerShip.left = 400

    if 'd' in keys:
        playerShip.centerX += playerShip.dx
        
        ## Wraparound 
        if playerShip.left >= 400:
            playerShip.right = 0
            
def onKeyPress(key):
    ## When the splace bar is pressed a projectile is shot out
    if key == 'space':
        releaseProjectile(playerShip.centerX, playerShip.centerY - 40, playerShip.centerX, playerShip.centerY - 30)

def onStep():
    ## Moving projectile vertically
    allProjectiles.centerY += -allProjectiles.dy
    
    ## Alien Ship movement
    alienShips.centerY += alienShips.dy
    
    ## Remove projectiles that are off-screen
    for projectile in allProjectiles.children[:]:
        if projectile.top < -10:
            allProjectiles.remove(projectile)
    
    ## End game if alien ship gets past the player's ship
    if alienShips.bottom >= 430:
        Label('GAMEOVER!', 200, 200, size=50, font='orbitron',fill = 'white', bold = True)
        waves.visible = False
        wavePoint.visible = False
        alienShips.clear()
        allProjectiles.clear()
        stars.opacity = 60
        app.stop()
    
    ## If projectiles hit the alien ship they disappear and the level, and score, both increase
    if allProjectiles.hitsShape(alienShips):
        checkCollision()
        instructions1.visible = False
        instructions2.visible = False
        scoreLabel.visible = True
        score.visible = True
        score.value += 1
        waves.visible = True
        wavePoint.visible = True
        
        ## Spawning alien ships at random locations
        if score.value % 2 == 1: ## Check if points are an odd value
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
        if score.value % 2 == 0: ## Check if points are an even value
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
        
        ## The start of each wave will begin by clearing the alien ships spawning more
        ## alien ships, increasing the wavePoint, and increasing the the speed of alien ships
        
        ## WAVE 1
        if score.value == 5:
            alienShips.clear()
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
            wavePoint.value += 1 
            print('Next Wave is at 20 points')

        ## WAVE 2
        if score.value == 20:
            alienShips.clear()
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
            wavePoint.value += 1
            alienShips.dy = 1.3
            print('Next Wave is at 40 points')

        ## WAVE 3
        if score.value == 40:
            alienShips.clear()
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
            wavePoint.value += 1
            alienShips.dy = 1.4
            print('Next Wave is at 65 points')

        ## WAVE 4
        if score.value == 65:
            alienShips.clear()
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
            wavePoint.value += 1
            alienShips.dy = 1.6
            print('Next Wave is at 100 points')

        ## WAVE 5 (Final Wave)
        if score.value == 100:
            alienShips.clear()
            spawnAlienShips(random.randint(20, 380), 20 + random.randint(0, 10))
            wavePoint.value += 1
            alienShips.dy = 1.8
            print('Final Wave is at 150 points')

        ## You Win
        if score.value == 150:
            alienShips.clear()
            allProjectiles.clear()
            wavePoint.value += 1
            waves.visible = False
            wavePoint.visible = False
            Star(200, 200, 150, 11, fill=gradient('midnightBlue', 'black'), border='white', borderWidth = 3)
            Label('YOU', 195, 180, size=45, font='orbitron', bold = True, fill = 'white')
            Label('WIN!', 200, 230, size=45, font='orbitron', bold = True, fill = 'white')
            playerShip.centerY = 370
            playerShip.toFront()
            stars.toBack()
            stars.opacity = 60
            app.stop()

cmu_graphics.run()