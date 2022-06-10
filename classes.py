import pygame

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


class text_Button():
	def __init__(self, text, scale, color, font, x, y):	
		font = pygame.font.Font(font, scale)
		self.text_surface = font.render(text, True, color)
		self.rect = self.text_surface.get_rect(center=(x, y))
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.text_surface, (self.rect.x, self.rect.y))

		return action

class Player():
	def __init__(self, playerImg, x, y, obstacles, res):
		self.obstacles = obstacles
		self.res = res
		self.image = pygame.transform.scale(playerImg, [int(res[0]/16), int(res[1]/9)])
		self.rect = self.image.get_rect(center=(x, y))
		self.side = self.image.get_width()

	def move(self, dx, dy, current_chunk):

		# Move each axis separately. Note that this checks for collisions both times.
		if dx != 0:
			return self.move_single_axis(dx, 0, current_chunk)

		if dy != 0:
			return self.move_single_axis(0, dy, current_chunk)
		
		

 
	def move_single_axis(self, dx, dy, current_chunk):

		# Move the rect
		self.rect.x += dx
		self.rect.y += dy

  
		# If you collide with a wall, move out based on velocity
		for lines in range(9):
			for column in range(16):
				if current_chunk[lines][column] in self.obstacles:
					current_tile = pygame.Rect(column * self.res[0]/16, lines * self.res[1]/9, self.res[0]/16, self.res[1]/9)
					if self.rect.colliderect(current_tile):
						if dx > 0: # Moving right; Hit the left side of the wall
						    self.rect.right = current_tile.left
						if dx < 0: # Moving left; Hit the right side of the wall
						    self.rect.left = current_tile.right
						if dy > 0: # Moving down; Hit the top side of the wall
						    self.rect.bottom = current_tile.top
						if dy < 0: # Moving up; Hit the bottom side of the wall
						    self.rect.top = current_tile.bottom
		
		if self.rect.x + self.side>self.res[0]:
			self.rect.x=10
			return "right"
		elif self.rect.x<0:
			self.rect.x=self.res[0] - self.side -10
			return "left"
		if self.rect.y + self.side>self.res[1]:
			self.rect.y=100
			return "down"
		elif self.rect.y<0:
			self.rect.y=self.res[1]- self.side -10
			return "up"
