# Tetris Game recreation
# Started on 3/4/2020
import pygame
import sys
import random

gameArray = []
ROWS = 16
COLS = 10
gameOver = False
WIN_W = 300
WIN_H = 800

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

print(gameArray)

gameArray[ROWS-1][0] = 2


def print_2DArray(array):
	for row in range(ROWS):
		print(array[row])

print_2DArray(gameArray)

def drawText(labelText, xPos, yPos):
	fontColor = (255, 255, 255)
	font = pygame.font.Font("freesansbold.ttf", 25)
	text = font.render(labelText, True, fontColor)
	textRect = text.get_rect()
	textRect.center = (xPos, yPos)
	return gameScreen.blit(text, textRect)

def intoArray(array, row, col, val):
	if row >= 0 and row < ROWS and col >= 0 and col < COLS:
		array[row][col] = val

# Return False if the position below is 2 or the edge
def testUnder(array, row, col):
	if row > ROWS - 2:
		print("Hit bottom")
		return False

	elif row > 0 and row < ROWS -1 and array[row+1][col] == 2: 

		print("Hit a 2 at ROW: " + str(row))
		return False

	return True

class Shape():
	def __init__(self, startX, startY):
		self.yPos = startY
		self.xPos = startX
		#self.rotation = rotation
		#self.shape = shape
		self.num = random.randint(1,9)
		self.validToMove = True
		
		#ONLY DRAW IT IF IT IS IN THE ARRAY

	def updatePos(self):
		global gameArray
		if not testUnder(gameArray, self.yPos, self.xPos):
			self.validToMove = False
		if self.validToMove:
			self.yPos = self.yPos + 1

	def getShape(self, value):
		global gameArray
		intoArray(gameArray, self.yPos, self.xPos, value)
				

	def drawShape(self):
		self.getShape(0)
		self.updatePos()
		self.getShape(1)

	def draw(self):
		self.getShape(2)


def getShapeList(rotation, shape, centX, centY):
	shapesList = []

	# Just try to draw these from the (TOP DOWN)obottom up for some reason, because they are overwriting themselves when they are below.
	if shape == "I":
		# Get the modulator to 0, if it is over 360 yeah?
		if rotation == 0 or 180:
			shapesList.extend((Shape(centX, centY+1),Shape(centX, centY),Shape(centX, centY-1),Shape(centX, centY-2)))		

	return shapesList

testShape = getShapeList(0, "I", random.randint(0,COLS-1), -3)

def getNewShape():
	global testShape

	testShape = []
	testShape = getShapeList(0, "I", random.randint(0,COLS-1), -3)

def processShape(array):
	for obj in array:
		for o in array:
			if o.validToMove == False:
				for objw in array:
					objw.draw()

				getNewShape()
				checkGrid() # HERE, draw the grid before you restARt, to see what happened
				return # Stop processing this shape, get a new shape.
		obj.drawShape()

def checkGrid():
	global gameArray, gameOver
	for elem in gameArray[0]:
		if elem != 0:
			pass
			gameOver = True


def drawArray(array):

	processShape(testShape)

 	#rectSize = 10
	SPREAD = 40
	MARG = 40
	for rows in range(ROWS):
		for cols in range(COLS):
			drawText(str(array[rows][cols]), cols * SPREAD + MARG, rows * SPREAD + MARG)


def updateDisplay():
	timeTracker = 0

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

		if timeTracker % 50 == 0:
			gameScreen.fill(backgroundCol)
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