import tkinter as tk
import os, random


class Game(tk.Tk):

	def __init__(self):
		super().__init__()
		self.create_background()
		self.player = Player(self.canvas)
		self.jelly = self.add_jelly()
		self.bind_all_events()
		self.create_info_window()

	def create_background(self):
		self.bg = tk.PhotoImage(file="bg.png")
		self.canvas = tk.Canvas(width=self.bg.width(), height=self.bg.height())
		self.canvas.pack()
		self.canvas.create_image(self.bg.width() / 2, self.bg.height() / 2, image=self.bg)

	def gameover(self):
		self.endgame = tk.PhotoImage(file="gameover.png")
		self.canvas.create_image(self.bg.width() / 2, self.bg.height() / 2, image=self.endgame)

	def create_info_window(self):
		self.info_window = tk.PhotoImage(file="info.png")
		self.info_window = self.info_window.subsample(2)
		self.canvas.create_image(1400, 100, image=self.info_window)
		self.canvas.create_text(1350, 75, text=" POINTS:", font="arial 15")
		self.id_points = self.canvas.create_text(1450, 72, text="0", font="arial 25")
		self.canvas.create_text(1350, 120, text="LIVES  :", font="arial 15")
		self.id_lives = self.canvas.create_text(1450, 120, text="5", font="arial 25")

	def bind_all_events(self):
		self.canvas.bind_all("<KeyPress-Right>", self.player.press_right)
		self.canvas.bind_all("<KeyRelease-Right>", self.player.release_right)
		self.canvas.bind_all("<KeyPress-Left>", self.player.press_left)
		self.canvas.bind_all("<KeyRelease-Left>", self.player.release_left)
		# fire
		self.canvas.bind_all("<KeyPress-space>", self.player.fire)
		self.canvas.bind_all("<KeyRelease-space>", self.player.fire_stop)

	# self.canvas.bind_all("<KeyPress-Up>", self.player.press_up)
	# self.canvas.bind_all("<KeyRelease-Up>", self.player.release_up)

	def add_jelly(self):
		jellys = [yellow, yellow, black, yellow, red, blue, red, blue, red, blue, red, blue, black]
		jelly_type = random.choice(jellys)
		jelly = jelly_type(self.canvas)
		return jelly

	def timer(self):
		self.player.tik()
		self.jelly.tik()
		if self.jelly.destroyed:
			self.jelly = self.add_jelly()
			self.player.lives -= 1
			self.player.update_lives()

		if self.player.eat(self.jelly):
			self.jelly = self.add_jelly()
			self.player.show_points()

		if self.player.lives == 0:
			self.gameover()

		self.canvas.after(75, self.timer)


class BaseSprite():
	def __init__(self, canvas, x, y):
		self.canvas = canvas
		self.x, self.y = x, y
		self.id = self.canvas.create_image(x, y)
		self.destroyed = False

	def load_sprites(self, path):
		sprites = []
		folder = os.listdir(path)
		for item in folder:
			sprite_img = tk.PhotoImage(file=path + item)
			sprite_img = sprite_img.subsample(2)
			sprites.append(sprite_img)
		return sprites

	def tik(self):
		pass

	def destroy(self):
		self.destroyed = True
		self.canvas.delete(self.id)


class Jelly(BaseSprite):
	value = 0
	speed = 0

	def __init__(self, canvas):
		x = random.randrange(100, 1500)
		y = 0
		super().__init__(canvas, x, y)

	def move(self):
		y = self.y + self.speed
		if y <= 884:
			self.y = y
		else:
			self.destroy()
		self.canvas.coords(self.id, self.x, self.y)

	def tik(self):
		self.move()


class yellow(Jelly):
	value = 1
	speed = 8

	def __init__(self, canvas):
		super().__init__(canvas)
		self.sprites = self.load_sprites("sprites/jelly/")
		self.canvas.itemconfig(self.id, image=self.sprites[0])


class red(Jelly):
	value = 2
	speed = 10

	def __init__(self, canvas):
		super().__init__(canvas)
		self.sprites = self.load_sprites("sprites/jelly/")
		self.canvas.itemconfig(self.id, image=self.sprites[1])


class blue(Jelly):
	value = 5
	speed = 20

	def __init__(self, canvas):
		super().__init__(canvas)
		self.sprites = self.load_sprites("sprites/jelly/")
		self.canvas.itemconfig(self.id, image=self.sprites[2])


class black(Jelly):
	value = 10
	speed = 35

	def __init__(self, canvas):
		super().__init__(canvas)
		self.sprites = self.load_sprites("sprites/jelly/")
		self.canvas.itemconfig(self.id, image=self.sprites[3])


class Player(BaseSprite):
	MOVE = "move"
	IDLE = "idle"
	RWALK = "walk_right"
	LWALK = "walk_left"
	RJUMP = "jump_right"
	LJUMP = "jump_left"
	FIRE = "fire"

	def __init__(self, canvas, x=700, y=715):
		super().__init__(canvas, x, y)
		self.sprite_sheet = self.load_all_sprites()
		self.status = self.IDLE
		self.movement = self.IDLE
		self.sprite_idx = 0
		self.dx = 0
		self.dy = 0
		self.points = 0
		self.lives = 5

	def show_points(self):
		if game.id_points:
			self.canvas.delete(game.id_points)
		game.id_points = self.canvas.create_text(1450, 72, text=self.points, font="arial 25")

	def update_lives(self):
		if game.id_lives:
			self.canvas.delete(game.id_lives)
		game.id_lives = self.canvas.create_text(1450, 120, text=self.lives, font="arial 25")

	def eat(self, jelly):
		dist = ((self.x - jelly.x) ** 2 + (self.y - jelly.y) ** 2) ** 0.5
		if dist < 50:
			self.points = self.points + jelly.value
			jelly.destroy()
			return True
		else:
			return False

	def load_all_sprites(self):
		sprite_sheet = {
			self.MOVE: {
				self.RWALK: [],
				self.LWALK: [],
				self.RJUMP: [],
				self.LJUMP: []
			},
			self.IDLE: {
				self.IDLE: [],
				self.FIRE: []
			}
		}
		sprite_sheet[self.MOVE][self.RWALK] = self.load_sprites("sprites/walk_right/")
		sprite_sheet[self.MOVE][self.LWALK] = self.load_sprites("sprites/walk_left/")
		sprite_sheet[self.MOVE][self.RJUMP] = self.load_sprites("sprites/jump_right/")
		sprite_sheet[self.MOVE][self.LJUMP] = self.load_sprites("sprites/jump_left/")
		sprite_sheet[self.IDLE][self.IDLE] = self.load_sprites("sprites/idle/")
		sprite_sheet[self.IDLE][self.FIRE] = self.load_sprites("sprites/fire/")
		return sprite_sheet

	def next_animation_index(self, idx):
		idx += 1
		max_idx = len(self.sprite_sheet[self.status][self.movement])
		idx = idx % max_idx
		return idx

	def tik(self):
		self.sprite_idx = self.next_animation_index(self.sprite_idx)
		img = self.sprite_sheet[self.status][self.movement][self.sprite_idx]
		self.canvas.itemconfig(self.id, image=img)

		if self.status == self.MOVE:
			self.move()

	def move(self):
		x = self.x + self.dx
		y = self.y + self.dy
		if x >= 100 and x <= self.canvas.winfo_width() - 100:
			self.x = x
		self.canvas.coords(self.id, x, y)


	def press_right(self, event):
		self.status = self.MOVE
		self.movement = self.RWALK
		self.dx = 30

	def release_right(self, event):
		self.dx = 0
		self.status = self.IDLE
		self.movement = self.IDLE

	def press_left(self, event):
		self.status = self.MOVE
		self.movement = self.LWALK
		self.dx = -30

	def release_left(self, event):
		self.status = self.IDLE
		self.movement = self.IDLE
		self.dx = 0

	def fire(self, event):
		self.status = self.IDLE
		self.movement = self.FIRE

	def fire_stop(self, event):
		self.status = self.IDLE
		self.movement = self.IDLE


# def press_up(self, event):
# 	self.status = self.MOVE
# 	self.movement = self.RJUMP
# 	self.dy = -70
# 	self.dx = 30
#
# def release_up(self, event):
# 	self.dy = 0
# 	self.dx = 0
# 	self.status = self.IDLE
# 	self.movement = self.IDLE


game = Game()
game.timer()
game.mainloop()
