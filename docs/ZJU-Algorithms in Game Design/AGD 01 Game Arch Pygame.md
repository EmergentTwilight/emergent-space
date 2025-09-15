---
status:
  - archived
tags: CS/Language/Python/Pygame
attachment:
  - "[[slides/S01_GameArchPygame.pdf|GameArchPygame]]"
date_created: 2024-10-25T18:24:59
date_modified: 2025-09-12T15:23:18
number headings: auto, first-level 1, max 6, contents ^toc, skip ^skipped, 1.1
---

# 1 Conclusion

代码不用学，直接查就好

# 2 Pygame

- Python for writing video games
	- [[slides/S01_GameArchPygame.pdf#page=10&selection=0,0,0,7|Modules]]
	- Install `pip/conda install pygame`

## 2.1 Example

```python title="intro1.py"
import pygame

pygame.init()

size = width, height = 1024, 768
speed = [3, 2]
black = (0, 0, 0)

screen = pygame.display.set_mode(size)
logo = pygame.image.load('new.jpg')
logo_width, logo_height = logo.get_size()
logo_x = logo_y = 0

running = True

while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            running = False  

    logo_x += speed[0]
    logo_y += speed[1]

    if logo_x < 0 or logo_x + logo_width > width:
        speed[0] = -speed[0]
    if logo_y < 0 or logo_y + logo_height > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(logo, (logo_x, logo_y))
    pygame.display.flip()
```

创建一个窗口，窗口内 `new.jpg` 在移动，接触到边反弹

# 3 Game Loop

- the common structure
	- initialization
	- a loop (while running)
		- **check inputs**, from user, network
		- **upgrade game state**, based on inputs
		- **draw next frame**, based on the state
- philosophy: games need to be **responsive**

## 3.1 Frame

- one picture is rendered each time, which is a frame
- FPS is usually an important **design metric/goal**

```python title="normal structure of a game"
initialize_game()
while not done:
	*user_inputs, done = get_inputs()
	game_state = update_game_state(user_inputs)
	render_game(game_state)
```

## 3.2 Event Queue

- Pygame uses **event queue** to manage user inputs
	- FIFO: first-in-first-out
	- Event: an object representing sth. happening in the system
- Each game loop, you must **handle all the events in the queue**
- Pygame's event module has very extensive features for handling the even queue

### 3.2.1 Event Objects

- `event_object.type`
	- `KEYDOWN`: `key`, `mod`(are shift, ctrl keys also pressed), `unicode`, `scancode`
	- `MOUSEBUTTONDOWN`: `pos`(x, y of the cursor), `button`(which is clicked)
	- `VIDEORESIZE`: `size`

```python title="Example event processing"
def get_inputs()
	done = ledt = right = False
	for event in pygamme.event.get():
		if event.type == pygame.QUIT
			done = True
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE
				done = True
			elif event.key == pygame.K_RIGHT:
				right = True
			elif event.key == pygame.K_LEFT:
				left = True
	return (left, right, done)
```

# 4 Game Architecture

- **Architecture** is all about the structure of our code.
	- components
	- how they interact with each other

## 4.1 MVC: Model-View-Controller

- MVC is a common architectural style for GUI, web applications and games

### 4.1.1 Model

- **Manages the data and operations on the data**
- Provides a well-defined interface to the data
	- *changes to the data structure don't require changes to the rest of the code*
- In web and many GUI apps, model is a **database**
- Example: Chess Game
	- Data: where are all pieces, which have been captured
	- Operations: init, moving pieces, werid moves, scoring of captured pieces

### 4.1.2 View

- **Provides a way to visualize the data**
	- frame, music, runble, etc.
- Example: Chess Game
	- 2D/3D/VR, phone/laptor/console views

### 4.1.3 Controller

- **Maps input actions to model or view actions**
	- input actions: user input
	- model actions: avatar moved left, opponent forfeits, spaceship explodes...
	- view actions: window resized, menu button pressed, instant replay requested
- Game customizations often result in **different mappings** for the controller
	- WASD/arrow keys

### 4.1.4 Advice on MVC

- When programming, start with the model, how to store data and how are they controlled

## 4.2 Object-Orinted Model/View

- Another common style is having **objects**
	- Pac-Man, Ghosts, fruit, the maze ...

### 4.2.1 Object

- Each object knows **its own state** and update rules, so is part of the model
- A model component may still keep trach of all objects and tell them when to update

### 4.2.2 Draw

- Each object knows **how to draw itself**, so is part of view
	- `object.draw()` is called by the view module

### 4.2.3 Conclusion

- You still have a model, *which calls `object.update()`*
- You still have a view, *which calls `object.draw()`, in correct order*

# 5 Graphic Primitives

- Provides visual feedback
- Provides guidance

## 5.1 Engine

- An engine provides some level of graphic algorithms to be **embedded** in your code

### 5.1.1 Digital Image

- array of pixels of colors
- RGB/RGBA, `A` is for **Alpha Channel**

## 5.2 The Surface

- In Pygame, a **surface** is a place to draw
- Special surface, the **display surface**, is visible to the user in game window
	- `{python}display_surface = pygame.display.set_mode((1024, 768))`
- Other surfaces can be created too
- Commonly, have a background surface
	- `{python}background = pygame.Surface(display_surface.get_size())`
	- 每一帧先复制一遍 `background` 再开始绘图

### 5.2.1 Surface Operations

- set the color of single pixel`{python}background.set_at((x, y), color)`
- get the color of single pixel `{python}color = background.get_at(x, y)`

```python title="draw_notepaper.py (naive version)"
def draw(surface, size_x, size_y):
	blue = (0, 0, 200)
	red = (200, 0, 0)
	white = (255, 255, 255)
	
	# draw white background
	for x in range(size_x):
		for y in range(size_y):
			surface.set_at((x, y), white)
	
	# draw horizontal lines
	for y in range(60, size_y, 20):
		for x in range(size_x):
			surface.set_at((x, y), red)
	
	# draw a red vertical line in the left
	x = 25
	for y in range(0, size_y):
		surface.set_at((x, y), red)
```

## 5.3 `pygame.draw`

> TMBABW *There must be a better way*

```python title="draw_notepaper.py (better version)"
def draw(surface, size_x, size_y):
	blue = (0, 0, 200)
	red = (200, 0, 0)
	white = (255, 255, 255)
	
	# draw white background
	surface.fill(white)
	
	# draw horizontal lines
	for y in range(60, size_y, 20):
		left_side = (0, y)
		right_side = (size_x, y)
		pygame.draw.line(surface, blue, left_size, right_side)
	
	# draw a red vertical line in the left
	pygame.draw.line(surface, red, (25, 0), (25, size_y))
```

- `{python}pygame.draw.arc(surface, color, rect, start_angle, stop_angle, width=1)`
	- `rect` 是一个 bounding box
	- `start_angle` 和 `stop_angle` 是弧度制的
- `{python}pygame.draw.lines(surface, color, closed, points, width=1)`
	- 绘制一些直线，经过 `points` 列表里的所有 `(x, y)` 元组
	- `closed: bool`，是否生成闭合图形
- `{python}pygame.draw.polygon(surface, color, points, width=1)`
	- 连接所有 `(x, y)` 点，并填充封闭空间
- `{python}pygame.draw.circle(surface, color, center, radius)`

```python title="draw_python.py -- Draw the Python logo"
surface.fill(white)
points = [(27, 50), (76, 50), (76, 45), (45, 45), (45, 26)]
pygame.draw.lines(surface, blue, False, points)
pygame.draw.arc(surface, blue, (45, 15, 61, 22), 0*radians, 180*radians)
pygame.draw.line(surface, blue, (106, 26), (106, 62))
pygame.draw.arc(surface, blue, (76, 47, 30, 30), 270*radians, 0*radians)
pygame.draw.line(surface, blue, (91, 76), (57 ,76))
pygame.draw.arc(surface, blue, (41, 76, 32, 32), 90*radians, 180*radians)
pygame.draw.line(surface, blue, (41, 92), (41, 110))
pygame.draw.line(surface, blue, (41,110), (27, 110))
pygame.draw.arc(surface, blue, (12,50,30, 60), 90*radians, 270*radians)
......
```

## 5.4 `pygame.rect`

- `{python}pygame.Rect(x, y, width, height)`
- `{python}pygame.Rect((x, y), (width, height))`
- [[slides/S01_GameArchPygame.pdf#page=64&selection=0,0,0,12|Rect Methods]]

## 5.5 Using Rects with Draw

- `{python}pygame.draw.rect(surface, color, rect, width=0)`
- `{python}pygame.draw.ellipse(surface, color, rect, width=0)`

```python title="Use rects for boxes, circles in draw_checherboard.py"
rect = pygame.Rect(strip_size, strip_size, box_size, box_size)  # make rect for checkerboard box
color = black
for row in range(8):
	for col in range(8):
		pygame.draw.rect(surface, color, rect)  # draw the box
		if row in rows_with_pieces and color == black:
			circle_rect = rect.inflate(deflate, deflate)
			pygame.draw.ellipse(surface, white, circle_rect)   # draw ellipse in smaller box
		rect.move_ip(box_size + strip_size, 0)  # move rect to the next place in row
		if color == black:
			color = red
		else:
			color = black
	rect.move_ip(-8*(box_size + strip_size), box_size + strip_size)  # move rect to next row
	if color == black:
		color = red
	else: 
		color = black
```

# 6 Images and Blit

- 使用 `.png, .jpg, .gif` 等图像代替绘制语句
- Pygame supports PG, PNG, GIF + BMP, PCX, TGA, TIF, LBM, PBM, PPM and XPM formats

## 6.1 Image Load/Save

- `{python}surface = pygame.image.load(filename)`
- `{python}pygame.image.save(surface, filename)`
- `{python}pygame.surface.convert()`
	- 能够修改 `surface` 的格式来 match `display surface`
	- 最好对每个加载的 image 都使用，不然每次都要 `convert`

## 6.2 BLIT

- 每个图像都是单独的 `surface`，但是需要在每个 loop 结尾绘制单个 `display_surface`
- `blit` 能够复制粘贴图像

### 6.2.1 Pygame blit

- `surface` 对象具有这样的方法：`{python}surface.blit(source, dest, area=None, special_flags=0)`
	- `source` 另一个 `surface`
	- `dest` 是一个 `(x, y)` 坐标
	- `area` 可以是一个 `rect`，来限制粘贴的范围

```python title="render mario"
display_surface = pygame.display.set_mode(1200, 622)
background = pygame.image.load('mario_background.png').convert()
mario = pygame.image.load('mario_sprited.png').convert()
...
while not done:
	*user_inputs, done = get_inputs()
	...
	jump_r = pygame.Rect(254, 13, 42, 49)
	display_surface.blit(background, (0, 0))
	display_surface.blit(mario, (390, 510), jump_r)
	pygame.display.flip()
```

### 6.2.2 Blit Optimizaiton

> 使用 `spacial_flags` 参数加速处理过程，`ADD, SUB, MULT, MIN, MAX`

## 6.3 ColorKey

> 用于将素材种的某种颜色当成透明，不覆写 `display_surface` 中的部分像素

```python title="render mario"
display_surface = pygame.display.set_mode(1200, 622)
background = pygame.image.load('mario_background.png').convert()
mario = pygame.image.load('mario_sprited.png').convert()
white = mairo.get_at((0, 0))
mario.set_colorkey(white)
...
while not done:
	*user_inputs, done = get_inputs()
	...
	jump_r = pygame.Rect(254, 13, 42, 49)
	display_surface.blit(background, (0, 0))
	display_surface.blit(mario, (390, 510), jump_r)
	pygame.display.flip()
```

## 6.4 Surface Transforms

- You can `rotate` / `scale` / `chop` / `greyscale` / ...
- `{python}pygame.transform.rotate(source_surface, angle) -> Surface`

# 7 Conclusion

- Games are a part of human nature
- Game architectures are important
- Pygame engine is a library with lots of useful routines
	- lines, colors, circles, images, ...
	- events
	- surfaces

> [!hint]
> 其实 python 程序可读性都很强，完全不用记这些函数定义也能看懂
