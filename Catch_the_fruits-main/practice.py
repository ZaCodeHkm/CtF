import pygame,random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Practice")

#Define FPS
FPS = 60
clock = pygame.time.Clock()


"""A class to define gameplay and launching entire game"""
class Game():

    """Pull player and fruits group and initialize it"""
    def __init__(self , player , fruits_group):
        self.score = 0
        self.round_catch = 8
        self.round_time = 60 # 60s for the first round
        self.round_level = 1
        self.frame_count = 0 # To count frame time 
        self.total_catch = 0

        self.player = player
        self.fruits_group = fruits_group

        self.font = pygame.font.Font("Facon.ttf" , 20)

        #Define fruits variable
        apple = "apple.png"
        banana = "banana.png"
        lemon = "lemon.png"
        strawberry = "strawberry.png"

        self.fruits_list = [apple , banana , lemon , strawberry]
        self.target_new_fruit = random.randint(0 , 3)


        """Target the first fruit first"""
        self.targeted_fruit = self.fruits_list[self.target_new_fruit]
        self.targeted_fruit_image = pygame.image.load(self.targeted_fruit)
    
    """A method to update the gameplay"""
    def update(self):
        
        self.check_game_status()

    """A method to draw neccessary component to the screen"""
    def draw(self):

        WHITE = (255 , 255 , 255)
        GREEN = (64, 241, 64)
        YELLOW = (225, 241, 64)
        PINK = (220, 64, 241)
        RED = (241, 64, 64)

        color = [GREEN , YELLOW , PINK , RED]

        score_text = self.font.render(f"Score: {self.score}" , True , WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (1 , 1)

        total_catch = self.font.render(f"Total catch: {self.total_catch}" , True , WHITE)
        total_catch_rect = total_catch.get_rect()
        total_catch_rect.topleft = (1 , 30)

        round_level = self.font.render(f"Round level: {self.round_level}" , True , WHITE)
        round_level_rect = round_level.get_rect()
        round_level_rect.topleft = (1 , 60)

        lives_text = self.font.render(f"Lives: {self.player.lives}" , True , WHITE)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (1 , 90)

        current_catch_text = self.font.render("Current catch" , True , WHITE)
        current_catch_text_rect = current_catch_text.get_rect()
        current_catch_text_rect.topleft = (1 , 120)

        time_text = self.font.render(f"Time: {self.round_time}" , True , WHITE)
        time_text_rect = time_text.get_rect()
        time_text_rect.topleft = (1 , 250)

        self.fruit_image = self.targeted_fruit_image.get_rect()
        self.fruit_image.topleft = (10 , 155)


        display_surface.blit(score_text , score_text_rect)
        display_surface.blit(total_catch , total_catch_rect)
        display_surface.blit(round_level , round_level_rect)
        display_surface.blit(lives_text , lives_text_rect)
        display_surface.blit(current_catch_text , current_catch_text_rect)
        display_surface.blit(self.targeted_fruit_image , self.fruit_image)
        display_surface.blit(time_text , time_text_rect)

        pygame.draw.rect(display_surface , color[self.target_new_fruit] , (10 , 150 , 68 , 68) , 3)
        pygame.draw.rect(display_surface , color[self.target_new_fruit] , (230 , 1 , WINDOW_WIDTH - 230 , WINDOW_HEIGHT) , 3)

    def start_new_round(self):
        pass

    """To randomly choose a new target"""
    def choose_new_target(self):
        self.target_new_fruit = random.randint(0,3)
        self.targeted_fruit = self.fruits_list[self.target_new_fruit]
        self.targeted_fruit_image = pygame.image.load(self.targeted_fruit)

    """Check the gameplay status , winning condition and losing condition"""
    def check_game_status(self):
        
        if len(self.fruits_group) == 0:
            self.spawn_new_fruits()

    """Check is the player complete the round"""
    def check_round_completion(self):
        pass

    """A method to pause the game whenever is call"""
    def paused_game(self):
        pass
    
    """To detect if player hit a fruit"""
    def hit_fruit(self):
        collide_fruit = pygame.sprite.spritecollideany(self.player , self.fruits_group)

        if collide_fruit:

            if collide_fruit.fruit_type == self.target_new_fruit:
                
                collide_fruit.remove(self.fruits_group)
                self.choose_new_target()

    def spawn_new_fruits(self):
        """clear the fruits list first"""
        for fruit in self.fruits_group:
            self.fruits_group.remove(fruit)

        """Add all the fruits into list"""
        for i in range(self.round_level):
            self.fruits_group.add(Fruit(random.randint(294 , WINDOW_WIDTH-10) , -random.randint(100 , 200) , "apple.png" , 0))
            self.fruits_group.add(Fruit(random.randint(294 , WINDOW_WIDTH-10) , -random.randint(100 , 200) , "banana.png" , 1))
            self.fruits_group.add(Fruit(random.randint(294 , WINDOW_WIDTH-10) , -random.randint(100 , 200) , "lemon.png" , 2))
            self.fruits_group.add(Fruit(random.randint(294 , WINDOW_WIDTH-10) , -random.randint(100 , 200) , "strawberry.png" , 3))

    def reset_game(self):
        pass


class Fruit(pygame.sprite.Sprite):

    def __init__(self , x , y , image , fruit_type):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)

        self.fruit_type = fruit_type
        self.velocity = random.randint(3 , 5)
        self.buffer_distance = 2
        self.random_direction = random.choice([-1,1])

    def update(self):
        self.rect.y += self.velocity

        self.move_horizontally()

        if self.rect.bottom > WINDOW_HEIGHT:
            self.kill()

    """To move the x-axis at a certain y axis degree"""
    def move_horizontally(self):
        if self.rect.bottom > WINDOW_HEIGHT // 2 + 100:
            if self.rect.left > 294 and self.rect.right < WINDOW_WIDTH - 10:
                self.rect.x += self.buffer_distance * self.random_direction



                

                




class Player(pygame.sprite.Sprite):

    def __init__(self):
        """Initialize everything"""

        """To inherit value from sprite library using 'super' method"""
        super().__init__()

        """Define default value"""
        self.monkey_image = "monkey.png"
        self.wrong_monkey_image = "wrong_monkey.png"
        self.image = pygame.image.load(self.monkey_image)
        self.rect = self.image.get_rect()
        self.rect.center = (WINDOW_WIDTH // 2 + 100 , WINDOW_HEIGHT - 32)
        self.lives = 5

        self.velocity = 8

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 235:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def reset_position(self):
        self.rect.center = (WINDOW_WIDTH // 2 + 100 , WINDOW_HEIGHT - 32)



my_player_group = pygame.sprite.Group()
player = Player()
my_player_group.add(player)

my_fruits_group = pygame.sprite.Group()

my_game = Game(player , my_fruits_group)
my_game.spawn_new_fruits()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_game.hit_fruit()

    display_surface.fill((0,0,0))

    # This also a default method but I override already
    my_player_group.update()
    # This is a default method in Sprite library to draw , you have to place in our surface as parameter
    my_player_group.draw(display_surface)

    
    my_fruits_group.update()
    my_fruits_group.draw(display_surface)
    
    my_game.update()
    my_game.draw()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()