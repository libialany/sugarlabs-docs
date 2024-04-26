#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sugar3.activity.activity import get_activity_root
import time
import locale
from pygame.locals import Rect
from pygame.locals import QUIT
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEMOTION
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
import pygame
import random
from gi.repository import Gtk
import gi

gi.require_version("Gtk", "3.0")


class number(pygame.sprite.Sprite):

    def __init__(self, x, y, image, answer=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect((x, y), (self.image.get_width(), self.image.get_height()))
        self.answer = answer

    def update(self, time_to_iterate, vel, level):
        incremento_nivel = {"facil": 1, "medio": 2, "dificil": 3}
        self.rect.move_ip(0, - (time_to_iterate * vel * incremento_nivel[level]))


class expresion:

    def __init__(self, level, fuente):

        incremento_nivel = {"facil": 9, "medio": 20, "dificil": 50}
        operacion = {1: "+", 2: "-", 3: "*", 4: "/"}
        self.fuente = fuente
        self.simbolo = {1: "+", 2: "-", 3: "X", 4: ":"}
        self.operador = random.randint(2, 3)
        self.primero = str(random.randint(0, incremento_nivel[level]))
        self.segundo = str(random.randint(0, incremento_nivel[level]))
        self.expresion = fuente.render(
            " " + self.primero + self.simbolo[self.operador] + self.segundo + " = ? ",
            True,
            (255, 120, 120),
            (0, 0, 0),
        )
        self.resultado = str(
            eval(self.primero + operacion[self.operador] + self.segundo)
        )
        self.vida = 0

        list_y = [
            int(sx(1100)),
            int(sx(1090)),
            int(sx(1080)),
            int(sx(1070)),
            int(sx(1060)),
            int(sx(1050)),
            int(sx(950)),
            int(sx(850)),
            int(sx(900)),
        ]
        list_x = [
            int(sx(80)),
            int(sx(200)),
            int(sx(320)),
            int(sx(440)),
            int(sx(560)),
            int(sx(680)),
            int(sx(800)),
            int(sx(920)),
            int(sx(1040)),
        ]

        def rand_generator_x():
            rand_coord_x = random.choice(list_x)
            list_x.remove(rand_coord_x)
            return rand_coord_x

        def rand_generator_y():
            rand_coord_y = random.choice(list_y)
            list_y.remove(rand_coord_y)
            return rand_coord_y

        self.preguntas = pygame.sprite.Group()
        self.correct_number = number(
            rand_generator_x(),
            rand_generator_y(),
            fuente.render(self.resultado, True, (255, 120, 120)),
            True,
        )
        self.preguntas.add(self.correct_number)
        self.wrong_numbers = []
        for i in range(0, 5):
            if random.randint(0, 1) == 0:
                wrong = str(int(self.resultado) - random.randint(1, 10))
            else:
                wrong = str(int(self.resultado) + random.randint(1, 10))
            wrong_x_coord = rand_generator_x()
            wrong_y_coord = rand_generator_y()
            image_wrong = fuente.render(wrong, True, (255, 120, 120))
            self.wrong_numbers.append(
                number(wrong_x_coord, wrong_y_coord, image_wrong, False)
            )
        self.preguntas.add(*self.wrong_numbers)

    def update_expression(self, user):
        self.expresion = self.fuente.render(
            " "
            + self.primero
            + self.simbolo[self.operador]
            + self.segundo
            + " = "
            + user,
            True,
            (255, 120, 120),
            (0, 0, 0),
        )


def cargar_imagen(nombre, trasnparent=False):
    try:
        imagen = pygame.image.load(nombre)
        sizex, sizey = imagen.get_rect().size
        imagen = pygame.transform.scale(
            imagen, (int(sizex * scale_x), int(sizey * scale_y))
        )
    except pygame.error as message:
        raise SystemExit(message)
    imagen = imagen.convert()
    return imagen


def get_translated_text(text):
    if locale.getdefaultlocale()[0][:2] != "es":
        return text
    translations = {
        "PLAY": "JUGAR",
        "LEVEL": "NIVEL",
        "QUIT": "SALIR",
        "easy": "facil",
        "medium": "medio",
        "hard": "dificil",
        "Score : ": "Punjate : ",
        "Highest Score : ": "Puntaje Mas Alto : ",
        "Timer : ": "Temporizador : ",
        "PLAY AGAIN": "jUEGA DE NUEVO",
        "GAME OVER!!": "JUEGO TERMINADO!!",
        "Hurray! you won :)": "Hurra! ganaste :)",
        "Ay! you lost :(": "Ay! perdiste :(",
        "Select correct ball to answer or type it using keyboard": "Selecciona la bola correcta para responder o escribe la respuesta usando el teclado",
    }
    return translations[text]


class Game:

    def __init__(self, activity):
        self.activity = activity
        self.user = ""
        self.keys = (
            pygame.K_0,
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
            pygame.K_MINUS,
            pygame.K_BACKSPACE,
            pygame.K_RETURN,
        )

    global sx, sy

    def sx(coord_x):
        return coord_x * scale_x

    def sy(coord_y):
        return coord_y * scale_y
    
    def play(self, level):
        die_point = {"facil": 200, "medio": 100, "dificil": 60}
        another_quest = True
        fondo = cargar_imagen("data/" + str(1) + ".jpg")
        score = 0
        response = 0
        play_again = self.fuente_60.render(
            get_translated_text("PLAY AGAIN"), True, (0, 0, 0), (255, 0, 0)
        )
        quit_game = self.fuente_60.render(
            get_translated_text("QUIT"), True, (0, 0, 0), (255, 0, 0)
        )
        max_time_limit = 60.00
        start_time = time.time()
        current_time = max_time_limit
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(fondo, (0, 0))
            if response == 0:
                time_to_iterate = self.clock.tick(30) / 1000.0
                if another_quest:
                    nueva_expresion = expresion(level, self.fuente_60)
                    another_quest = False

                nueva_expresion.vida += 1
                if nueva_expresion.vida > die_point[level]:
                    another_quest = True
                nueva_expresion.preguntas.update(
                    time_to_iterate, random.randint(80, 155), level
                )
                current_score = self.fuente_32.render(
                    get_translated_text(" Score : ") + str(score) + " ",
                    True,
                    (120, 120, 120),
                    (0, 0, 0),
                )

                current_score_rect = current_score.get_rect()
                current_score_rect.topleft = sx(60), sy(10)
                self.screen.blit(current_score, current_score_rect)
                expresion_rect = nueva_expresion.expresion.get_rect()
                expresion_rect.midtop = sx(600), sy(10)
                self.screen.blit(nueva_expresion.expresion, expresion_rect)

                for number in (
                    nueva_expresion.correct_number,
                    *nueva_expresion.wrong_numbers,
                ):
                    pygame.draw.circle(
                        self.screen, (40, 40, 40), number.rect.center, 50
                    )
                nueva_expresion.preguntas.draw(self.screen)
                current_time = max_time_limit - (time.time() - start_time)
                countdown_time = "{:.2f}".format(current_time)
                timer = self.fuente_32.render(
                    get_translated_text(" Timer : ") + str(countdown_time),
                    True,
                    (255, 120, 120),
                    (0, 0, 0),
                )
                timer_rect = timer.get_rect()
                timer_rect.topleft = sx(980), sy(10)
                self.screen.blit(timer, timer_rect)

            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            if float(current_time) <= 00.10:
                game_over()
                response = 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return
                elif event.type == MOUSEMOTION:
                    not_hover = True
                    if not_hover:
                        play_again = self.fuente_60.render(
                            get_translated_text("PLAY AGAIN"),
                            True,
                            (0, 0, 255),
                            (0, 0, 0),
                        )
                        quit_game = self.fuente_60.render(
                            get_translated_text("QUIT"), True, (0, 0, 255), (0, 0, 0)
                        )

                    if (
                        event.pos[0] > sx(260)
                        and event.pos[0] < sx(260) + play_again.get_width()
                        and event.pos[1] > sy(700)
                        and event.pos[1] < sy(700) + play_again.get_height()
                    ):
                        play_again = self.fuente_60.render(
                            get_translated_text("PLAY AGAIN"),
                            True,
                            (122, 245, 61),
                            (102, 110, 98),
                        )
                    if (
                        event.pos[0] > sx(840)
                        and event.pos[0] < sx(840) + quit_game.get_width()
                        and event.pos[1] > sy(700)
                        and event.pos[1] < sy(700) + quit_game.get_height()
                    ):
                        quit_game = self.fuente_60.render(
                            get_translated_text("QUIT"),
                            True,
                            (122, 245, 61),
                            (102, 110, 98),
                        )
                    else:
                        not_hover = True
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in nueva_expresion.preguntas.sprites():
                            if (
                                event.pos[0] > i.rect.x
                                and event.pos[0] < i.rect.x + i.image.get_width()
                                and event.pos[1] > i.rect.y
                                and event.pos[1] < i.rect.y + i.image.get_height()
                            ):
                                if i.answer:
                                    another_quest = True
                                    score += 7

                                else:
                                    another_quest = True
                                    score -= 3
                        if response == 1:
                            if (
                                event.pos[0] > sx(260)
                                and event.pos[0] < sx(260) + play_again.get_width()
                                and event.pos[1] > sy(700)
                                and event.pos[1] < sy(700) + play_again.get_height()
                            ):
                                return
                            if (
                                event.pos[0] > sx(840)
                                and event.pos[0] < sx(840) + quit_game.get_width()
                                and event.pos[1] > sy(700)
                                and event.pos[1] < sy(700) + quit_game.get_height()
                            ):
                                self.running = False
                                self.activity.close()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return 0
                    if event.key in self.keys:
                        if event.key == pygame.K_RETURN:
                            if self.user == nueva_expresion.resultado:
                                score += 7
                            else:
                                score -= 3
                            another_quest = True
                            self.user = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.user = self.user[:-1]
                        elif event.key == pygame.K_MINUS:
                            if len(self.user) > 0 and self.user[0] == "-":
                                self.user = self.user[1:]
                            else:
                                self.user = "-" + self.user
                        else:
                            self.user += pygame.key.name(event.key)
                        nueva_expresion.update_expression(self.user)

            def game_over():

                while Gtk.events_pending():
                    Gtk.main_iteration()
                gameover = self.fuente_130.render(
                    get_translated_text("GAME OVER!!"), True, (255, 255, 255), (0, 0, 0)
                )
                score_display = self.fuente_60.render(
                    get_translated_text("Your Score : ") + str(score),
                    True,
                    (0, 255, 255),
                    (0, 0, 0),
                )
                gameover_rect = gameover.get_rect()
                gameover_rect.midtop = (sx(590), sy(100))
                score_display_rect = score_display.get_rect()
                score_display_rect.center = (sx(590), sy(400))
                quit_rect = quit_game.get_rect()
                quit_rect.topleft = (sx(840), sy(700))
                play_again_rect = play_again.get_rect()
                play_again_rect.topleft = (sx(260), sy(700))
                self.screen.blit(fondo, (0, 0))
                self.screen.blit(gameover, gameover_rect)
                self.screen.blit(score_display, score_display_rect)
                self.screen.blit(quit_game, quit_rect)
                self.screen.blit(play_again, play_again_rect)
                pygame.display.flip()

            pygame.display.update()

    def run(self):
        self.running = True
        self.screen = pygame.display.get_surface()

        info = pygame.display.Info()

        if not self.screen:
            self.screen = pygame.display.set_mode((info.current_w, info.current_h))

        global scale_x, scale_y
        scale_x = self.screen.get_width() / 1200.0
        scale_y = self.screen.get_height() / 900.0

        self.clock = pygame.time.Clock()

        self.fuente_32 = pygame.font.Font("data/fuente.ttf", int(sx(32)))
        self.fuente_60 = pygame.font.Font("./data/fuente.ttf", int(sx(60)))
        self.fuente_130 = pygame.font.Font("./data/fuente.ttf", int(sx(130)))

        self.fondo = cargar_imagen("data/1.jpg")
        self.screen.blit(self.fondo, (0, 0))
        pygame.display.flip()
        while self.running:
            self.play("facil")


# Funcion para cargar Sonidos
# def load_sound(name):
#     path = os.path.join("data", name)
#     try:
#         sound = pygame.mixer.Sound(path)
#         return sound
#     except BaseException:
#         logging.debug("Warning, unable to load: ", path)
#     return None