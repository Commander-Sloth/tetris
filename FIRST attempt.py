# Tetris Game recreation
# Started on 3/4/2020
import pygame
import sys
import random

# CURRENT BUG: The blocks are not spawning correctly. When i spawn them in the 0 column, they do not drop, however, a new shape IS being generated, just getting stuck. It just keeps making more and more.
# The blocks are not spawning properly still
# After rotating-90, it can go outside of the right side
gameArray = []
ROWS = 9
COLS = 9
gameOver = False
WIN_W = 500
WIN_H = 1000


# Global variable to address the last generated shape type.
crntCentInd = 0
crntRotation = 0
crntShape = ""
rotationDone = True

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
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,2,0,0,0,0],
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


class Shape():
	def __init__(self, startX, startY):
		self.yPos = startY
		self.xPos = startX
		self.num = random.randint(1,9)
		self.validToDrop = True
		self.validToLeft = True
		self.validToRight = True

	def updateDown(self):
		global gameArray
		if testUnder(gameArray, self.yPos, self.xPos):
			self.validToDrop = True
			if self.yPos >= 0:
				if gameArray[self.yPos+1][self.xPos] != 2:
					self.yPos = self.yPos + 1
				return
			else:
				self.yPos = self.yPos + 1
		else:
			self.getShape(2)
			self.validToDrop = False

	def updateRight(self):
		global gameArray
		if not testRight(gameArray, self.yPos, self.xPos):
			self.validToRight = False
		else:
			self.validToLeft = True
			self.xPos = self.xPos + 1

	def updateLeft(self):
		global gameArray
		if not testLeft(gameArray, self.yPos, self.xPos):
			self.validToLeft = False
		else:
			self.validToRight = True
			self.xPos = self.xPos - 1

	def getShape(self, value):
		global gameArray
		intoArray(gameArray, self.yPos, self.xPos, value)
				
	def blockDown(self):
		self.getShape(0)
		self.updateDown()
		self.getShape(1)


	def blockRight(self):
		self.getShape(0)
		self.updateRight()
		self.getShape(1)

	def blockLeft(self):
		self.getShape(0)
		self.updateLeft()
		self.getShape(1) # For some reason I had to comment these out, wierd glitch.

	def solidify(self):
		#print('Solodifying: R' + self.yPos + ", and C:" + self.xPos)
		self.getShape(2)


def getShapeList(rotation, shape, centX, centY):
	global crntCentInd, crntRotation, crntShape
	shapList = []

	# Just try to draw these from the (TOP DOWN), bottom up for some reason, because they are overwriting themselves when they are below.
	if shape == "I":
		crntShape = shape
		# Get the modulator to 0, if it is over 360 yeah?
		if rotation == 0 or rotation == 360 or rotation == -360:
			shapList.extend((Shape(centX, centY+1),Shape(centX, centY),Shape(centX, centY-1),Shape(centX, centY-2)))
			crntCentInd = 1
			#crntRotation = 0
		elif rotation == 180 or rotation == -180:
			shapList.extend((Shape(centX, centY+2),Shape(centX, centY+1),Shape(centX, centY),Shape(centX, centY-1)))
			crntCentInd = 2
		elif rotation == -90 or rotation == 270:
			shapList.extend((Shape(centX+2, centY),Shape(centX+1, centY),Shape(centX, centY),Shape(centX-1, centY)))
			crntCentInd = 2
		elif rotation == 90 or rotation == -270:
			shapList.extend((Shape(centX+1, centY),Shape(centX, centY),Shape(centX-1, centY),Shape(centX-2, centY)))
			crntCentInd = 1

	#print("Returning shapesList")
	return shapList

shapeList = getShapeList(0, "I", 4, -3) # Why can't I draw something in the 0 column?, my temp solution is just to spawn them in the middle

# NOT SPAWNING FOR SOMEREASON
def spawnNewShape():
	global shapeList, crntRotation

	crntRotation = 0
	
	shapeList.clear()

	#print("Remaking shapesList")
	shapeList = getShapeList(0, "I", 3, 0)#HERErandom.randint(1,6)

	for obj in shapeList:
		obj.validToDrop = True
		obj.validToLeft = True
		obj.validToRight = True

	#print(len(shapeList))
	#return


def shapeMovement(array, direction):
	global shapeList, gameArray

	if direction == "Down" and len(shapeList)>0:
		isOkToDrop = True
		for obj in shapeList:
			if obj.validToDrop == False:
				isOkToDrop = False
				gameArray[obj.yPos][obj.xPos] = 0
				obj.yPos +=1 # THIS SOLVED IT HAH
				#break


		print(isOkToDrop)

		

		if not isOkToDrop:
			shapeList[len(shapeList)-1].getShape(2)
			for u in range(len(shapeList) ):
				shapeList[u].solidify()
				print(str(shapeList[u].yPos))
			shapeList.clear()
			checkARow(shapeList) # HEre, make this test after the block is solidified
			spawnNewShape()
			checkGrid() # Ends the game.
			return# Stop processing this shape, get a new shape.

		elif isOkToDrop:
			for o in shapeList:	
				o.blockDown()
	elif direction == "Right" and len(array)>0:
		for obj in array:
			for o in array:
				if o.validToRight == False:
					return # Stop processing this shape, get a new shape.
			obj.blockRight()
	elif direction == "Left" and len(array)>0:
		for obj in array:
			for o in array:
				if o.validToLeft == False:
					return # Stop processing this shape, get a new shape.
			obj.blockLeft()


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


def shapeRotation(array, degrees):
	global shapeList
	global crntCentInd, crntRotation, crntShape
	global rotationDone

	rotationDone = False

	currentX = shapeList[crntCentInd].xPos
	currentY = shapeList[crntCentInd].yPos 

	newRotation = crntRotation + degrees

	if newRotation > 360:
			newRotation-=360
	elif newRotation < -360:
		newRotation+=360

	if testNewRotation(array, newRotation) == True:
		for obj in shapeList:
			gameArray[obj.yPos][obj.xPos] = 0

		shapeList.clear()

		shapeList = getShapeList(newRotation, crntShape, currentX, currentY)
		crntRotation = newRotation

		print("Rotated: " + str(crntRotation))

	rotationDone = True
		
	return


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
				

	



def updateDisplay():
	timeTracker = 0
	global shapeList
	global gameArray
	global gameOver
	global rotationDone

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
					shapeMovement(shapeList, "Right")
				elif event.key == pygame.K_LEFT:
					shapeMovement(shapeList, "Left")
				elif event.key == pygame.K_DOWN:
					if rotationDone and len(shapeList) > 0:
						
						shapeRotation(shapeList, -90)
					#print(rotationDone)


		if timeTracker % 30 == 0:
			gameScreen.fill(backgroundCol)
			# Here, draw the array real time, but play the game in here (separate this function).
			shapeMovement(shapeList, "Down")
		
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