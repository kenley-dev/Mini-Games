from cmu_graphics import *

## WORDLE
app.background = 'black'
app.winningLetters = []
app.gameOver = False

## Instructions
instructions = Group(
    Rect(0, 100, 400, 235, fill = 'white'),
    Label('Try to guess the correct 6-letter',  200, 130, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('word. If it is the correct letter',  200, 155, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('and in the right place, the letter',  200, 180, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('turns green. If it is the correct',  200, 205, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('letter, but in the wrong place the',  200, 230, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('letter turns yellow. And if it is the',  200, 255, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('wrong letter, the letter turns grey.',  200, 280, fill = 'black', font = 'montserrat', size = 20, bold = True),
    Label('Tap Spacebar to start!!',  200, 305, fill = 'black', font = 'montserrat', size = 20, bold = True),
    )
instructions.centerY = 200 # Center the instructions

## Background for when text is dispalyed
cover1 = Rect(0, 167, 400, 66, fill = 'white')
cover2 = Rect(0, 167, 400, 66, fill = 'white', opacity = 80)
cover1.visible = False
cover2.visible = False

## Create a word bank, and select the right word randomly
wordBank = ['WORDLE', 'CANADA', 'KENLEY', 'NUMBER', 'PRAYER', 'NATHAN', 'OCEANS', 'NARUTO', 'HINATA', 'JIGSAW', 'FICKLE', 'VORTEX',
'RIPPLE', 'MELLOW', 'WRENCH', 'FROSTY', 'MANTIS', 'BUMPER', 'SUMMIT', 'DAGGER', 'LEBRON', 'QUIVER', 'SIZZLE', 'GOBLIN', 'JOCKEY', 'NIMBUS',
'TIMBER', 'ALBEDO', 'QUENCH', 'PUZZLE', 'OYSTER', 'TANGLE', 'FROKIE', 'WORKER', 'NARROW', 'DURANT', 'GIDDEY', 'PDIDDY', 'REIGER', 'MORRIS',
'HARRIS', 'DANIEL', 'PICKLE', 'SOCCER', 'FRUGAL', 'INFLUX', 'LAKERS', 'TARIFF', 'QUIRKY', 'PEBBLE', 'PIMPLE', 'NECTAR', 'OUTLAW', 'HICCUP',
'YAPPER', 'HUZZES', 'ZANJAY', 'GOONER', 'TAPERS', 'KNICKS', 'PENCIL', 'UPDATE', 'GOOGLE', 'PEANUT', 'KESLEY', 'MOTHER', 'FATHER']

app.rightWord = choice(wordBank) # choice a random word as the correct word

## Set to track the number of guesses
app.numGuess = 0

## Creating groups for each row and collum to properly sort each word in blocks
rows = [[] for _ in range(6)]
cols = [[] for _ in range(6)]

## Track the row in which the user is in
app.guessRow = 0

blocks = []
## Using nested for loops to create the wordle grid
for centerX in range(35, 366, 66):
    for centerY in range(35, 366, 66):
        block = Rect(0, 0, 60, 60, fill = 'gainsboro', border = 'grey', opacity = 15)
        block.centerX = centerX
        block.centerY = centerY
        blocks.append(block)

## Using this for loop to create words within blocks
for colIndex, centerX in enumerate(range(35, 366, 66)):
    for rowIndex, centerY in enumerate(range(35, 366, 66)):
        letter = Label('', centerX, centerY, fill = 'white', font = 'montserrat', size = 40, bold = True, border = 'black')
        
        ## Adding letters to corresponding row and colum lists
        rows[rowIndex].append(letter)
        cols[colIndex].append(letter)
    
    ## Potential bug
    if rows[app.guessRow][colIndex].hits(block.centerX, block.centerY):
        print('collision detected')

# Define a hitTest function that can apply to labels
def hitTest(self, x, y):
    return self.hits(x, y)

# Attch it to the label class
Label.hitTest = hitTest
    

## Increases size of letters
def onMousePress(x, y):
    for row in rows:
        for label in row:
            if label.hitTest(x, y):
                label.size += 2

## Animation for a win
def winAnimation(rowIndex):
    app.winningLetters.clear() # clear any previous letters
    for letter in rows[rowIndex]: # only the row that was just guessed
        letter.growAmount = 0.5
        app.winningLetters.append(letter)
    
    
## Function that checks if the users input is the correct word.
def checkGuess():
    ## Create a list of booleans ofr checking matched letters
    matched = [False] * 6 # Mark if letter is matched
    wordsLeft = list(app.rightWord) # List to track lingering letters
    removedWord = wordBank.pop(randrange(0, len(wordBank))) # eliminate a random word to aid user
    print('Hint: ' + str(removedWord) + ' is not the word')
    
    for colIndex in range(6):
        guessedLetter = rows[app.guessRow][colIndex].value
        
        ## If the letters guessed are the correct letters all in the right place with respect to the app.rightWord, 
        ## letters will be turned green
        if guessedLetter == app.rightWord[colIndex]:
            rows[app.guessRow][colIndex].fill = 'green' # Green check
            matched[colIndex] = True # Marked as matched
            wordsLeft[colIndex] = None # Marks this letter as used
        
        ## If the letters guessed are the correct letters all the wrong place with respect to the app.rightWord, 
        ## letters will be truned gold
        elif guessedLetter in wordsLeft: # If there are still some letters left, check gold
            rows[app.guessRow][colIndex].fill = 'gold'
            wordsLeft[wordsLeft.index(guessedLetter)] = None # Marks this letter as used
        
        ## If the letters guessed are the wrong letters with respect to the app.rightWord, letters will be truned grey
        else: # If no letters match the right ones check for grey
            rows[app.guessRow][colIndex].fill = rgb(70, 70, 70)
           
## Reveals covers 
def revealCover():
    cover1.visible = True
    cover2.visible = True
    cover2.toFront() # Places at the front of the screen

## Storing user inputs and ensuring they are uppercase
def onKeyPress(key):
    if app.gameOver:
        return
    if key == 'space':
        ## Removes instructions when spacebar is pressed
        instructions.visible = False
        ## Keeps asking user for another guessed word if their guess is invalid
        while True:
            guessedLetters = app.getTextInput('Guess another word:')
                
            ## Ensures user inputs are not empty, if they aren't, it prompts the user to guess another word
            if guessedLetters:
                guessedLetters = guessedLetters.upper()
                ## Ensures user inputs are 6 indexes long and are letters, if they are not, it prompts the user to guess another word
                if len(guessedLetters) == 6 and guessedLetters.isalpha() == True:
                    ## Save guessed letters on the wordle blocks
                    for colIndex in range(6):
                        rows[app.guessRow][colIndex].value = guessedLetters[colIndex]
                        
                    ## If guess is valid, check the guess, update number of guesses by 1
                    checkGuess()
                    app.numGuess += 1
                    
                    ## If the guessed letter is the same as the right word, then stop the game, and show how many guesses it took
                    if guessedLetters == app.rightWord:
                        winningRow = app.guessRow # Save current row
                        winAnimation(winningRow) # Play win animation
                        revealCover()
                        response1 = Label('You win! You only used ' + str(app.numGuess) + ' guess!', 200, 200, fill = 'black', font = 'montserrat', size = 21, bold = True)
                        response1.toFront() # Places at the front of the screen
                        app.gameOver = True
                        
                        ## Remove the word 'only' as guessing the word after 5 trys is not that impressive
                        if app.numGuess >= 5:
                            response1.toBack()
                            response3 = Label('You win! You used ' + str(app.numGuess) + ' guess!', 200, 200, fill = 'black', font = 'montserrat', size = 21, bold = True)
                            response3.toFront()
                        
                    ## If all 6 guesses are made, stop the game, and reveal the word
                    elif app.numGuess == 6:
                        revealCover()
                        response2 = Label('You lose! The word was: ' + app.rightWord,  200, 200, fill = 'black', font = 'montserrat', size = 21, bold = True)
                        response2.toFront() # Places at the front of the screen
                        app.gameOver = True
                        
                    # Keeps guessRow in bounds
                    if app.guessRow < 5:
                        app.guessRow += 1
                    ## Esnures that this loop ends once the user wins or loses
                    return None
                    
                else:
                    print("Invalid input, insert a 6-lettered word")
            else:
                print('Invalid input, input cannot be empty')

## Animate the winning letters             
def onStep():
    for letter in app.winningLetters:
        letter.size += letter.growAmount
        if letter.size >= 50: # Upper limit for size
            letter.growAmount  = -0.5 # shrinks letters
        elif letter.size <= 40: # Original size
            letter.growAmount = 0.5 # grows letters

cmu_graphics.run()