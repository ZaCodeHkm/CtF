import pygame,random,sys

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Catch the fruits")

FPS = 60
clock = pygame.time.Clock()

# Define classes
class Game():
    """To control gameplay and launch"""
    def __init__(self , player , fruit_group, powerup_group):
        """ Initialize """
        self.round_catch = 0
        self.round_target = 7
        self.round_level = 1
        self.round_fruits = 2
        self.score = 0
        self.round_time = 20
        self.round_count = self.round_time
        self.frame_count = 0

        self.font = pygame.font.Font("Facon.ttf" , 20)

        self.player = player
        self.fruit_group = fruit_group
        self.powerup_group = powerup_group

        # Set fruits images
        apple = pygame.image.load("apple.png")
        banana = pygame.image.load("banana.png")
        lemon = pygame.image.load("lemon.png")
        strawberry = pygame.image.load("strawberry.png")

        self.target_fruits_images = [apple , banana , lemon , strawberry]
        self.target_fruit_type = random.randint(0 , 3)

        self.target_fruit_image = self.target_fruits_images[self.target_fruit_type]

        # set power up images
        melon = pygame.image.load('melon.png')
        self.powerup_images = [melon]
        self.powerup_type = 0

        

    def update(self):
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time -= 1
            self.frame_count = 0

        self.check_game_status()
        self.check_game_completion()
    
    def draw(self):
        """Blit HUD"""
        WHITE = (255 , 255 , 255)
        YELLOW = (229, 254, 49)
        RED = (254, 49, 49)
        PINK = (242, 49, 254)
        GREEN = (84, 255, 46)

        colors = [GREEN , YELLOW , PINK , RED]

        score_text = self.font.render(f"Score: {self.score}" , True , WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (1 , 1)

        catch_text = self.font.render(f"Total catch: {self.round_catch}" , True , WHITE)
        catch_text_rect = catch_text.get_rect()
        catch_text_rect.topleft = (1 , 30)

        catch_target_text = self.font.render(f"Total target catch:{self.round_target}" , True , WHITE)
        catch_target_text_rect = catch_target_text.get_rect()
        catch_target_text_rect.topleft = (1 , 60)

        round_level_text = self.font.render(f"Round level: {self.round_level}" , True , WHITE)
        round_level_text_rect = round_level_text.get_rect()
        round_level_text_rect.topleft = (1 , 90)

        lives_text = self.font.render(f"Lives: {self.player.lives}" , True , WHITE)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (1 , 120)
        
        current_catch = self.font.render("Current catch" , True , WHITE)
        current_catch_rect = current_catch.get_rect()
        current_catch_rect.topleft = (1 , 150)

        fruit_image = self.target_fruit_image
        fruit_image_rect = fruit_image.get_rect()
        fruit_image_rect.topleft = (20 , 203)

        round_time = self.font.render(f"Round Time: {self.round_time}s" , True , WHITE)
        round_time_rect = round_time.get_rect()
        round_time_rect.topleft = (1 , 300)

        display_surface.blit(score_text , score_text_rect)
        display_surface.blit(catch_text , catch_text_rect)
        display_surface.blit(lives_text , lives_text_rect)
        display_surface.blit(round_time , round_time_rect)
        display_surface.blit(catch_target_text , catch_target_text_rect)
        display_surface.blit(round_level_text , round_level_text_rect)
        display_surface.blit(current_catch , current_catch_rect)
        display_surface.blit(fruit_image , fruit_image_rect)

        pygame.draw.rect(display_surface , colors[self.target_fruit_type] , (300 , 1 , WINDOW_WIDTH - 300 , WINDOW_HEIGHT) , 2)
        pygame.draw.rect(display_surface , colors[self.target_fruit_type] , (20 , 200 , 66 , 66) , 2)


    
    def hit_fruit(self):
         collide_fruit = pygame.sprite.spritecollideany(self.player , self.fruit_group)

         if collide_fruit:
             self.player.image = pygame.image.load("monkey.png")
             self.player.rect = self.player.image.get_rect()
             self.player.rect.centerx = WINDOW_WIDTH // 2 + 100
             self.player.rect.bottom = WINDOW_HEIGHT
            
             if collide_fruit.fruit_type == self.target_fruit_type:

                 self.score += 100
                 self.round_catch += 1

                 collide_fruit.remove(self.fruit_group)
                 self.player.movement = "normal"
                 self.player.image = pygame.image.load(self.player.monkey_image)
                 self.choose_new_target()
             else:
                 self.player.lives -= 1
                 self.player.movement = "normal"
                 self.player.image = pygame.image.load(self.player.wrong_monkey_image)
                 self.choose_new_target()

    def hit_powerup(self):
        collide_powerup = pygame.sprite.spritecollideany(self.player , self.powerup_group)

        #melon = net power
        if collide_powerup:
                if collide_powerup.powerup_type == 0:
                            self.player.image = pygame.image.load("monkeybasketbig.png")
                            self.player.rect = self.player.image.get_rect()
                            self.player.rect.centerx = WINDOW_WIDTH//2 + 50
                            self.player.rect.bottom = WINDOW_HEIGHT
                            self.player.movement = "normal"
                            self.player.power_status = 1

                if collide_powerup.powerup_type == 1:
                        self.player.movement = "normal"
                        self.round_time += 10

                if collide_powerup.powerup_type == 2:
                     self.player.movement = "inverse"
            

    def start_new_round(self):

        self.paused_game(f"Round level: {self.round_level}" , "Press 'Enter' to start , press 'SPACE_BAR' to catch")

        self.spawn_the_fruits()
        self.spawn_powerup()

    
    def paused_game(self , main_text , sub_text):
        
        WHITE = (255 , 255 , 255)
        BLACK = (0 , 0 , 0)

        main_text = self.font.render(main_text , True , WHITE)
        main_text_rect = main_text.get_rect()
        main_text_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2)

        sub_text = self.font.render(sub_text , True , WHITE)
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (WINDOW_WIDTH // 2 , WINDOW_HEIGHT // 2 + 50)

        display_surface.fill(BLACK)
        display_surface.blit(main_text , main_text_rect)
        display_surface.blit(sub_text , sub_text_rect)

        pygame.display.update()

        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False


    def reset_game(self):
        self.round_level = 1
        self.frame_count = 0
        self.round_time = 60
        self.score = 0
        self.player.lives = 5
        self.round_catch = 0
        self.round_target = 8
        self.round_fruits = 2
        self.player.reset_position()

        for fruit in self.fruit_group:
            self.fruit_group.remove(fruit)



    def check_game_status(self):
        
        """If player exceeds the amount of time given or lives to 0 , player lost"""
        if self.round_time == 0 or self.player.lives == 0:
            self.paused_game(f"Final score: {self.score} , run out of time or lives" , "Press 'Enter' to play again")
            self.reset_game()
        
        """If all the fruits has done , respawn the fruits"""
        if len(self.fruit_group) >= 0 and len(self.fruit_group) <= 7:
            self.spawn_the_fruits()
            self.spawn_powerup()




    def check_game_completion(self):

        """Check the player has done catching all the fruits"""
        if self.round_catch == self.round_target:
            self.paused_game(f"Score: {self.score} , You clear level {self.round_level}" , "Press 'Enter' to continue~ ")
            self.round_level += 1
            self.score += 100 * self.round_time
            self.round_time = self.round_count * self.round_level
            self.round_target += self.round_target
            self.round_catch = 0
            self.round_fruits = self.round_fruits * self.round_level
            self.player.movement = "normal"
            """Remove all the fruits first otherwise overlapping"""
            for fruit in self.fruit_group:
                self.fruit_group.remove(fruit)
            self.start_new_round()



    def spawn_the_fruits(self):

        """Add the fruits into the group"""
        for i in range(self.round_fruits):
                apple = Fruits(random.randint(301 , WINDOW_WIDTH - 64) , random.randint(10 , 200) * -1 , pygame.image.load("apple.png") , 0)
                banana = Fruits(random.randint(301 , WINDOW_WIDTH - 64) , random.randint(10 , 200) * -1 , pygame.image.load("banana.png") , 1)
                lemon = Fruits(random.randint(301 , WINDOW_WIDTH - 64) , random.randint(10 , 200) * -1 , pygame.image.load("lemon.png") , 2)
                strawberry = Fruits(random.randint(301 , WINDOW_WIDTH - 64) , random.randint(10 , 200) * -1 , pygame.image.load("strawberry.png") , 3)

                self.fruit_group.add(apple)
                self.fruit_group.add(banana)
                self.fruit_group.add(lemon)
                self.fruit_group.add(strawberry)


    def spawn_powerup(self):
        
        for i in range(1):
            melon = PowerUp(random.randint(301 , WINDOW_WIDTH - 64) , -random.randint(10 , 200) , pygame.image.load("melon.png") , 0)
            gold = PowerUp(random.randint(301 , WINDOW_WIDTH - 64) , -random.randint(10 , 200) , pygame.image.load("gold.jpeg") , 1)
            silver_mask = PowerUp(random.randint(301 , WINDOW_WIDTH - 64) , -random.randint(10 , 200) , pygame.image.load("silver_mask.jpeg") , 2)

            self.powerup_group.add(melon)
            self.powerup_group.add(gold)
            self.powerup_group.add(silver_mask)



    def choose_new_target(self):
        self.target_fruit_type = random.randint(0 , 3)
        self.target_fruit_image = self.target_fruits_images[self.target_fruit_type]


class Fruits(pygame.sprite.Sprite):

    def __init__(self , x , y , image , fruit_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        self.velocity = random.randint(4 , 5)
        self.fruit_type = fruit_type
        self.buffer_distance = 2
        self.random_direction = random.choice([-1,1])

    def update(self):
        self.rect.y += self.velocity

        self.bouncing()

        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()


    """To make the fruits' bounce and move around"""
    def bouncing(self):
        if self.rect.bottom > 50:
            if self.rect.left > 290 and self.rect.right < WINDOW_WIDTH + 10:
                self.rect.x += self.buffer_distance * self.random_direction
            if self.rect.left < 301:
                self.random_direction *= -1
                self.rect.x += self.buffer_distance * 5
            if self.rect.right > WINDOW_WIDTH - 10:
                self.random_direction *= -1
                self.rect.x += self.buffer_distance * -5


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.monkey_image = "monkey.png"
        self.wrong_monkey_image = "wrong_monkey.png"
        self.image = pygame.image.load(self.monkey_image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2 + 100
        self.rect.bottom = WINDOW_HEIGHT
        self.movement = "normal"
        self.power_status = 0

        self.velocity = 8
        self.lives = 5

    def update(self):
         keys = pygame.key.get_pressed()

         if self.movement == "normal":

            if keys[pygame.K_LEFT] and self.rect.left > 300:
                if self.power_status == 1:
                    self.rect.x -= self.velocity
                else:
                    self.image = pygame.image.load(self.monkey_image)
                    self.rect.x -= self.velocity

            if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
                if self.power_status == 1:
                    self.rect.x += self.velocity
                    print(self.rect.x)
                else:
                    self.image = pygame.image.load(self.monkey_image)
                    self.rect.x += self.velocity

         elif self.movement == "inverse":

            if keys[pygame.K_LEFT] and self.rect.left > 300 and self.rect.right < WINDOW_WIDTH:
                self.rect.x += self.velocity


                if self.rect.left <= 300:
                    self.rect.x = 320
                if self.rect.right >= 980:
                    self.rect.x = 890

            if keys[pygame.K_RIGHT] and self.rect.left > 300 and self.rect.right < WINDOW_WIDTH:
                self.rect.x -= self.velocity

                if self.rect.left <= 300:
                    self.rect.x = 320
                if self.rect.right >= 980:
                    self.rect.x = 890
    
    def reset_position(self):
        self.rect.centerx = WINDOW_WIDTH // 2 + 100
        self.rect.bottom = WINDOW_HEIGHT

class PowerUp(pygame.sprite.Sprite):

    def __init__(self , x , y , image , powerup_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        self.velocity = random.randint(6,7)
        self.powerup_type = powerup_type
        self.buffer_distance = 2
        self.random_direction = random.choice([-1,1])
        self.activepowerup = 0

    def update(self):
        self.rect.y += self.velocity

        self.bouncing()

        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()


    """To make the fruits' bounce and move around"""
    def bouncing(self):
        if self.rect.bottom > 50:
            if self.rect.left > 290 and self.rect.right < WINDOW_WIDTH + 10:
                self.rect.x += self.buffer_distance * self.random_direction
            if self.rect.left < 301:
                self.random_direction *= -1
                self.rect.x += self.buffer_distance * 5
            if self.rect.right > WINDOW_WIDTH - 10:
                self.random_direction *= -1

my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)


my_fruits_group = pygame.sprite.Group()

my_powerup_group = pygame.sprite.Group()

my_game = Game(my_player , my_fruits_group, my_powerup_group)
my_game.start_new_round()



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_game.hit_fruit()
                my_game.hit_powerup()

    display_surface.fill((0,0,0))

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_fruits_group.update()
    my_fruits_group.draw(display_surface)

    my_powerup_group.update()
    my_powerup_group.draw(display_surface)

    my_game.update()
    my_game.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()