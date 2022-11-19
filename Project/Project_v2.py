import pygame
import random
from pygame import Vector2

SPRITE_SHEET = None

GREEN_SHIP  = pygame.Rect(0, 292, 32, 32)
RED_SHIP    = pygame.Rect(0, 324, 32, 32)
BLUE_SHIP   = pygame.Rect(0, 356, 32, 32)
YELLOW_SHIP = pygame.Rect(0, 388, 32, 32)


class EnemyController:

    def __init__(self):
        self.direction = Vector2(1, 0)

    def update(self, sprite, events, dt):
        if not pygame.display.get_surface().get_rect().contains(sprite.rect):
            self.direction *= -1
        sprite.direction = self.direction

class PlayerController:

    movement = {
        pygame.K_UP:    Vector2( 0, -1),
        pygame.K_DOWN:  Vector2( 0,  1),
        pygame.K_LEFT:  Vector2(-1,  0),
        pygame.K_RIGHT: Vector2( 1,  0)
    }

    def update(self, sprite, events, dt):
        pressed = pygame.key.get_pressed()
        v = Vector2(0, 0)
        for key in PlayerController.movement:
            if pressed[key]:
                v += PlayerController.movement[key]

        sprite.direction = v

        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    sprite.groups()[0].add(Explosion(sprite.pos))

class Animation:
    def __init__(self, frames, speed, sprite):
        self.sprite = sprite
        self.speed = speed
        self.ticks = 0
        self.frames = frames
        self.running = 0
        self.start()

    def cycle_func(self, iterable):
        saved = []
        for element in iterable:
            yield element
            saved.append(element)
        if hasattr(self.sprite, 'on_animation_end'):
            self.sprite.on_animation_end()
        while saved:
            for element in saved:
                yield element
            if hasattr(self.sprite, 'on_animation_end'):
                self.sprite.on_animation_end()
    def stop(self):
        self.running = 0
        if self.idle_image:
            self.sprite.image = self.idle_image

    def start(self):
        if not self.running:
            self.running = 1
            self.cycle = self.cycle_func(self.frames)
            self.sprite.image = next(self.cycle)

    def update(self, dt):
        self.ticks += dt
        if self.ticks >= self.speed:
            self.ticks = self.ticks % self.speed
            if self.running:
                self.sprite.image = next(self.cycle)

class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, pos, frames, speed):
        super().__init__()
        self.animation = Animation(frames, speed, self)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.animation.start()

    def update(self, events, dt):
        self.animation.update(dt)

class Explosion(AnimatedSprite):

    frames = None

    def __init__(self, pos):
        if not Explosion.frames:
            Explosion.frames = parse_sprite_sheet(SPRITE_SHEET, pygame.Rect(0, 890, 64, 64), 6, 4)

        super().__init__(pos, Explosion.frames, 50)

    def on_animation_end(self):
        self.kill()

class DirectionalImageSprite(pygame.sprite.Sprite):

    directions = [(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(0,0)]

    def __init__(self, pos, directional_images_rect):
        super().__init__()
        images = parse_sprite_sheet(SPRITE_SHEET, directional_images_rect, 9, 1)
        self.images = { x: img for (x, img) in zip(DirectionalImageSprite.directions, images) }
        self.direction = Vector2(0, 0)
        self.image = self.images[(self.direction.x, self.direction.y)]
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos

class SpaceShip(DirectionalImageSprite):

    def __init__(self, pos, controller, directional_images_rect):
        super().__init__(pos, directional_images_rect)
        self.controller = controller
        self.speed = 3

    def update(self, events, dt):
        super().update(events, dt)

        if self.controller:
            self.controller.update(self, events, dt)

        self.image = self.images[(self.direction.x, self.direction.y)]
        if self.direction.length():
            self.pos = self.pos + self.direction.normalize() * self.speed

        self.rect.center = int(self.pos[0]), int(self.pos[1])

def parse_sprite_sheet(sheet, start_rect, frames_in_row, lines):
    frames = []
    rect = start_rect.copy()
    for _ in range(lines):
        for _ in range(frames_in_row):
            frame = sheet.subsurface(rect)
            frames.append(frame)
            rect.move_ip(rect.width, 0)
        rect.move_ip(0, rect.height)
        rect.x = start_rect.x
    return frames

def main():
    screen = pygame.display.set_mode((800, 600))
    global SPRITE_SHEET
    SPRITE_SHEET = pygame.image.load("ipLRR.png").convert_alpha()
    clock = pygame.time.Clock()
    dt = 0
    all_sprites = pygame.sprite.Group(
        SpaceShip((400, 300), PlayerController(), YELLOW_SHIP),
        SpaceShip((400, 100), EnemyController(), GREEN_SHIP)
    )

    while True:
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                return

        all_sprites.update(events, dt)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        dt = clock.tick(120)

main()