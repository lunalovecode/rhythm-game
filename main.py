import pygame as pg
import math
import time

pg.init()

screen = pg.display.set_mode((800, 600), pg.RESIZABLE)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

pg.display.set_caption("Peripheral")
# Idea 1: Square Good
# 5 by 5 grid of squares
# squares fade into the background. click on them before they fade
# if they fade, it will briefly reappear as red and disappear again
# some squares are replaced by circles. do not click on them

# Idea 2: Peripheral
# a large circle in the middle of the screen. press the space bar to the beat.
# arrows appear on the screen from time to time, and you have to press WASD (or the arrow keys)
# up arrows usually appear above the circle, down arrows usually appear below the circle, left arrows appear to the left, and right arrows appear to the right
# sometimes, the places they appear change. an up arrow could appear on the left side of the circle, a down arrow could be above it, a right arrow could be below, etc.
# only 1 arrow is on the screen at a time

class Circle(pg.sprite.Sprite):
    def __init__(self, radius, color, callback, coords):
        super().__init__()
        self.image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        self.color = color
        pg.draw.circle(self.image, self.color, (radius, radius), radius, 0)
        self.callback = callback
        self.rect = self.image.get_rect(center=(coords[0], coords[1]))
 
    def update(self, events):
        for event in events: 
            # if event.type == pg.MOUSEBUTTONUP:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # if self.rect.collidepoint(event.pos):
                self.callback()

class Arrow(pg.sprite.Sprite):
    def __init__(self, size, coords, direction):
        super().__init__()

        self.size = size
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        half_size = size / 2
        height = math.sqrt(3) / 2 * size
        
        self.direction = direction
        if self.direction == "up":
            self.color = (0, 255, 0)
            self.points = (
                (SCREEN_WIDTH / 2, 0), # top
                ((SCREEN_WIDTH / 2) + half_size, size), # right
                ((SCREEN_WIDTH / 2) - half_size, size) # left
            )
        elif self.direction == "down":
            self.color = (0, 255, 255)
            self.points = (
                (SCREEN_WIDTH / 2, SCREEN_HEIGHT),  # top
                ((SCREEN_WIDTH / 2) + half_size, SCREEN_HEIGHT - size), # right
                ((SCREEN_WIDTH / 2) - half_size, SCREEN_HEIGHT - size) # left
            )
        elif self.direction == "left":
            self.color = (255, 0, 0)
            self.points = (
                (size, SCREEN_HEIGHT / 2),  # top
                (2 * size, (SCREEN_HEIGHT / 2) + half_size), # right
                (2 * size, (SCREEN_HEIGHT / 2) - half_size) # left
            )
        else:
            self.color = (255, 255, 0)
            self.points = (
                (SCREEN_WIDTH - size, SCREEN_HEIGHT / 2),  # top
                (SCREEN_WIDTH - (2 * size), (SCREEN_HEIGHT / 2) + half_size), # right
                (SCREEN_WIDTH - (2 * size), (SCREEN_HEIGHT / 2) - half_size) # left
            )
        pg.draw.polygon(screen, self.color, self.points)
        self.rect = self.image.get_rect(center=(coords[0], coords[1]))
    
    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_UP or event.key == pg.K_w) and self.direction == "up":
                    self.kill()
                if (event.key == pg.K_DOWN or event.key == pg.K_s) and self.direction == "down":
                    self.kill()
                if (event.key == pg.K_LEFT or event.key == pg.K_a) and self.direction == "left":
                    self.kill()
                if (event.key == pg.K_RIGHT or event.key == pg.K_d) and self.direction == "right":
                    self.kill()

def on_space():
    global circle_alpha
    circle_alpha = 0

main_circle = Circle(100, (255, 255, 255), on_space, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
circle_alpha = 0
group = pg.sprite.GroupSingle(main_circle)
arrows = pg.sprite.Group()
font = pg.font.Font("Lato-Regular.ttf", 30)
text = None
# text_rect = text.get_rect()
# text_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 130)
text_alpha = 255
text_timer = 0
text_duration = 10
clock = pg.time.Clock()
pg.mixer.music.load("modern chillout.mp3")
beat_sound = pg.mixer.Sound("tap.wav")
beat_sound.set_volume(0.2)
bpm = 128
interval = 60 / bpm
last_beat = time.time()
miss_window = 0.2
pressed_circle = False
pressed_arrow = False
run = True
beats = 0
arrow_direction = "down"
arrow = Arrow(100, (100, 100), "down")
while run:
    # pg.draw.circle(screen, (100, 0, 100), (200, 200), 170, 5)
    # clock.tick(60)
    screen.fill((0, 0, 0))
    if beats <= 8:
        beat_sound.play()
    elif beats == 9:
        pg.mixer.music.play()
    elif beats > 9 and beats < 13 and (not pressed_arrow):
        arrow = Arrow(100, (100, 100), "down")
        arrows.add(arrow)

    current_time = time.time()
    since_last_beat = current_time - last_beat
    
    if since_last_beat >= interval:
        if not pressed_circle:
            print("Miss!")
            text = font.render("Miss!", True, (255, 255, 255))
            text_alpha = 255
            text_timer = text_duration
            circle_alpha = 0
            main_circle.image.set_alpha(circle_alpha)
        
        beats += 1
        print(beats)
        last_beat = current_time
        pressed_circle = False
    
    circle_alpha += 0.5
    main_circle.image.set_alpha(circle_alpha)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_SPACE:
                if abs(since_last_beat) < miss_window:
                    print("Perfect!")
                    text = font.render("Perfect!", True, (255, 255, 255))
                    # text_alpha -= 100
                    # text.set_alpha(text_alpha)
                elif since_last_beat > 0:
                    print("Late!")
                    text = font.render("Late!", True, (255, 255, 255))
                    # text_alpha -= 100
                    # text.set_alpha(text_alpha)
                else:
                    print("Early!")
                    text = font.render("Early!", True, (255, 255, 255))
                    # text_alpha -= 100
                    # text.set_alpha(text_alpha)
                pressed_circle = True
                circle_alpha = 0
                text_alpha = 255
                text_timer = text_duration
                main_circle.image.set_alpha(circle_alpha)
            elif event.key == pg.K_s:
                pressed_arrow = True
                # arrow.color = (0, 0, 0)
        elif event.type == pg.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
            main_circle.rect.x = (SCREEN_WIDTH / 2) - 100
            main_circle.rect.y = (SCREEN_HEIGHT / 2) - 100
            # text_rect.center = (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 130)

    if text:
        text_timer -= (1 / 60)
        if text_timer > 0:
            text_alpha = max(0, text_alpha - 1)  # Reduce opacity by 5 per frame
            text.set_alpha(text_alpha)
            screen.blit(text, ((SCREEN_WIDTH / 2) - text.get_width() // 2, ((SCREEN_HEIGHT / 2) - text.get_height() // 2) - 130))
        else:
            text = None
    
    group.update(events)
    group.draw(screen)
    pg.display.update()

pg.quit()