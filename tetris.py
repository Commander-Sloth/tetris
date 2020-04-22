# Tetris Game recreation
# Started on 3/4/2020
import pygame
import sys
import random

gameArray = []
ROWS = 9
COLS = 9
gameOver = False
WIN_W = 500
WIN_H = 1000

# Global variable to address the last generated shape type.

gameScreen = pygame.display.set_mode((WIN_W, WIN_H))

backgroundCol = (0, 0, 0)

clock = pygame.time.Clock()

pygame.display.set_caption("Tetris")

pygame.init()

# Set up the 2D array according to the desired rows and columns.
for i in range(ROWS):
	localCol = []
	for j in range(COLS):
		localCol.append(0)
	gameArray.append(localCol)

gameArray = [
[0,0,0,0,0,0,0,0,0],
[0,2,0,0,0,0,0,0,0],
[0,2,0,0,0,0,0,0,0],
[0,2,0,0,0,0,0,0,0],
[0,2,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,2,0,0,2,0,0,0,0],
[0,0,0,2,2,0,0,0,0],
]

def print_2DArray(array):
	for row in range(ROWS):
		print(array[row])


def drawText(labelText, xPos, yPos):
	fontColor = (255, 255, 255)
	font = pygame.font.Font("freesansbold.ttf", 25)
	text = font.render(labelText, True, fontColor)
	textRect = text.get_rect()
	textRect.center = (xPos, yPos)
	return gameScreen.blit(text, textRect)


def validatePosition(rowPos, colPos):
	if rowPos < 0 or rowPos > ROWS-1 or colPos > COLS-1 or colPos < 0 or gameArray[rowPos][colPos] == 2:
		return False

	elif rowPos >= 0 or rowPos <= ROWS-1 or colPos <= COLS-1 or colPos >= 0: # and gameArray[rowPos][colPos] != 2: 
		return True

def posInArray(rowPos, colPos):
	if rowPos >= 0 and rowPos <= ROWS-1 and colPos <= COLS-1 and colPos >= 0:
		return True
	else:
		
		return False
		
def valueThere(rowPos, colPos):
	if rowPos <= 0:
		return False
	if posInArray(rowPos, colPos):
		if gameArray[rowPos][colPos] != 0 and gameArray[rowPos][colPos] != 1:
			return True

	return False

def valInPos(rowPos, colPos):
	global gameArray
	if posInArray(rowPos, colPos) and gameArray[rowPos][colPos] != 0:
		print('BAD val'+ str(gameArray[rowPos][colPos]) )
		return True

	return False


def checkARow(moveDownArray):
	global gameArray
	# HERE MANUALLY GO THROUGH EACH ROW, becuase IF A ZERO IS IN THE BOTTOM, NONE WILL EVER GET FIXED

	maybeGo = False
	# Go through this row, and see if it is all zero. (Make sure it tests from the bottom up, otherwise it will always detect the blank first line)
	for thisRow in range(ROWS-1,-1,-1):
		for column in range(COLS):
			if gameArray[thisRow][column] == 0:
				maybeGood = True
				return

	print("Found a row to Erase")

	# Move the shape down 1 more before rearranging the array.
	for obj in moveDownArray:
		#shapeMovement(shapeList, "Down") 
		obj.blockDown()

	# If there were no zeros in this row
	gameArray.pop(thisRow)

	columnToAdd = []
	for column in range(COLS+1):
		columnToAdd.append(0)

	gameArray.insert(0, columnToAdd)


def intoArray(array, row, col, val):
	if row > -1 and row < ROWS and col > -1 and col < COLS:
		array[row][col] = val


# Return False if the position below is 2 or the edge
def testUnder(array, row, col):
	global gameArray

	if row >= 0:
		if row < ROWS-1 and gameArray[row+2][col] == 2:
			#print("A 2")
			return False

		if row == ROWS-1:
			#print("Hit bottom")
			return False

	
	#print('Nothing under')
	return True


# Return False if the position right is 2 or the edge
def testRight(array, row, col):
	if col == COLS - 1:
		#print("Hit Edge")
		return False

	elif col < COLS - 1 and array[row][col+1] == 2: 

		#print("Right : 2 at Col: " + str(col))
		return False

	else: return True


# Return False if the position right is 2 or the edge
def testLeft(array, row, col):
	if col == 0:
		#print("Hit Edge")
		return False

	elif col > 0 and array[row][col-1] == 2: 

		#print("Left: 2 at Col: " + str(col))
		return False

	return True


class block():
	def __init__(self, startX, startY):
		self.yPos = startY
		self.xPos = startX

	def draw(self, x, y):
		global gameArray
		if posInArray(y, x) == True:
			gameArray[y][x] = 1

			self.xPos ,self.yPos = x, y

	def erase(self):
		global gameArray
		if posInArray(self.yPos, self.xPos):
			gameArray[self.yPos][self.xPos] = 0

	def freeze(self):
		global gameArray
		if posInArray(self.yPos, self.xPos):
			gameArray[self.yPos][self.xPos] = 2
		

class Shape():
	def __init__(self, coordinateList): # [x,y]
		self.cent_yPos = coordinateList[0][1]
		self.cent_xPos = coordinateList[0][0]
		
		self.blockList = []
		for i in range(len(coordinateList)):
			self.blockList.append(block(coordinateList[i][0],coordinateList[i][1]))

	def clearBlocks(self):
		global gameArray
		for i in range(len(self.blockList)):
			self.blockList[i].erase()

	def stopBlocks(self):
		global gameArray
		for i in range(len(self.blockList)):
			self.blockList[i].freeze()
		spawnNewShape()

	def updateDown(self):
		global gameArray
		self.clearBlocks()

		goodToMove = True
		for a in range(len(self.blockList)):
			newX = self.blockList[a].xPos + 0
			newY = self.blockList[a].yPos + 1 
			
			if (not posInArray(newY, newX) and newY>ROWS-1) or valInPos(newY, newX):
				goodToMove = False
				self.stopBlocks()# STOP THE FUNCTION: SPAWN NEW SHPAE

		if goodToMove:
			for i in range(len(self.blockList)):
				self.blockList[i].xPos += 0
				self.blockList[i].yPos += 1
				# Update the center coordinates.
				if i == 0:
					self.cent_yPos = self.blockList[0].yPos
					self.cent_xPos = self.blockList[0].xPos

				self.blockList[i].draw(self.blockList[i].xPos, self.blockList[i].yPos)

	def drawBlocks(self):
		for i in range(len(self.blockList)):
			self.blockList[i].draw(self.blockList[i].xPos, self.blockList[i].yPos)#self.blockList[i].draw(self.cent_xPos, self.cent_xPos)

	def moveBlocks(self, direction):
		goodToMove = True
		for a in range(len(self.blockList)):
			thisRise = self.blockList[a].yPos - self.cent_yPos # y2 - y1
			thisRun = self.blockList[a].xPos - self.cent_xPos # x2 - x1

			if direction == "Right":
				newX = self.blockList[a].xPos + (1)
				newY = self.blockList[a].yPos
			elif direction == "Left":
				newX = self.blockList[a].xPos + (-1)
				newY = self.blockList[a].yPos

			if not posInArray(newY, newX) or valueThere(newY, newX): #valueThere(newY, newX): #or (newX >= 0 and newX <= COLS-1):#
				goodToMove = False
				return# STOP THE FUNCTION: this is not a valid rotation
		
		if goodToMove:
			self.clearBlocks()
			for i in range(len(self.blockList)):

				if direction == "Right":
					newX = self.blockList[i].xPos + (1)
					newY = self.blockList[i].yPos
				elif direction == "Left":
					newX = self.blockList[i].xPos + (-1)
					newY = self.blockList[i].yPos
				
				self.blockList[i].draw(newX, newY)
		print('MOved')

	def rotateBlocks(self, rotation):
		goodToMove = True
		for a in range(len(self.blockList)):
			thisRise = self.blockList[a].yPos - self.cent_yPos # y2 - y1
			thisRun = self.blockList[a].xPos - self.cent_xPos # x2 - x1

			if rotation == -90:
				newX = self.cent_xPos + (-thisRise)
				newY = self.cent_yPos + (thisRun)
			elif rotation == 90:
				newX = self.cent_xPos + (thisRise)
				newY = self.cent_yPos + (-thisRun)

			if not posInArray(newY, newX) or valueThere(newY, newX): #valueThere(newY, newX): #or (newX >= 0 and newX <= COLS-1):#
				goodToMove = False
				return# STOP THE FUNCTION: this is not a valid rotation
		
		if goodToMove:
			self.clearBlocks()
			for i in range(len(self.blockList)):
				thisRise = self.blockList[i].yPos - self.cent_yPos # y2 - y1
				thisRun = self.blockList[i].xPos - self.cent_xPos # x2 - x1

				if rotation == -90:
					newX = self.cent_xPos + (-thisRise)
					newY = self.cent_yPos + (thisRun)
				elif rotation == 90:
					newX = self.cent_xPos + (thisRise)
					newY = self.cent_yPos + (-thisRun)
				
				self.blockList[i].draw(newX, newY)
		print('ROTATED')
				

#shapeTest = Shape([[2,5],[3,7]])
shapeTest = Shape([[2,0],[3,0]])

def spawnNewShape():
	global shapeTest
	shapeTest = []
	shapeTest = Shape([[2,-1],[3,-1]])


def shapeMovement(array, direction):
	global shapeList, gameArray


def testNewRotation(array, rotation):
	global crntCentInd, crntRotation, crntShape

	# Use the information of the last used shape.
	tempShapeList = getShapeList(rotation, crntShape, array[crntCentInd].xPos, array[crntCentInd].yPos)

	for obj in tempShapeList:
		#print(validatePosition(obj.yPos, obj.xPos))
		if not validatePosition(obj.yPos, obj.xPos):
			#print("Invalid pos")
			return False

	# If all of the spaces are valid to rotate into, then return True to do it!
	return True



def checkGrid():
	global gameArray, gameOver

	# If the blocks have reach the top of the screen (Maybe make sure there is a zero in every row as well).
	for elem in gameArray[0]:
		if elem != 0:
			pass
			gameOver = True


def drawArray(array):
	global shapeList

 	#rectSize = 10
	SPREAD = 40
	MARG = 40
	for rows in range(ROWS):
		for cols in range(COLS):
			if array[rows][cols] > 0:
				drawText(str(array[rows][cols]), cols * SPREAD + MARG, rows * SPREAD + MARG)
				if shapeTest.cent_yPos == rows and shapeTest.cent_xPos == cols:
					drawText('C', cols * SPREAD + MARG, rows * SPREAD + MARG)
	shapeTest.drawBlocks()



def updateDisplay():
	timeTracker = 0
	global shapeList
	global gameArray
	global gameOver

	while not gameOver:
		timeTracker += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()
				elif event.key == pygame.K_RIGHT:
					shapeTest.moveBlocks("Right")
				elif event.key == pygame.K_LEFT:
					shapeTest.moveBlocks("Left")
				elif event.key == pygame.K_UP:
					shapeTest.rotateBlocks(90)
				elif event.key == pygame.K_DOWN:
					shapeTest.rotateBlocks(-90)

		gameScreen.fill(backgroundCol)
		if timeTracker % 80 == 0:
			None
			# Here, draw the array real time, but play the game in here (separate this function).
			#shapeMovement(shapeList, "Down")
			shapeTest.updateDown()

		drawArray(gameArray)


		pygame.display.update()
		clock.tick(60)

	while gameOver:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()

		

		if timeTracker % 10 == 0:
			gameScreen.fill(backgroundCol)
			#drawArray(gameArray)
			drawText("GAME OVER", 0, 0)


		pygame.display.update()
		clock.tick(60)

updateDisplay()