import pygame
import random
import math
import sys

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Polar")

clock = pygame.time.Clock()

# ================= IMAGENS =================

player_img_original = pygame.image.load("player3.png").convert_alpha()
player_img_original = pygame.transform.scale(player_img_original,(50,40))

enemy_img = pygame.image.load("enemy1.png").convert_alpha()
enemy_img = pygame.transform.scale(enemy_img,(32,24))

bullet_img = pygame.Surface((5,5))
bullet_img.fill((255,255,0))

# ================= SONS =================

shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
explosion_sound = pygame.mixer.Sound("sound/explosion.wav")

# ================= FONTES =================

font = pygame.font.Font(None,36)
big_font = pygame.font.Font(None,64)

# ================= ESTADOS =================

MENU="menu"
PLAYING="playing"
NIVELDOIS = "nível 2"
WIN="win"
LOSE="lose"
INSTRUCTION="instruction"

game_state = MENU

# ================= PLAYER =================

player_x = WIDTH//2
player_y = HEIGHT//2

player_angle = 0
rotation_speed = 2

# ================= BULLET =================

bullet_x = player_x
bullet_y = player_y

bullet_speed = 5
bullet_state = "ready"

bullet_dx = 0
bullet_dy = 0

# ================= ENEMIES =================

enemies=[]

def create_enemies():

    enemies.clear()

    rings=[140,190,240,290]
    counts=[5,7,10,14]

    ring_speeds=[0.002,0.004,-0.006,0.008]   # velocidade de cada círculo

    for r,n,speed in zip(rings,counts,ring_speeds):

        for i in range(n):

            theta=2*math.pi*i/n

            enemies.append({
                "r":r,
                "theta":theta,
                "speed":speed
            })

# ====== CRIACAO DOS INIMIGOS PARA A FASE 2 =======

def create_enemies2():

    enemies.clear()

    rings=[140,190,240,290]
    counts=[3,5,7,10]

    ring_speeds2=[0.004,-0.006,0.008,-0.010]   # velocidade de cada círculo

    for r,n,speed2 in zip(rings,counts,ring_speeds2):

        for i in range(n):

            theta=2*math.pi*i/n

            enemies.append({
                "r":r,
                "theta":theta,
                "speed2":speed2
            })


# ================= SCORE =================

score=0

def show_score():
    screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,10))

# ================= COLISAO =================

def collision(ex,ey,bx,by):
    return math.hypot(ex-bx,ey-by)<24

# ================= BOTAO COM ANIMACAO =================

def draw_button(text,x,y,w,h,click):

    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x,y,w,h)

    base_color = (70,70,200)
    hover_color = (100,100,255)
    press_color = (150,150,255)

    if rect.collidepoint(mouse):

        if click:
            pygame.draw.rect(screen,press_color,rect,border_radius=8)
            activated = True
        else:
            pygame.draw.rect(screen,hover_color,rect,border_radius=8)
            activated = False
    else:
        pygame.draw.rect(screen,base_color,rect,border_radius=8)
        activated = False

    pygame.draw.rect(screen,(255,255,255),rect,2,border_radius=8)

    label=font.render(text,True,(255,255,255))
    screen.blit(label,(x+w//2-label.get_width()//2,
                       y+h//2-label.get_height()//2))

    return activated

# ================= RESET =================

def reset_game():

    global bullet_state,score,player_angle

    bullet_state="ready"
    score=0
    player_angle=0

    create_enemies()

reset_game()

running=True

# ================= GAME LOOP =================

while running:

    click=False

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN:
            click=True

        if game_state==PLAYING:

            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_SPACE and bullet_state=="ready":

                    bullet_x=player_x
                    bullet_y=player_y

                    angle_rad = math.radians(player_angle)

                    bullet_dx = -bullet_speed * math.sin(angle_rad)
                    bullet_dy = -bullet_speed * math.cos(angle_rad)

                    bullet_state="fire"

                    shoot_sound.play()

        if game_state == NIVELDOIS:

            if event.type==pygame.KEYDOWN:

                if event.key==pygame.K_SPACE and bullet_state=="ready":

                    bullet_x=player_x
                    bullet_y=player_y

                    angle_rad = math.radians(player_angle)

                    bullet_dx = -bullet_speed * math.sin(angle_rad)
                    bullet_dy = -bullet_speed * math.cos(angle_rad)

                    bullet_state="fire"

                    shoot_sound.play()

    screen.fill((0,0,0))

    # ================= MENU =================

    if game_state==MENU:

        title=big_font.render("POLAR SPACE INVADERS",True,(255,255,255))
        screen.blit(title,(WIDTH//2-title.get_width()//2,150))

        if draw_button("Como Jogar",300,210,200,50,click):
            game_state=INSTRUCTION

        if draw_button("Iniciar Jogo",300,280,200,50,click):
            reset_game()
            game_state=PLAYING

        if draw_button("Sair",300,350,200,50,click):
            pygame.quit()
            sys.exit()

    # ================= JOGANDO =================

    elif game_state==PLAYING:

        keys=pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_angle += rotation_speed

        if keys[pygame.K_RIGHT]:
            player_angle -= rotation_speed

        rotated_player = pygame.transform.rotate(player_img_original,player_angle)
        rect = rotated_player.get_rect(center=(player_x,player_y))

        screen.blit(rotated_player,rect.topleft)

        if bullet_state=="fire":

            bullet_x += bullet_dx
            bullet_y += bullet_dy

            screen.blit(bullet_img,(bullet_x,bullet_y))

            if bullet_x<0 or bullet_x>WIDTH or bullet_y<0 or bullet_y>HEIGHT:
                bullet_state="ready"

        for enemy in enemies[:]:

            enemy["theta"] += enemy["speed"]
            enemy["r"] -= 0.05

            r=enemy["r"]
            theta=enemy["theta"]

            ex = player_x + r*math.cos(theta)
            ey = player_y + r*math.sin(theta)

            if r < 52:
                game_state = LOSE

            if bullet_state=="fire" and collision(ex,ey,bullet_x,bullet_y):

                explosion_sound.play()
                enemies.remove(enemy)
                bullet_state="ready"
                score += 10

            screen.blit(enemy_img,(ex,ey))

        show_score()

        if not enemies:
            game_state = NIVELDOIS
            create_enemies2()

 # ================= NIVEL 2 =================
    elif game_state == NIVELDOIS:

        bullet_img = pygame.Surface((3, 3))    # superfície da bala de 3 x 10 pixels
        bullet_img.fill((255, 255, 225))     # preenche toda a superfície com a branca (255,255,255).
        # bullet_dy = 0
        keys=pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_angle += rotation_speed

        if keys[pygame.K_RIGHT]:
            player_angle -= rotation_speed

        rotated_player = pygame.transform.rotate(player_img_original,player_angle)
        rect = rotated_player.get_rect(center=(player_x,player_y))

        screen.blit(rotated_player,rect.topleft)

        if bullet_state=="fire":

            if keys[pygame.K_LEFT]:
                bullet_x += bullet_dx - 3
                bullet_y += bullet_dy
                screen.blit(bullet_img,(bullet_x,bullet_y))

            elif keys[pygame.K_RIGHT]:
                bullet_x += bullet_dx + 3
                bullet_y += bullet_dy
                screen.blit(bullet_img,(bullet_x,bullet_y))

            else:
                bullet_x += bullet_dx
                bullet_y += bullet_dy
                screen.blit(bullet_img,(bullet_x,bullet_y))

            if bullet_x<0 or bullet_x>WIDTH or bullet_y<0 or bullet_y>HEIGHT:
                bullet_state="ready"

        for enemy in enemies[:]:

            enemy["theta"] += enemy["speed2"]
            enemy["r"] -= 0.1

            r=enemy["r"]
            theta=enemy["theta"]

            ex = player_x + r*math.cos(theta)
            ey = player_y + r*math.sin(theta)

            if r < 52:
                game_state = LOSE

            if bullet_state=="fire" and collision(ex,ey,bullet_x,bullet_y):

                explosion_sound.play()
                enemies.remove(enemy)
                bullet_state="ready"
                score += 25

            screen.blit(enemy_img,(ex,ey))

        show_score()

        if not enemies:
            game_state = WIN


    # ================= COMO JOGAR =================

    elif game_state==INSTRUCTION:

        text=big_font.render("APERTE O ESPAÇO PARA ATIRAR",True,(0,255,0))
        screen.blit(text,(WIDTH//15-text.get_width()//20,150))

        text=big_font.render("APERTE A SETA PARA ESQUERDA",True,(255,0,0))
        screen.blit(text,(WIDTH//15-text.get_width()//20,250))
        text=big_font.render("OU DIREITA PARA GIRAR A NAVE",True,(255,0,0))
        screen.blit(text,(WIDTH//15-text.get_width()//20,350))

        if draw_button("Menu",280,400,240,50,click):
            game_state=MENU

    # ================= WIN =================

    elif game_state==WIN:

        text=big_font.render("YOU WIN!",True,(0,255,0))
        screen.blit(text,(WIDTH//2-text.get_width()//2,150))

        show_score()

        if draw_button("Jogar Novamente",280,300,240,50,click):
            reset_game()
            game_state=PLAYING

        if draw_button("Menu",280,370,240,50,click):
            game_state=MENU

    # ================= LOSE =================

    elif game_state==LOSE:

        text=big_font.render("YOU LOSE!",True,(255,50,50))
        screen.blit(text,(WIDTH//2-text.get_width()//2,150))

        show_score()

        if draw_button("Jogar Novamente",280,300,240,50,click):
            reset_game()
            game_state=PLAYING

        if draw_button("Menu",280,370,240,50,click):
            game_state=MENU

    pygame.display.update()
    clock.tick(60)
