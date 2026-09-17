from cmu_graphics import *

## Connect 4!
Rect(0, 0, 400, 400, fill = None, border = 'navy', borderWidth = 3)
app.background = 'dodgerBlue'
Label('Connect 4!', 200, 35, fill = 'navy', font = 'montserrat', size = 42, bold = True, border = 'navy', borderWidth = 7)
Label('Connect 4!', 200, 35, fill = 'dodgerBlue', font = 'montserrat', size = 42, bold = True)

## Instructions
instructions = Group(
    Rect(0, 160, 400, 104, fill = 'white', opacity = 80), 
    Label('Tap above the column you wish to', 200, 180, font = 'montserrat', size = 20, bold = True), 
    Label('drop the chip in. First player to', 200, 210, font = 'montserrat', size = 20, bold = True), 
    Label('Connect four chips in a line wins!', 200, 240, font = 'montserrat', size = 20, bold = True)
    )
    
## Game Timing and Animation
app.stepsPerSecond = 35 # smoother animations
app.bounceCount = 0
app.dy = 8 # vertical velocity for fallinng chips

## Game State Control
app.turn = 'red' # will be updated based on random start
app.winDelay = 0
app.flashCol = None
app.flashTime = 0
app.prevChip = None
app.prevHovering = None
app.isGameOver = False

## Grid and Chip Tracking
app.gridData = [[None for _ in range(7)] for _ in range(6)] # sets up a 7x6 grid filled with nothing
app.cellSize = 52 # scaling variable
app.slots = [[None for _ in range(7)] for _ in range(6)] # slots will be stored here
app.placedChips = [] # chips locked into place
app.winningChips = [] # coordinates of a 4-in-a-row
app.highlightedSlot = [] # circles drawn around winning chips

## UI Components
app.stars = Group()
app.winLabel = [] # displayed when a player wins

## Actively Falling Chip
app.fallingChip = None 
app.fallingTargetY = None
app.fallingRow = None
app.fallingCol = None

## Player Info & Score
app.redScore = 0
app.yellowScore = 0
app.playerRed = '' # store name
app.playerYellow = '' # store name

## Randomly set you who goes first
def chooseTurn():
    randNum = randrange(1, 11)
    if randNum % 2 == 0: # if number is even then red goes first
        app.turn = 'red'
    else: # if number is not even, if it is odd, yellow goes first
        app.turn = 'yellow'

chooseTurn()

# Get Red player's name
while True:
    name = app.getTextInput("Enter Red Player's Name:")
    if name is not None and name.strip() != '':
        app.playerRed = name.strip()
        break
    elif name is None:
        app.playerRed = "Red Player"
        break # Defeault fallback if user cancels
    
# Get Yellow player's name
while True:
    name = app.getTextInput("Enter Yellow Player's Name:")
    if name is not None and name.strip() != '':
        app.playerYellow = name.strip()
        break
    elif name is None:
        app.playerYellow = "Yellow Player"
        break # Defeault fallback if user cancels

# Sound variables
bounceSound = Sound('cmu://911870/39539221/421372__jaszunio15__click_42.wav')
winSound = Sound('cmu://911870/39540553/666280__logatron__oldtada.wav')

## Creates the connect four grid
def drawConnectFourGrid():
    for row in range(6):
        for col in range(7):
            x = 44 + col * app.cellSize
            y = 90 + row * app.cellSize
            slot = Circle(x, y, 24, fill = 'white', border = 'navy', borderWidth = 4)
            app.slots[row][col] = slot
            
drawConnectFourGrid()
instructions.toFront() # place instructions at the front of the canvas

## Draws a chip on canvas
def drawChip(row, col, color):
    x = 44 + col * app.cellSize
    y = 60
    filling = 'red' if color == 'red' else 'yellow'
    outline = 'fireBrick' if color == 'red' else 'gold'
    chip = Group(
        Circle(x, y, 20, fill = filling, border = outline, borderWidth = 4), 
        Circle(x, y, 10, fill = outline, opacity = 30),
        Arc(x, y, 24, 24, 0, 35, fill = 'white', opacity = 10)
    )
    return chip
    
## Convert x positions to a column number
def getColumn(x):
    return int((x - 18) // app.cellSize) # divides by the scale to find the approximate x with respect to the column

## Function that contains logic for highlighting column for user experince
def highlightColumn(col):
# Reset previous column to default
    if app.prevHovering is not None and app.prevHovering >= 0 and app.prevHovering <= 6:
        for i in range(6):
            app.slots[i][app.prevHovering].fill = 'white'
            app.slots[i][app.prevHovering].opacity = 100
        
    # Highlight current column only if its in bounds
    if col >= 0 and col <= 6:
        for i in range(6):
            app.slots[i][col].fill = app.turn
            app.slots[i][col].opacity = 60 if app.turn == 'red' else 70
        
    # Update column
    app.prevHovering = col
    
## Function that contains logic for dropping a chip
def dropChip(col):
    if col < 0 or col > 6:
        return # if mouseX is out of range do nothing
    
    ## Drops chip until it hits a previous chip
    for row in reversed(range(6)):
        if app.gridData[row][col] == None:
            app.fallingRow = row
            app.fallingCol = col
            app.fallingTargetY = 90 + row * app.cellSize
            app.fallingChip = drawChip(row, col, app.turn)
            break
        
    else:
        # If there is no empty row found, column is full
        app.flashCol = col
        app.flashTime = 15
        
    # Clear the hovering
    app.prevHovering = None

## Track mouse movement over columns
def onMouseMove(mouseX, mouseY):
    if app.isGameOver == True:
        return # stops function body execution if game is over
    
    col = getColumn(mouseX)
    highlightColumn(col)
    
## Allows user to preview chips when dragging their mouse
def onMouseDrag(mouseX, mouseY):
    if app.isGameOver == True:
        return # stops function body execution if game is over
    
    col = getColumn(mouseX)
    highlightColumn(col)
    
    if 0 <= col <= 6: # bound col's range
        if app.prevChip:
            app.prevChip.centerX = 44 + col * app.cellSize
            app.prevChip.centerY = 60
            
        else:
            color = 'red' if app.turn == 'red' else 'yellow'
            outline = 'fireBrick' if app.turn == 'red' else 'gold'
            app.prevChip = Group(
                Circle(44 + col * app.cellSize, 60, 20, fill = color, border = outline, borderWidth = 4),
                Circle(44 + col * app.cellSize, 60, 10, fill = outline, opacity = 30),
                Arc(mouseX, mouseY, 24, 24, 0, 35, fill = 'white', opacity = 10)
                )
  
## Deletes the preview chip              
def onMouseRelease(mouseX, mouseY):
    if app.prevChip:
        app.prevChip.clear()
        app.prevChip = None

## Takes user press and drops chip into its place
def onMousePress(mouseX, mouseY):
    if app.isGameOver == True:
        return # stops function body execution if game is over
    
    # Remove instructions
    instructions.visible = False
    
    # Checking if chip is falling
    if app.fallingChip != None:
        return # don't drop another while one is falling
    
    # Only start falling if user taps above the grid
    if mouseY > 370:
        return
    
    # Gets col
    col = getColumn(mouseX)
    
    # Drops chip
    dropChip(col)

## Message when column is full
fullMessage = Group(
    Rect(0, 160, 400, 80, fill = 'white', opacity = 60), 
    Label('Full Column!', 200, 200, fill = 'orangeRed', font = 'montserrat', size = 26, bold = True, border = 'orangeRed', borderWidth = 4), 
    Label('Full Column!', 200, 200, fill = 'orange', font = 'montserrat', size = 26, bold = True)
    )
    
fullMessage.visible = False # hide message

def flashFullCol():
    # If column is full, and flash time is greater than 0
    if app.flashCol is not None and app.flashTime > 0:
        for i in range(6):
            app.slots[i][app.flashCol].border = 'orangeRed'
            app.slots[i][app.flashCol].opacity = 80
            fullMessage.toFront() # place at the top 
            fullMessage.visible = True # reveal message
        app.flashTime -= 1 # decrease time
    
    # Once time is up then reset values to default and remove message
    elif app.flashCol is not None:
        for i in range(6):
            app.slots[i][app.flashCol].border = 'navy'
            app.slots[i][app.flashCol].opacity = 100
            fullMessage.visible = False # hide message
        app.flashCol = None

## Checks for a winner; if someone connects 4 chips in a row, column or diagonal
def displayGameOutcome():
    boardFull = True # to check if there is space remaining 
    app.winningChips.clear() # clear previous winning chips
    
    for row in range(6):
        for col in range(7):
            player = app.gridData[row][col]
            if player is None:
                boardFull = False
                continue
            
            ## Identify a win and place winning chips into a list
            # Horizontal win condition
            if col <= 3 and all(app.gridData[row][col+i] == player for i in range(4)):
                app.winningChips = [(row, col+i) for i in range(4)]
                return True
            
            # Vertical win condition
            if row <= 2 and all(app.gridData[row+i][col] == player for i in range(4)):
                app.winningChips = [(row+i, col) for i in range(4)]
                return True
            
            # Diagonal down-right win condition
            if row <= 2 and col <= 3 and all(app.gridData[row+i][col+i] == player for i in range(4)):
                app.winningChips = [(row+i, col+i) for i in range(4)]
                return True
            
            # Diagonal up-right win condition
            if row >= 3 and col <= 3 and all(app.gridData[row-i][col+i] == player for i in range(4)):
                app.winningChips = [(row-i, col+i) for i in range(4)]
                return True
                
    # Check for a draw, if all slots are filled
    if boardFull:
        return 'draw'
        
    return False

##Draw stars in the background
def drawStars():
    for row in range(13):
        for col in range(13):
            cx = 20 + row*35 - randrange(-10, 11)
            cy = 20 + col*35 - randrange(-10, 11)
            star = Star(cx, cy, 8, 5, fill = 'white', opacity = 20)
            app.stars.add(star)

def drawWinOrDrawLabel():
    # Get output from win or draw checking function
    result = displayGameOutcome()
                
    # If its a win, draw the winner's label
    if result == True:
        winSound.play() # play win sound
        app.isGameOver = True # game is over
        cover = Rect(0, 160, 400, 80, fill = 'white', opacity = 60)
        app.winLabel.append(cover)
            
        # Assign points to winner
        if app.turn == 'red':
            app.redScore += 1
        else:
            app.yellowScore += 1
                    
        # Highlight winning column
        for (row, col) in app.winningChips:
            slot = app.slots[row][col]
            highlightedSlot = Circle(slot.centerX, slot.centerY, 24, fill = None, border = 'white', borderWidth = 4)
            app.highlightedSlot.append(highlightedSlot)
                    
        # If red, draw red wins, otherwise draw yellow wins
        if app.turn == 'red':
            redWinLabel = Group(
                Label(app.playerRed + ' Wins! Score: ' + str(app.redScore), 200, 185, fill = 'crimson', font = 'montserrat', size = 26, bold = True, border = 'crimson', borderWidth = 4), 
                Label(app.playerRed + ' Wins! Score: ' + str(app.redScore), 200, 185, fill = 'red', font = 'montserrat', size = 26, bold = True),
                Label("press 'r' to restart", 200, 210, fill = 'crimson', font = 'montserrat', size = 26, bold = True, border = 'crimson', borderWidth = 4),
                Label("press 'r' to restart", 200, 210, fill = 'red', font = 'montserrat', size = 26, bold = True)
                )
            app.winLabel.append(redWinLabel)
        else:
            yellowWinLabel = Group(
                Label(app.playerYellow + ' Wins! Score: ' + str(app.yellowScore), 200, 185, fill = 'gold', font = 'montserrat', size = 26, bold = True, border = 'gold', borderWidth = 4), 
                Label(app.playerYellow + ' Wins! Score: ' + str(app.yellowScore), 200, 185, fill = 'yellow', font = 'montserrat', size = 26, bold = True),
                Label("press 'r' to restart", 200, 210, fill = 'gold', font = 'montserrat', size = 26, bold = True, border = 'gold', borderWidth = 4),
                Label("press 'r' to restart", 200, 210, fill = 'yellow', font = 'montserrat', size = 26, bold = True)
                )
            app.winLabel.append(yellowWinLabel)
                
    # If its a draw, draw a label
    if result == 'draw':
        app.isGameOver = True
        app.isGameOver = True # game is over
        Rect(0, 160, 400, 80, fill = 'white', opacity = 70)
        Label('DRAW', 200, 200, fill = 'navy', font = 'montserrat', size = 26, bold = True, border = 'navy', borderWidth = 4)
        Label('DRAW', 200, 200, fill = 'dodgerBlue', font = 'montserrat', size = 26, bold = True)

def restartGame():
    # Only check for restart if the game is won and there are no falling chips
    if displayGameOutcome() and not app.fallingChip:
        # Clear grid
        app.gridData = [[None for _ in range(7)] for _ in range(6)]
        
        # Reset each slot's visual
        for row in range(6):
            for col in range(7):
                slot = app.slots[row][col]
                slot.fill = 'white'
                slot.border = 'navy'
                slot.opacity = 100
        
        # Clear highlighted chips
        for circle in app.highlightedSlot:
            circle.visible = False
        app.highlightedSlot.clear()
        
        # Clear winning labels
        for label in app.winLabel:
            label.visible = False
        app.winLabel.clear()
        
        # Toggle background after each round
        if app.background == 'dodgerBlue':
            app.background = gradient('dodgerBlue', 'midnightBlue')
            # Draw stars to create a galaxy themed board
            drawStars()
        # Clear stars if background is dodger blue
        else:
            app.background = 'dodgerBlue'
            for star in app.stars:
                star.visible = False
            app.stars.clear()
        
        # Remove any chips
        for chip in app.placedChips[:]:
            chip.clear()
        app.placedChips.clear()
        
        # Randomly choose truns again
        chooseTurn()
                    
        # Reset all the other variables to default values
        app.prevHovering = None
        app.winningChips.clear()
        app.winDelay = 0
        app.fallingChip = None
        app.fallingTargetY = None
        app.fallingRow = None
        app.fallingCol = None
        app.bounceCount = 0
        app.dy = 8
        app.flashCol = None
        app.flashTime = 0
        instructions.visible = True
        fullMessage.visible = False
        app.isGameOver = False # game continues

def onKeyPress(keys):
    # When 'r' is pressed, restart game
    if 'r' in keys:
        restartGame()

def onStep():
    # If column is full, warn the user
    flashFullCol()
    
    # Chip falls with gravity
    if app.fallingChip:
        app.fallingChip.centerY += app.dy
        app.dy += 0.5 # gravity effect
            
        if app.fallingChip.bottom >= app.fallingTargetY + 24: # if chip touches the bottom of its target Y
            app.fallingChip.bottom = app.fallingTargetY + 24
            bounceSound.play() # play bounce sound
            app.dy *= -0.4 # bounce up
            app.bounceCount += 1
            
            # If chip has bounced 5 or more times or bounce height is short, then lock chip
            if app.bounceCount >= 5 or abs(app.dy) < 1:
                app.fallingChip.centerY = app.fallingTargetY
                app.gridData[app.fallingRow][app.fallingCol] = app.turn # Locks chip in the grid
                app.placedChips.append(app.fallingChip) # adds falling chips into the list of placed chips
                
                # Draw the win or draw label
                drawWinOrDrawLabel()
                        
                # Switch turn
                app.turn = 'yellow' if app.turn == 'red' else 'red'
                        
                # Remove falling chip
                app.fallingChip = None
                        
                # Resetting vertical speed to 8 and bounce tracker to 0
                app.dy = 8
                app.bounceCount = 0

cmu_graphics.run()