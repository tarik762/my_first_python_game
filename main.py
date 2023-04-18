#!/usr/bin/python3
import pygame as PG;
import random as RN;

### Константи
#Встановлюємо висоту і ширину екрану
HEIGHT_SCREEN = 768;
WIDTH_SCREEN = 1024;

#Встановлюємо розміри гравця (фігури-поверхні)
HEIGHT_PLAYER = 50;
WIDTH_PLAYER = 50;

#Встановлюємо кольори в hex
WINDOW_COLOR = "#000000"; #колір вікна
PLAYER_COLOR = "#ffffff"; #колір фігури

#Початкове положення фігури
PLAYER_X = 0;
PLAYER_Y = 350;

#швидкість
PLAYER_WAY_RIGHT = [3,0];
PLAYER_WAY_LEFT = [-3,0];

#FPS
FPS = 240;


### Змінні
#Встановлюємо прапопець роботи циклу гри
playing = True;
way_left = True;

### Код
#Ініціалізуємо pygame
PG.init();
#Створюємо фігуру-гравця і заповнюємо її кольором;
player = PG.Surface((WIDTH_PLAYER, HEIGHT_PLAYER));
player.fill(PG.Color(PLAYER_COLOR));
player_rect = player.get_rect(topleft=(PLAYER_X, PLAYER_Y));

#ініціалізуємо головне вікно гри
main_display = PG.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN));
#Встановлюємо заголовок вікна
PG.display.set_caption('Моя перша гра на Пайтон');



while playing:
    #Заповнюємо чорним вікно гри
    main_display.fill(PG.Color(WINDOW_COLOR));

    #Додаємо фігуру-гравця на вікно програми
    main_display.blit(player, player_rect);
    PG.draw.circle(player, (0,0,255), (WIDTH_PLAYER/2, HEIGHT_PLAYER/2), HEIGHT_PLAYER/2-1);

    

    #зміна напрямку при відбитті від стіни (ліворуч-праворуч)
    if player_rect.right <= WIDTH_SCREEN and way_left:
        player_rect = player_rect.move(PLAYER_WAY_RIGHT);
    else:
        player_rect = player_rect.move(PLAYER_WAY_LEFT);
        way_left = False;

    if player_rect.left <= 0:
        way_left = True;
        player.fill((RN.randint(0,255),RN.randint(0,255),RN.randint(0,255)));

    if player_rect.right >= WIDTH_SCREEN:
        player.fill((RN.randint(0,255),RN.randint(0,255),RN.randint(0,255)));
    


    #Перевіряємо клавішу на закриття вікна
    for event in PG.event.get():
        #Ловим події виходу з гри На хрестик і Ескейп
        if event.type == PG.QUIT:
            playing = False;
        if event.type == PG.KEYDOWN:
            if event.key == PG.K_ESCAPE:
                playing = False;
    pass;
    PG.time.Clock().tick(FPS);
    PG.display.update(main_display.get_rect());
    PG.display.update(player_rect);
pass;
