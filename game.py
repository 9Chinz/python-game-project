import pygame, sys, random, math, json
from pygame import Vector2
from spritesheet import SpriteSheet
from config import *
from ui import GameUI, OptionMenu

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.asset = pygame.image.load(PLAYER_SHIP).convert_alpha()
        self.sheet = SpriteSheet(self.asset, 16, 24)
        self.sprites = [self.sheet.get_img(3, x) for x in range(2)]
        self.current_sp = 0
        self.image = self.sprites[self.current_sp]
        self.rect = self.image.get_rect(midtop = (pos_x, pos_y))
    
    def update(self, speed):
        self.current_sp += speed
        if self.current_sp >= len(self.sprites):
            self.current_sp = 0
        self.image = self.sprites[int(self.current_sp)]


class SpaceObj:
    def __init__(self, pos_x, pos_y):
        self.pos = Vector2(pos_x, pos_y)
        self.direction = Vector2(0, 0)
    
    def update(self, speed):
        self.current_sp += speed
        if self.current_sp >= len(self.sprites):
            self.current_sp = 0
        self.image = self.sprites[int(self.current_sp)]


class Enemy(SpaceObj):
    def __init__(self, pos_x, pos_y, world_list, enemy_sprites, spr_width, spr_height):
        super().__init__(pos_x, pos_y)
        self.asset = pygame.image.load(enemy_sprites).convert_alpha()
        self.sheet = SpriteSheet(self.asset, spr_width, spr_height)
        self.sprites = [self.sheet.get_img(x, 0) for x in range(2)]
        self.current_sp = 0
        self.image = self.sprites[self.current_sp]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.velocity = 0.9
        self.original_word_list = world_list
        self.world_list = world_list
        self.user_input = ''
        self.word_font = pygame.font.Font(MINECRAFT_FONT, 24)
        self.get_lock = False
    
    def move(self):
        playerx, playery = WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.8
        dx = playerx - self.pos.x
        dy = playery - self.pos.y
        angle = math.atan2(dx, dy)
        velo_x = math.sin(angle)
        velo_y = math.cos(angle)
        self.pos += Vector2(velo_x * self.velocity, velo_y * self.velocity)
        self.rect = self.image.get_rect(center = self.pos)
        
    def draw(self, screen):
        self.update(0.2)
        self.move()
        if self.get_lock:
            color = ORANGE
        else:
            color = WHITE
        word_text = self.word_font.render(f"{self.world_list}", True, color)
        word_rect = word_text.get_rect(midtop = (self.rect.midbottom[0], self.rect.midbottom[1]+5))
        screen.blit(word_text, word_rect)
        screen.blit(self.image, self.rect)


class Bullet(SpaceObj):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.asset = pygame.image.load(LASER_BULLET).convert_alpha()
        self.sheet = SpriteSheet(self.asset, 16, 16)
        self.sprites = [self.sheet.get_img(x, 0) for x in range(2)]
        self.current_sp = 0
        self.image = self.sprites[self.current_sp]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.velocity = 50
    
    def draw(self, screen):
        self.update(0.2)
        screen.blit(self.image, self.rect)
        
    def shoot(self, pos):
        targetx, targety = pos.x, pos.y
        dx = targetx - self.pos.x
        dy = targety - self.pos.y
        angle = math.atan2(dx, dy)
        velo_x = math.sin(angle)
        velo_y = math.cos(angle)
        self.pos += Vector2(velo_x * self.velocity, velo_y * self.velocity)
        self.rect = self.image.get_rect(midtop = self.pos)


class ShipExplode(SpaceObj):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.asset = pygame.image.load(EXPLODE_EFFECT).convert_alpha()
        self.sheet = SpriteSheet(self.asset, 16, 16, 6)
        self.sprites = [self.sheet.get_img(x, 0) for x in range(5)]
        self.current_sp = 0
        self.image = self.sprites[self.current_sp]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    
    def draw(self, screen):
        if self.update(0.15):
            return True
        screen.blit(self.image, self.rect)
    
    def update(self, speed):
        self.current_sp += speed
        if self.current_sp >= len(self.sprites):
            return True
        self.image = self.sprites[int(self.current_sp)]
        

class Game():
    def __init__(self):        
        self.is_game_end = False
        self.background = pygame.image.load(BACKGROUND_IMG).convert_alpha()
        self.background = pygame.transform.scale(self.background, (256*4, 608*4))
        self.background_rect = self.background.get_rect()
        self.bg_y = self.background_rect.y
        self.option_menu = OptionMenu()
        self.game_ui = GameUI()
        self.is_pause = False
        self.heal = True
        self.current_time = pygame.time.get_ticks()
        self.word_dict = self.open_word_json()
        
        self.enemys = []
        self.enemy_amount = 0
        self.max_enemys = 4
        
        self.player_sp = pygame.sprite.Group()
        self.player = PlayerShip(WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.8)
        self.player_sp.add(self.player)
        
        self.lock_enemy = 0
        self.is_lock_on = False
        self.bullets = []
        self.shoot_music = pygame.mixer.Sound(LASER_SHOOT_SOUND)
        self.shoot_music.set_volume(EFFECT_VOLUME)
        self.high_score = self.get_score()
        
        self.count_kill = 0
        self.steak = 0
        self.level = 1
        
        self.explosion = []
        self.explode_sound = pygame.mixer.Sound(EXPLODE_SOUND)
        self.explode_sound.set_volume(EFFECT_VOLUME)
    
    def draw_background(self, screen):
        # return remain y
        rel_y = self.bg_y % self.background_rect.width
        screen.blit(self.background, (0, rel_y - self.background_rect.width))
        if rel_y < WINDOW_HEIGHT:
            screen.blit(self.background, (0, rel_y))
        # update screen
        self.bg_y += 1
    
    def game_pause(self, screen):
        while self.is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_pause = False
                        
            self.option_menu.draw(screen, self.game_ui.score)
            
            if self.option_menu.botton_resume.check_click():
                self.is_pause = False
            if self.option_menu.botton_exit.check_click():
                self.is_game_end = True
                self.is_pause = False
                
            pygame.display.update()
    
    def game_over(self, screen):
        while self.is_pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.option_menu.draw_game_over(screen, self.game_ui.score)
            if self.option_menu.botton_exit.check_click():
                if self.game_ui.score > self.high_score['high_score']:
                    self.high_score['high_score'] = self.game_ui.score
                    self.write_score(self.high_score)
                self.is_game_end = True
                self.is_pause = False
                
            pygame.display.update()
            
    def main(self, screen, mode):
        self.draw_background(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for index, enemy in enumerate(self.enemys):
                    if enemy.world_list:
                        if event.unicode == enemy.world_list[0] and not self.is_lock_on:
                            self.lock_enemy = index
                            self.is_lock_on = True
                            enemy.get_lock = True
                            break
                if self.is_lock_on:
                    char_typed = event.unicode
                    if self.enemys[self.lock_enemy].world_list:
                        if char_typed == self.enemys[self.lock_enemy].world_list[0]:
                            self.steak += 1
                            # shoot
                            self.shoot_music.play()
                            new_bullet = Bullet(WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.8)
                            self.bullets.append(new_bullet)  
                            self.enemys[self.lock_enemy].user_input += char_typed
                        else:
                            self.steak = 0
                            self.game_ui.multiplier_score = 1
                        
                if event.key == pygame.K_ESCAPE:
                    self.is_pause = True
        
        
        if self.enemy_amount < self.max_enemys and pygame.time.get_ticks() - self.current_time > 1500:
            self.current_time = pygame.time.get_ticks()
            self.enemy_amount += 1
            self.spawn_enemy(mode)
        if self.count_kill >= (6 * self.level):
            for index, enemy in enumerate(self.enemys):
                enemy.velocity += 0.2
            self.max_enemys += 1
            self.count_kill = 0
            self.level += 1
        if self.steak >= 5:
            self.game_ui.multiplier_score += 0.25
            self.steak = 0

        
        if self.heal:
            self.game_ui.health_amount += 2
        if self.game_ui.health_amount == self.game_ui.max_health:
            self.heal = False
        
        for index, enemy in enumerate(self.enemys):
            if self.player.rect.colliderect(enemy.rect):
                self.explosion.append(ShipExplode(self.player.rect.x, self.player.rect.y))
                self.explode_sound.play()
                self.steak = 0
                self.game_ui.multiplier_score = 1
                self.is_lock_on = False
                enemy.get_lock = False
                self.enemy_amount -= 1
                self.game_ui.health_amount -= DAMAGE   
                self.enemys.pop(index)     
            enemy.draw(screen)
            for index, bullet in enumerate(self.bullets):
                bullet.shoot(self.enemys[self.lock_enemy].pos)
                bullet.draw(screen)
                if bullet.rect.colliderect(enemy.rect) or (abs(bullet.rect.midtop[0] - enemy.rect.midbottom[0]) <= COLLISION_TOLERANCE and abs(bullet.rect.midtop[1] - enemy.rect.midbottom[1]) <= COLLISION_TOLERANCE):
                    self.enemys[self.lock_enemy].world_list = self.enemys[self.lock_enemy].world_list[1:]
                    if (self.enemys[self.lock_enemy].user_input == self.enemys[self.lock_enemy].original_word_list) or not enemy.world_list:
                        self.explosion.append(ShipExplode(self.enemys[self.lock_enemy].pos.x, self.enemys[self.lock_enemy].pos.y))
                        self.explode_sound.play()
                        self.enemy_amount -= 1
                        self.game_ui.score += 1 * self.game_ui.multiplier_score
                        self.count_kill += 1
                        self.enemys.pop(self.lock_enemy)
                        self.bullets.pop(index)
                        self.is_lock_on = False
                        self.enemys[self.lock_enemy].get_lock = False
                        self.lock_enemy = 0
                    else:
                        self.bullets.pop(index)
                    break
        
        for index, effect in enumerate(self.explosion):
            if effect.draw(screen):
                self.explosion.pop(index)
        
        self.player_sp.draw(screen)
        self.player_sp.update(0.2)
        self.game_ui.draw(screen)
        
        # pause game
        if self.game_ui.popup_botton.check_click():
            self.is_pause = True
        if self.game_ui.health_amount <= 0:
            self.is_pause = True
            self.game_over(screen)
        if self.is_pause:
            self.game_pause(screen)
        
        pygame.display.update()
    
    def spawn_enemy(self, mode):
        rand_word = self.random_word(self.word_dict, mode)
        rand_word_len = len(rand_word)
        if rand_word_len <= 3:
            spawn_enemy = ENEMY_SMALL
            enemy_spr_width = 16
            enemy_spr_height = 16
        elif rand_word_len <= 5:
            spawn_enemy = ENEMY_MEDIUM
            enemy_spr_width = 32
            enemy_spr_height = 16
        else:
            spawn_enemy = ENEMY_BIG
            enemy_spr_width = 32
            enemy_spr_height = 32
        enemy = Enemy(random.randrange(0, WINDOW_WIDTH), -50, rand_word, spawn_enemy, enemy_spr_width, enemy_spr_height)
        self.enemys.append(enemy)
        
    def reset(self):
        self.is_game_end = False
        self.heal = True
        self.enemys = []
        self.enemy_amount = 0
        self.max_enemys = 3
        self.steak = 0
        self.game_ui.health_amount = 0
        self.game_ui.multiplier_score = 1
        self.game_ui.score = 0
        self.is_lock_on = False
        self.explosion.clear()
        self.bullets.clear()
        self.enemys.clear()
        
    def open_word_json(self):
        with open('data/words.json') as json_file:
            json_data = json.load(json_file)
        return json_data['data']

    def random_word(self, word_dict, level):    
        type_word = ''
        while True:
            type_word = random.choice(word_dict)
            if (level == 'easy' and len(type_word) <= 5) or level == 'hard':
                break
        return type_word

    def get_score(self):
        try:
            with open('./data/score_board.json', 'r') as score:
                return json.load(score)
        except:
            return { "high_score" : 0}

    def write_score(self, data):
        with open('./data/score_board.json', 'w') as score:
            json.dump(data, score)