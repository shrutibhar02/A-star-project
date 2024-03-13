import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # setting the size of the display box
pygame.display.set_caption(" Python Project on A* Path Finding Algorithm for CWS Evaluation") 

# color codes which we will be using
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#before impementing the A* algo we need to create a visualizer where we will be implementing the code 


class Spot:    # track of nodes or cubes in the grid
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width # Actual postion of the cube in the Grid 
		self.y = col * width 
        # By multiplying the width with the row or column position
		# we can easily show the position of the cube in the Grid which we are going to make 
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):   # to return the postion 
		return self.row, self.col
	def is_closed(self): 
		return self.color == RED
	def is_open(self):
		return self.color == GREEN
	def is_barrier(self):
		return self.color == BLACK
	def is_start(self):
		return self.color == ORANGE
	def is_end(self):
		return self.color == TURQUOISE
	def reset(self):
		self.color = WHITE
	def make_start(self):
		self.color = ORANGE
	def make_closed(self):
		self.color = RED
	def make_open(self):
		self.color = GREEN
	def make_barrier(self):
		self.color = BLACK
	def make_end(self):
		self.color = TURQUOISE
	def make_path(self):
		self.color = PURPLE
	
	def draw(self, win):  # drawing the spot or cubes 
        # for drawing we will require actual coordinates  i.e x and y ,length and breadth of each cube
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))  # .rect to draw rectangle 

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2): # function for measuring the manhaatan distance 
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2) # absolute distance  


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start)) # insert these into the priority queue , count is to keep check in case of same f values 
	came_from = {} 
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start} # to keep check about all the items present or not present in priority queue

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2] # returns only the value at index 2 i.e node 
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width): # defining the grids 
    # no of rows and columns are equal 
	grid = []
	gap = width // rows  # width of the cube  
	for i in range(rows): # rows
		grid.append([])   # making a 2d empty list
		for j in range(rows): # columns
			spot = Spot(i, j, gap, rows) 
			grid[i].append(spot) # list of small cubes or spots are saved inside the list named grid

	return grid


def draw_grid(win, rows, width):  # creating the gridlines
	gap = width // rows # width of a cube or spot
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) # creating the horizonal grid lines
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) # creating the vertical grid lines 


def draw(win, grid, rows, width): # main draw function which is going to draw everything 

	win.fill(WHITE) # filling everything with white acoording to the frame 

	for row in grid: #selecting a particular row from the 2d list of n rows  
		for spot in row: #selecting a spot or a cube of a particular row
			spot.draw(win) # already defined above in line 75 

	draw_grid(win, rows, width) # creating the grid lines 
	pygame.display.update() # updating the display

# to get the coordinate of the point where we clicked with the mouse button
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50 # defining the rows 
	grid = make_grid(ROWS, width)

	start = None # initialising the start and end 
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get(): # check while the program is running 
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT Mouse button 
				pos = pygame.mouse.get_pos()# return the postion already defined above in line 36
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end: #start and end should be not same(corner case)
											  #checking if start or end has been pressed or not
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot 
					end.make_end()

				elif spot != end and spot != start:   # creating the barrier
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT Mouse button for resetting the start and end
				pos = pygame.mouse.get_pos() # return the postion already defined above in line 36
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN: # to check whether a key has been pressed physically or not 
				if event.key == pygame.K_SPACE and start and end: 
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid) # check the neighbours for a barrier 

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # calling the algorithm function

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)