# Tetris Game recreation
# Started on 3/4/2020
import pygame
import sys
import random

# Make sure to get rid of unnecessary globaL decelerations
# SIDE: Display Shape, Score, What each key does

gameArray = []
ROWS = 20
COLS = 10
SPREAD = 40
MARG = 40
gameOver = False
WIN_W = COLS * SPREAD + MARG
WIN_H = ROWS * SPREAD + MARG
colors = [["Y", (254, 255, 3)],["R", (255, 3, 4)],["G", (3, 153, 2)],["L", (3, 255, 255)],["O", (255, 100, 3)],["B", (4, 3, 254)],["P", (160, 0, 241)],]

gameScreen = pygame.display.set_mode((WIN_W, WIN_H))

backgroundCol = (231, 223, 214)

clock = pygame.time.Clock()

pygame.display.set_caption("Tetris")

pygame.init()

# Set up the 2D array according to the desired rows and columns.
for i in range(ROWS):
	localCol = []
	for j in range(COLS):
		localCol.append(0)
	gameArray.append(localCol)

displayShape = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]

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


def posInArray(rowPos, colPos):
	if rowPos >= 0 and rowPos <= ROWS-1 and colPos <= COLS-1 and colPos >= 0:
		return True
	else:
		
		return False
	
# def valueThere(rowPos, colPos):
# 	if rowPos <= 0:
# 		return False
# 	if posInArray(rowPos, colPos):
# 		if gameArray[rowPos][colPos] != 0 and gameArray[rowPos][colPos] != 1:
# 			return True

# 	return False



def valInPos(rowPos, colPos):
	global gameArray
	if posInArray(rowPos, colPos) and gameArray[rowPos][colPos] != 0:
		return True # Bad value, there is something here.

	return False


def checkRows():
	global gameArray,shapeTest

	for thisRow in range(ROWS-1,-1,-1):
		if not (0 in gameArray[thisRow]) and not isinstance(gameArray[thisRow], int): # HERE, I had problems here, but I only want it to detect a FULL row of letters, not any numbers of the current moving shape.
			removeRow(thisRow)


def removeRow(rowThatIsFull):
	global gameArray, shapeTest

	shapeTest.updateDown()

	gameArray.pop(rowThatIsFull)
	
	columnToAdd = []
	for column in range(COLS+1):
		columnToAdd.append(0)

	gameArray.insert(0, columnToAdd)
	checkRows()

class block():
	def __init__(self, startX, startY, number):
		self.yPos = startY
		self.xPos = startX
		self.shapeID = number
		self.letter = colors[self.shapeID-1][0]

	def draw(self, x, y):
		global gameArray
		if posInArray(y, x) == True:
			gameArray[y][x] = self.shapeID

			self.xPos ,self.yPos = x, y

	def erase(self):
		global gameArray
		if posInArray(self.yPos, self.xPos):
			gameArray[self.yPos][self.xPos] = 0

	def freeze(self): # HERE:IS this function obsolete now?
		global gameArray
		if posInArray(self.yPos, self.xPos):
			gameArray[self.yPos][self.xPos] = self.letter

# Here: define color based off of id now		
class Shape():
	def __init__(self, coordinateList, shapeID): # [x,y]
		global displayShape
		self.cent_yPos = coordinateList[0][1]
		self.cent_xPos = coordinateList[0][0]
		self.shapeID = shapeID
		self.goodToRotate = True
		# self.value = random.randint(1,len(colors)) //If you want a random color, make a self.value variable to use. Truehen only use self.id when youcvaddress the type of shape; (but make sure the random number is passed to displayShape array so they match)

		# get a list of the coordinates based off of 1,2 // index coords, and set 
		self.displayCoors = getShapeList(1, 2, self.shapeID)
		for i in range(len(self.displayCoors)):
			displayShape[self.displayCoors[i][1]][self.displayCoors[i][0]] = self.shapeID

		if coordinateList == [[coordinateList[0][0], coordinateList[0][1]],[coordinateList[0][0]+1, coordinateList[0][1]],[coordinateList[0][0]+1, coordinateList[0][1]+1],[coordinateList[0][0], coordinateList[0][1]+1]]:
			self.goodToRotate = False # If this shape is a square, probably don't move it.

		self.blockList = []
		for i in range(len(coordinateList)):
			self.blockList.append(block(coordinateList[i][0],coordinateList[i][1], self.shapeID))

	def clearBlocks(self):
		global gameArray
		for i in range(len(self.blockList)):
			self.blockList[i].erase()

	def stopBlocks(self): # Here: Small bug: (Hard to see): The problem is: a row is deleted, and a new block spawns, but it hits a wall at the top, and the game stops for some reason.
		global gameArray, gameOver
		for i in range(len(self.blockList)):
			self.blockList[i].freeze()
			if self.blockList[i].yPos == 0:
				gameOver = True
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
		global gameArray
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

			if not posInArray(newY, newX) or (posInArray(newY, newX) and gameArray[newY][newX] != 0 and gameArray[newY][newX] != self.shapeID): #valueThere(newY, newX): #or (newX >= 0 and newX <= COLS-1):#
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

	def rotateBlocks(self, rotation):
		global gameArray

		goodToMove = self.goodToRotate
		for a in range(len(self.blockList)):
			thisRise = self.blockList[a].yPos - self.cent_yPos # y2 - y1
			thisRun = self.blockList[a].xPos - self.cent_xPos # x2 - x1

			if rotation == -90:
				newX = self.cent_xPos + (-thisRise)
				newY = self.cent_yPos + (thisRun)
			elif rotation == 90:
				newX = self.cent_xPos + (thisRise)
				newY = self.cent_yPos + (-thisRun)

			if not posInArray(newY, newX) or (posInArray(newY, newX) and gameArray[newY][newX] != 0 and gameArray[newY][newX] != self.shapeID): #valueThere(newY, newX): #or (newX >= 0 and newX <= COLS-1):#
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
				
# Here: make the shapes unrotatible if it is a square. If the shape coordinates list matches the square, dont rotateit.
def getShapeList(x, y, randInt):
	centX = x
	centY = y
	shapeList = [
		[
			[centX, centY],[centX+1, centY],[centX+1, centY+1],[centX, centY+1]
		], # O
		[
			[centX, centY],[centX-1, centY-1],[centX, centY-1],[centX+1, centY]
		], # Z
		[
			[centX, centY],[centX-1, centY],[centX+1, centY-1],[centX, centY-1]
		], # S
		[
			[centX, centY],[centX, centY+1],[centX, centY-1],[centX, centY-2]
		], # I
		[
			[centX, centY],[centX, centY+1],[centX+1, centY+1],[centX, centY-1]
		], # L
		[
			[centX, centY],[centX, centY+1],[centX-1, centY+1],[centX, centY-1]
		], # J
		[
			[centX, centY],[centX, centY+1],[centX-1, centY],[centX+1, centY]
		] # T
	]

	blockCoorList = shapeList[randInt-1]#random.choice(shapeList)

	return blockCoorList # [[2,0],[3,0]]

randomShapeID = random.randint(1,7) # 7 is the number of different shapes
shape = getShapeList(round(COLS/2), -1, randomShapeID)
shapeTest = Shape(shape, randomShapeID)#shapeRotable(shape)

def spawnNewShape():
	global shapeTest, displayShape
	displayShape = [[0, 0, 0],[0, 0, 0],[0, 0, 0],[0, 0, 0]]
	shapeTest = []
	randomShapeID = random.randint(1,7) # 7 is the number of different shapes
	shape = getShapeList(round(COLS/2), -1, randomShapeID)
	shapeTest = Shape(shape, randomShapeID)#shapeRotable(shape)


def checkGrid(): # HERE, delete this
	pass
	# global gameArray, gameOver

	# # If the blocks have reach the top of the screen (Maybe make sure there is a zero in every row as well).
	# for elem in gameArray[0]:
	# 	if elem == 0:
	# 		continue
	# 	gameOver = True



def drawArray(array):
	global shapeTest, displayShape

	for rows in range(ROWS):
		for cols in range(COLS):
			if array[rows][cols] != 0:
				# HERE: USE LETTER TO SOLIDIFY. SOLIDIFY TO A LETTER basded on number, and draw the colors based on number Or letter
				#drawText(str(array[rows][cols]), cols * SPREAD + MARG, rows * SPREAD + MARG)
				thisColor = (100, 100, 100)

				if isinstance(array[rows][cols], str):
					for elem in colors:
						if elem[0] == array[rows][cols]:
							thisColor = elem[1]
						#break

				elif isinstance(array[rows][cols], int):
					thisColor = colors[array[rows][cols]-1][1]
 
				pygame.draw.rect(gameScreen, thisColor, ((cols * SPREAD) + MARG - SPREAD/2, (rows * SPREAD) + MARG - SPREAD/2, SPREAD, SPREAD))
				# if shapeTest != []:  
				# 	if shapeTest.cent_yPos == rows and shapeTest.cent_xPos == cols:
				# 		drawText('C', cols * SPREAD + MARG, rows * SPREAD + MARG)

	if shapeTest != []:
		shapeTest.drawBlocks()

	for rows in range(4):
		for cols in range(3):
			if displayShape[rows][cols] != 0:
				thisColor = colors[displayShape[rows][cols]-1][1]
				pygame.draw.rect(gameScreen, thisColor, ((cols * SPREAD) + MARG - SPREAD/2, (rows * SPREAD) + MARG - SPREAD/2, SPREAD, SPREAD))
	#checkGrid(), I donty think I need this because I am checking the rows in the updateDisplay loop also



def updateDisplay():
	timeTracker = 0
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
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					if shapeTest != []:
						shapeTest.updateDown()
					#shapeTest.rotateBlocks(-90)., This used to be in the KEYUP event

		gameScreen.fill(backgroundCol)
		if timeTracker % 20 == 0:
			None
			# Here, draw the array real time, but play the game in here (separate this function).
			#shapeMovement(shapeList, "Down")
			checkRows()
			if shapeTest != []:
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
			drawText("GAME OVER", WIN_W/2, WIN_H/2)
			drawArray(gameArray)

		pygame.display.update()
		clock.tick(60)

updateDisplay()