#!/usr/bin/python3
import pygame as PG;
import random as RN;

### Константи
#Встановлюємо висоту і ширину екрану
SCREEN_HEIGHT = 768;
SCREEN_WIDTH = 1376;

#фон екрану
SCREEN_BACKGROUND = PG.transform.scale(PG.image.load("images/background.png"), (SCREEN_WIDTH,SCREEN_HEIGHT));

#Встановлюємо розміри гравця (фігури-поверхні)
PLAYER_HEIGHT = 50;
PLAYER_WIDTH = 50;

#Встановлюємо розміри ворога
ENEMY_HEIGHT = 30;
ENEMY_WIDTH = 60;

#діапазон екрану по вертикалі де будуть появлятися вороги
ENEMY_DIAPASON = [60,700]

#Встановлюємо розміри бонусу
BONUS_HEIGHT = 70;
BONUS_WIDTH = 70;

#розміри контейнера очок прогресу
SCORE_BACKGROUND_WIDTH = 60;
SCORE_BACKGROUND_HEIGHT = 40;


#Встановлюємо кольори в hex
WINDOW_COLOR = "#000000"; #колір вікна
PLAYER_COLOR = "#ffffff"; #колір фігури
ENEMY_COLOR = "#ff0000"; #колір ворога
BONUS_COLOR = "#ffff00"; #колір бонусу
SCORE_BACKGROUND_COLOR = "#f9f06b"; #колір фону тексту очок прогресу гри
SCORE_FONT_COLOR = "#3d3846" #Колір тексту очок прогресу гри

#Початкове положення фігури
PLAYER_X = 0;
PLAYER_Y = 350;

#швидкість пересування по області гри
PLAYER_WAY_RIGHT = [6,0];
PLAYER_WAY_LEFT = [-6,0];
PLAYER_WAY_TOP = [0,-6];
PLAYER_WAY_BOTTOM = [0,6];
ENEMY_SPEED_RANGE = [-10,-5];
BONUS_SPEED_RANGE = [5,8];
SCREEN_BACKGROUND_SPEED = 2; #швидкість руху бекграунду

#час випадання бонусу для рандома
BONUS_APPEARENCE_RANGE = [5,7];

#час появлення ворога для рандома
ENEMY_APPEARENCE_RANGE = [2,4];

#FPS
FPS = 500;

#Шрифт для рахунку бонусів
PG.font.init();
SCORE_FONT = PG.font.SysFont("Verdana",30);

#USEREVENT появи ворога
ENEMY_CREATE = PG.USEREVENT + 1;
#USEREVENT появи бонусу
BONUS_CREATE = PG.USEREVENT + 2;



### Змінні
#Встановлюємо прапопець роботи циклу гри
playing = True;
#рахунок гри
score = 0;
#рендерим перший текст рахунку
bonus_text = SCORE_FONT.render(str(score),True,PG.Color(SCORE_FONT_COLOR));
#лічильник для позиції бекграунда
bg_counter = 0;

###Функції
#обнова таймера для події
def set_timer_event(event,ms):
    PG.time.set_timer(event,ms);
    return None;

#додавання ворога
def create_enemy (x,y,speed):
    #Створюємо фігуру ворога
    enemy = PG.Surface((ENEMY_WIDTH,ENEMY_HEIGHT));
    PG.draw.rect(enemy,PG.Color(ENEMY_COLOR),PG.Rect(0,0,ENEMY_WIDTH,ENEMY_HEIGHT));
    enemy_rect = enemy.get_rect();
    enemy_rect.x = x;
    enemy_rect.y = y;
    return {"enemy":enemy,"enemy_rect":enemy_rect, "speed":speed};

#додавання бонусу
def create_bonus(x,y,speed):
    #Створюємо фігуру бонусу
    bonus = PG.Surface((BONUS_WIDTH,BONUS_HEIGHT));
    PG.draw.rect(bonus,PG.Color(BONUS_COLOR),PG.Rect(0,0,BONUS_WIDTH,BONUS_HEIGHT));
    bonus_rect = bonus.get_rect();
    bonus_rect.x = x;
    bonus_rect.y = y;
    return {"bonus":bonus,"bonus_rect":bonus_rect, "speed":speed};

### Код
#Ініціалізуємо pygame
PG.init();

#ініціалізуємо головне вікно гри
main_display = PG.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),vsync=1);
#Встановлюємо заголовок вікна
PG.display.set_caption('Моя перша гра на Пайтон');

#Створюємо фігуру-гравця - квадрат;
player = PG.Surface((PLAYER_WIDTH, PLAYER_HEIGHT));
#player = PG.image.load("images/player.png");
player_rect = player.get_rect(topleft=(PLAYER_X, PLAYER_Y));
#Малюємо круг в центрі фігури-гравця (об'єкт player, (колір,колір,колір), (координати центру,координати центру), радіус)
#Потім буде замінено на іконку гравця
PG.draw.circle(player, PG.Color(PLAYER_COLOR), (PLAYER_WIDTH/2, PLAYER_HEIGHT/2), PLAYER_HEIGHT/2-1);

#фігура для прогресу
score_container = PG.Surface((SCORE_BACKGROUND_WIDTH,SCORE_BACKGROUND_HEIGHT));
score_container.fill(PG.Color(SCORE_BACKGROUND_COLOR));
score_container_rect = score_container.get_rect(topright=(SCREEN_WIDTH,0));


#Ініціалізуємо таймер для першого ворога
set_timer_event(ENEMY_CREATE,RN.randint(*ENEMY_APPEARENCE_RANGE) * 1000);
#Ініціалізуємо таймер для першого бонусу
set_timer_event(BONUS_CREATE,RN.randint(*BONUS_APPEARENCE_RANGE) * 1000);
enemies = [];
bonuses = [];


#головний цикл програми
while playing:

    #Заповнюємо фон вікна рухаючимся бекграундом
    main_display.blit(SCREEN_BACKGROUND,(bg_counter,0))
    main_display.blit(SCREEN_BACKGROUND,(SCREEN_WIDTH + bg_counter,0))
    if bg_counter == -SCREEN_WIDTH:
        main_display.blit(SCREEN_BACKGROUND,(SCREEN_WIDTH + bg_counter,0))
        bg_counter = 0;
    bg_counter -= 2;


    #Додаємо фігуру-гравця на вікно програми
    main_display.blit(player, player_rect);
    

    #Ловимо події на натискання клавіш стрілок руху гравця-фігури
    key_pressed = PG.key.get_pressed();

    #Натистуна клавіша "стрілка вверх" - гравець-фігура пересувається вверх області екрану але не вище 0 по Y
    if key_pressed[PG.K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(PLAYER_WAY_TOP);
    #Натистуна клавіша "стрілка вниз" - гравець-фігура пересувається вниз області екрану але не нижче SCREEN_HEIGHT по Y
    if key_pressed[PG.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
        player_rect = player_rect.move(PLAYER_WAY_BOTTOM);
    #Натистуна клавіша "стрілка вліво" - гравець-фігура пересувається вліво області екрану але не лівіше 0 по X
    if key_pressed[PG.K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(PLAYER_WAY_LEFT);
    #Натистуна клавіша "стрілка вправо" - гравець-фігура пересувається вправо області екрану але не правіше SCREEN_WIDTH по X
    if key_pressed[PG.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect = player_rect.move(PLAYER_WAY_RIGHT);
    


    #Ловим події виходу з гри На хрестик і Ескейп
    for event in PG.event.get():
        match event.type:
            case PG.QUIT:
                playing = False;
            case PG.KEYDOWN:
                match event.key:
                    case PG.K_ESCAPE:
                        playing = False;
        #добавляємо нового ворога якщо їх не більше 4 на екрані
        if event.type == ENEMY_CREATE and len(enemies) < 5:
            enemies.append(create_enemy(SCREEN_WIDTH + ENEMY_WIDTH, RN.randint(*ENEMY_DIAPASON), [RN.randint(*ENEMY_SPEED_RANGE),0]));
            #оновлюємо час випадіння ворога
            set_timer_event(ENEMY_CREATE,RN.randint(*ENEMY_APPEARENCE_RANGE) * 1000);

        #добавляємо нового бонусу якщо їх немає
        if event.type == BONUS_CREATE and len(bonuses) < 1:
            bonuses.append(create_bonus(RN.randint(BONUS_WIDTH,SCREEN_WIDTH - BONUS_WIDTH), 0, [0,RN.randint(*BONUS_SPEED_RANGE)]));
            #оновлюємо час випадіння нового бонусу
            set_timer_event(BONUS_CREATE,RN.randint(*BONUS_APPEARENCE_RANGE) * 1000);
    
    #запускаємо ворогів на екран
    for enemy in enemies:
        main_display.blit(enemy["enemy"],enemy["enemy_rect"]);
        enemy["enemy_rect"] = enemy["enemy_rect"].move(enemy["speed"]);
        #видаляємо ворога коли він пролетів екран)
        if enemy["enemy_rect"].right <= 0:
            enemies.pop(enemies.index(enemy));
        #фіксуємо удар ворога по гравцю
        if player_rect.colliderect(enemy["enemy_rect"]):
            print ("BOOM");
    
    #запускаємо бонуси на екран
    for bonus in bonuses:
        main_display.blit(bonus["bonus"],bonus["bonus_rect"]);
        bonus["bonus_rect"] = bonus["bonus_rect"].move(bonus["speed"]);
        #видаляємо бонус коли він пролетів екран)
        if bonus["bonus_rect"].top >= SCREEN_HEIGHT:
            bonuses.pop(bonuses.index(bonus));
        #фіксуємо удар бонусу по гравцю
        if player_rect.colliderect(bonus["bonus_rect"]):
            score += 1;
            #оновлюємо текст прогресу гри
            bonus_text = SCORE_FONT.render(str(score),True,PG.Color(SCORE_FONT_COLOR));
            #затираємо старий текст прогресу гри
            score_container.fill(PG.Color(SCORE_BACKGROUND_COLOR));
            bonuses.pop(bonuses.index(bonus));  
            

    #додаємо контейнер рахунку гри на головне вікно - тут з самого низу щоб було поверх всіх
    main_display.blit(score_container,score_container_rect);
    #отримуємо контейнер тексту і відцентровуємо в предку
    bonus_text_rect = bonus_text.get_rect(center = score_container.get_rect().center);
    score_container.blit(bonus_text,bonus_text_rect);
    PG.time.Clock().tick(FPS);
    PG.display.update(main_display.get_rect());
