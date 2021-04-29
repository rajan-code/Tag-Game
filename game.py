import pygame
import sys
import time
from typing import *

pygame.init()
start = time.time()
infoObject = pygame.display.Info()
#screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

print((infoObject.current_w, infoObject.current_h))
HEIGHT = infoObject.current_h  # 1080
WIDTH = infoObject.current_w  # 1920
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
PLAYER_SIZE = 50

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
NAVY_BLUE = (0, 0, 128)

clock = pygame.time.Clock()
FRAME_COUNT = 0
FRAME_RATE = 60  # 30 for 3.7, 60 for 3.8
DEFAULT_TIME = 30  # 30 seconds
LOWEST_TIME, HIGHEST_TIME = 15, 60
DEFAULT_POWER_UPS = False
DEFAULT_ROUNDS = 3
DEFAULT_SPEED = "MED"  # 5
DEFAULT_CHASER = "RED"
#3, 5, 8

# lowest possible time is currently 15s
# highest possible time is 90s
#screen = pygame.display.set_mode()
print(pygame.FULLSCREEN)
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

run = True

TITLE_FONT = pygame.font.SysFont("times new roman", 80, True)
MEDIUM_FONT = pygame.font.SysFont("times new roman", 60)
TIMER_FONT = pygame.font.SysFont("times new roman", 70)  # used for timer
SMALL_FONT = pygame.font.SysFont("times new roman", 40)


def winner_screen(score: List[int]) -> None:
    """
    :param score: [red's score, blue's score]
    """
    screen.fill(BLACK)
    score_text = TIMER_FONT.render("RED " + str(score[0]), 1, RED)
    hyphen_text = TIMER_FONT.render("-", 1, WHITE)
    score_text2 = TIMER_FONT.render(str(score[1]) + " BLUE", 1, BLUE)
    screen.blit(score_text, [int(WIDTH/2-hyphen_text.get_width()/2 - score_text.get_width()), 350])
    screen.blit(hyphen_text, [int(WIDTH/2-hyphen_text.get_width()/2), 350])
    screen.blit(score_text2,
                [int(WIDTH/2-hyphen_text.get_width()/2 + hyphen_text.get_width()), 350])
    if score[0] > score[1]:  # red won
        text = TIMER_FONT.render("RED WON!", 1, RED)
    else:
        text = TIMER_FONT.render("BLUE WON!", 1, BLUE)
    screen.blit(text, [int(WIDTH/2-text.get_width()/2), 450])
    main_menu_text = MEDIUM_FONT.render("Back to Main Menu", 1, RED)
    pygame.draw.rect(screen, RED, (712, 808, main_menu_text.get_width() + 15, main_menu_text.get_height() - 5), 1)
    screen.blit(main_menu_text, (WIDTH // 2 - main_menu_text.get_width() // 2, 850 - 45))  # writes
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            if 712 <= mouse_pos[0] <= 712 + main_menu_text.get_width() + 15 and 808 <= mouse_pos[1] <= 808 + main_menu_text.get_height() - 5:
                main_menu_text = MEDIUM_FONT.render("Back to Main Menu", 1, GREEN)
                pygame.draw.rect(screen, GREEN, (712, 808, main_menu_text.get_width() + 15, main_menu_text.get_height() - 5), 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_menu()
            else:
                main_menu_text = MEDIUM_FONT.render("Back to Main Menu", 1, RED)
                pygame.draw.rect(screen, RED, (
                712, 808, main_menu_text.get_width() + 15,main_menu_text.get_height() - 5), 1)
            screen.blit(main_menu_text, (WIDTH // 2 - main_menu_text.get_width() // 2, 850 - 45))  # writes
            pygame.display.flip()


def detect_collision(p_1_pos: List[int], p_2_pos: List[int]) -> bool:
    """
    Return True iff Player 1 and Player 2 are touching each other.
    """
    x1 = p_1_pos[0]
    y1 = p_1_pos[1]
    x2 = p_2_pos[0]
    y2 = p_2_pos[1]

    if x1 <= x2 <= x1 + PLAYER_SIZE or x2 <= x1 <= x2 + PLAYER_SIZE:
        if y1 <= y2 <= y1 + PLAYER_SIZE or y2 <= y1 <= y2 + PLAYER_SIZE:
            return True
    return False


def draw_game():
    screen.fill(BLACK)
    #pygame.draw.rect(screen, BLACK,(322, 235, WIDTH-654, HEIGHT-470))  # reset game screen
    pygame.draw.rect(screen, WHITE, (333, 241, WIDTH-666, HEIGHT-482), 5)


# game(time, power_ups, num_rounds, speed, current_score, 0)
def game(timer, power_ups: bool, num_rounds: int, speed: str, current_score: List[int], chaser: str, frame_count=0):
    # current_score[0] = red's score

    rounds_played = current_score[0] + current_score[1]

    if speed == "LO":
        player_speed = 4
        chaser_speed = player_speed - 1  # chaser is slightly slower
    elif speed == "MED":
        player_speed = 6
        chaser_speed = player_speed - 1  # chaser is slightly slower
    else:
        player_speed = 9
        chaser_speed = player_speed - 2  # chaser is slightly slower
    draw_game()  # can take out
    p_1_pos = [408, 316]  # red (top left)
    #p_1_pos = [WIDTH-333-75-PLAYER_SIZE, HEIGHT-239-75-PLAYER_SIZE]  # red
    x1, y1 = p_1_pos[0], p_1_pos[1]  # red

    #p_2_pos = [408, 316]  # blue (top left)
    p_2_pos = [WIDTH-333-75-PLAYER_SIZE, HEIGHT-241-75-PLAYER_SIZE]
    x2, y2 = p_2_pos[0], p_2_pos[1]  # blue

    pygame.draw.rect(screen, RED, (x1, y1, PLAYER_SIZE, PLAYER_SIZE)) #draw p1
    pygame.draw.rect(screen, BLUE, (x2, y2, PLAYER_SIZE, PLAYER_SIZE)) #draw p2
    # pressed_keys = {"a": False, "s": False, "d": False, "w": False, "4": False,
    #                 "5": False, "6": False, "8": False}
    pressed_keys = {"a": False, "s": False, "d": False, "w": False, "LEFT": False,
                    "DOWN": False, "RIGHT": False, "UP": False}
    total_seconds = timer
    if current_score[0] == num_rounds//2+1 or current_score[1] == num_rounds//2+1 or sum(current_score) == num_rounds:  # all games have been played:
        print("GAME OVER")
        winner_screen(current_score)
    while total_seconds > 0:
        """
        Representation invariants:
        333 <= x1 and x2 <= WIDTH - 333
        241 <= y1 and y2 <= HEIGHT - 241
        """
        for event in pygame.event.get():
            #mouse_pos = pygame.mouse.get_pos()
            #if event.type == pygame.MOUSEBUTTONDOWN:  # testing
               # print(mouse_pos)
            #if time.time() - start >= 7:
               # pygame.quit()
               # sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Player 1 movement (WASD) red
                if event.key == pygame.K_a:
                    pressed_keys["a"] = True
                if event.key == pygame.K_d:  # right
                    pressed_keys["d"] = True
                if event.key == pygame.K_s:  # down
                    pressed_keys["s"] = True
                if event.key == pygame.K_w:
                    pressed_keys["w"] = True

                # Player 2 movement (num pad) blue
                if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                    pressed_keys["LEFT"] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                    pressed_keys["RIGHT"] = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_KP5:
                    pressed_keys["DOWN"] = True
                if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                    pressed_keys["UP"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    pressed_keys["a"] = False
                if event.key == pygame.K_d:
                    pressed_keys["d"] = False
                if event.key == pygame.K_s:
                    pressed_keys["s"] = False
                if event.key == pygame.K_w:
                    pressed_keys["w"] = False

                # Player 2 movement (arrow keys)
                if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                    pressed_keys["LEFT"] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                    pressed_keys["RIGHT"] = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_KP5:
                    pressed_keys["DOWN"] = False
                if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                    pressed_keys["UP"] = False
        # print(pressed_keys)
        player_to_speed = dict()
        if chaser == "RED":
            player_to_speed["RED"] = chaser_speed
            player_to_speed["BLUE"] = player_speed
        else:
            player_to_speed["RED"] = player_speed
            player_to_speed["BLUE"] = chaser_speed

        if pressed_keys["a"] and x1 > 338:
            x1 -= player_to_speed["RED"]
        if pressed_keys["d"] and x1 < WIDTH - 338 - PLAYER_SIZE:
            x1 += player_to_speed["RED"]
        if pressed_keys["s"] and y1 < HEIGHT - 246 - PLAYER_SIZE:
            y1 += player_to_speed["RED"]
        if pressed_keys["w"] and y1 > 246:
            y1 -= player_to_speed["RED"]

        if pressed_keys["LEFT"] and x2 > 338:
            x2 -= player_to_speed["BLUE"]
            # x2 = max(x2 - PLAYER_SPEED, 333+4)
        # pygame.draw.rect(screen, WHITE, (333, 241, WIDTH-666, HEIGHT-482), 5) white border
        if pressed_keys["RIGHT"] and x2 < WIDTH - 338 - PLAYER_SIZE:
            x2 += player_to_speed["BLUE"]
            # x2 = min(x2 + PLAYER_SPEED, 1587-PLAYER_SIZE-2)  # 1582 is where the white border is
        if pressed_keys["DOWN"] and y2 < HEIGHT - 246 - PLAYER_SIZE:
            y2 += player_to_speed["BLUE"]
            # y2 = min(y2 + PLAYER_SPEED, 333+HEIGHT-482-5)
        if pressed_keys["UP"] and y2 > 246:
            y2 -= player_to_speed["BLUE"]
            #y2 = max(y2 - PLAYER_SPEED, 241+3)
        # print(x2, y2)

        pygame.display.update()
        p_1_pos = [x1, y1]
        p_2_pos = [x2, y2]

        draw_game()

        #  TIMER
        pygame.draw.rect(screen, BLACK, (0, 0, 700, 240))  # draw black rectangle over timer
        total_seconds = timer - (frame_count // FRAME_RATE)

        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "{0:02}:{1:02}".format(minutes, seconds)

        text = TIMER_FONT.render(output_string, True, CYAN)
        screen.blit(text, [int(WIDTH/2 - text.get_width()/2), 140])
        score_text = TIMER_FONT.render("RED " + str(current_score[0]), 1, RED)
        hyphen_text = TIMER_FONT.render("-", 1, WHITE)
        score_text2 = TIMER_FONT.render(str(current_score[1]) + " BLUE", 1, BLUE)
        screen.blit(score_text, [333, 140])
        screen.blit(hyphen_text, [333 + score_text.get_width(), 140])
        screen.blit(score_text2, [333 + score_text.get_width() + hyphen_text.get_width(), 140])

        best_of_text = TIMER_FONT.render("BEST OF " + str(num_rounds), 1, WHITE)
        screen.blit(best_of_text, [int(WIDTH/2 - best_of_text.get_width()/2), 870])
        # update screen where timer is
        timer_rect = pygame.Rect(0, 0, 700, 240)

        frame_count += 1
        clock.tick(FRAME_RATE)
        pygame.display.update(timer_rect)
        #  TIMER end

        pygame.draw.rect(screen, RED,
                             (p_1_pos[0], p_1_pos[1], PLAYER_SIZE, PLAYER_SIZE))  # draw p1
        pygame.draw.rect(screen, BLUE,
                             (p_2_pos[0], p_2_pos[1], PLAYER_SIZE, PLAYER_SIZE))  # draw p2

        if detect_collision(p_1_pos, p_2_pos):  # the chaser wins
            pygame.display.update()
            rounds_played += 1
            time.sleep(0.5)
            if chaser == "RED":
                current_score[0] += 1  # increase red's score
            else:
                current_score[1] += 1  # increase blue's score
            print("Current score: Red:", current_score[0], "Blue:", current_score[1])
            game(timer, power_ups, num_rounds, speed, current_score, chaser, 0)
            # game_screen()
            # main_menu()
        pygame.display.update()

    # time runs out, chaser loses
    if chaser == "RED":
        current_score[1] += 1  # increase blue's score
    else:
        current_score[0] += 1  # increase red's score
    print("Current score: Red:", current_score[0], "Blue:", current_score[1])
    game(timer, power_ups, num_rounds, speed, current_score, chaser, 0)
    # rounds_played += 1
    # game(time, )
    # game(time, power_ups, num_rounds, speed, [0, 0], 0)
    # pygame.quit()  # exit when timer = 0

# game()


def game_screen(time=DEFAULT_TIME, power_ups=DEFAULT_POWER_UPS, num_rounds=DEFAULT_ROUNDS, speed=DEFAULT_SPEED, chaser=DEFAULT_CHASER):  # user can change settings
    rounds_to_col = dict()
    speeds_to_col = dict()
    for s in ["LO", "MED", "HI"]:
        if s == speed:
            speeds_to_col[s] = GREEN
        else:
            speeds_to_col[s] = WHITE
    for round_ in [1, 3, 5, 7]:
        if round_ == num_rounds:
            rounds_to_col[round_] = GREEN
        else:
            rounds_to_col[round_] = WHITE

    screen.fill(BLACK)
    title_text = TIMER_FONT.render("Settings", 1, BLUE)
    screen.blit(title_text, ((WIDTH // 2 - title_text.get_width() // 2), 175))
    # pygame.draw.rect(screen, BLUE, (636, 250, 609, 657), 1)
    text1 = MEDIUM_FONT.render("Time:  " + str(time) + "s", 1, WHITE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) - 150, 350-50))
    pygame.draw.rect(screen, WHITE, (990+47, 355-50, 190, 75), 1)
    pygame.draw.line(screen, WHITE, (1085+47, 355-50), (1085+47, 430-50), 1)

    # draw plus
    text1 = MEDIUM_FONT.render("+", 1, WHITE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) + 75+47, 355-50))  # plus
    minus = MEDIUM_FONT.render("-", 1, WHITE)
    screen.blit(minus, ((WIDTH // 2 - text1.get_width() // 2) + 179+47, 355-50))
    text1 = MEDIUM_FONT.render("Powerups:", 1, WHITE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) - 150, 450-50))
    pygame.draw.rect(screen, WHITE, (990+47, 455-50, 190, 75), 1)  # box containing ON and OFF
    pygame.draw.line(screen, WHITE, (1085+47, 455-50), (1085+47, 530-50), 1)
    if not power_ups:
        text1 = SMALL_FONT.render("ON", 1, WHITE)
        text2 = SMALL_FONT.render("OFF", 1, GREEN)
    else:
        text1 = SMALL_FONT.render("ON", 1, GREEN)
        text2 = SMALL_FONT.render("OFF", 1, WHITE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) + 79 + 47, 470-50))  # writes ON
    screen.blit(text2, ((WIDTH // 2 - text2.get_width() // 2) + 172 + 47, 470-50))  # writes OFF

    text1 = MEDIUM_FONT.render("Rounds:", 1, WHITE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) - 150, 550-50))
    # each small box has width = 95 and height = 75
    pygame.draw.rect(screen, WHITE, (990-47, 555-50, 380, 75), 1)  # ROUNDS rect
    for x_coord in [1038, 1038 + 95, 1038 + (95*2)]:
        pygame.draw.line(screen, WHITE, (x_coord, 555-50), (x_coord, 630-50), 1)
    for num, pos in [(1, 79), (3, 79+95), (5, 79+(95*2)), (7, 79+(95*3))]:  # write the numbers
        text1 = SMALL_FONT.render(str(num), 1, rounds_to_col[num])
        screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) + pos-47, 570-50))

    # plus rect: (990, 357, 95, 72)
    # minus rect: (1085, 355), (1180, 430)  (topleft, bottom_right)
    # ON rect: (990, 455), (1085, 530)
    # OFF rect: (1085, 455), (1180, 530)
    text1 = MEDIUM_FONT.render("Speed:", 1, WHITE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) - 150, 650-50))
    pygame.draw.rect(screen, WHITE, (989, 650-50, 285, 75), 1)
    for x_coord in [989+95, 989+(95*2)]:
        pygame.draw.line(screen, WHITE, (x_coord, 650-50), (x_coord, 725-50), 1)  # LO, MED, HI rect
    for sp, pos in [("LO", 79), ("MED", 79+94), ("HI", 79+(95*2))]:  # write LO, MED, HI
        text1 = SMALL_FONT.render(sp, 1, speeds_to_col[sp])
        screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) + pos, 665-50))

    play_text = MEDIUM_FONT.render("PLAY", 1, RED)
    pygame.draw.rect(screen, RED, (875, 853-45, play_text.get_width() + 15, play_text.get_height() - 5), 1)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 850-45))  # writes PLAY

    chaser_text = MEDIUM_FONT.render("Chaser:", 1, WHITE)
    screen.blit(chaser_text, ((WIDTH // 2 - chaser_text.get_width() // 2) - 150, 650 - 50+100))
    pygame.draw.rect(screen, WHITE, (990, 455-50+300, 190+47, 75), 1)  # box containing RED and BLUE
    pygame.draw.line(screen, WHITE, (1085+23, 455-50+300), (1085+23, 530-50+300), 1)
    if chaser == "RED":
        text1 = SMALL_FONT.render("RED", 1, RED)
        text2 = SMALL_FONT.render("BLUE", 1, WHITE)
    else:
        text1 = SMALL_FONT.render("RED", 1, WHITE)
        text2 = SMALL_FONT.render("BLUE", 1, BLUE)
    screen.blit(text1, ((WIDTH // 2 - text1.get_width() // 2) + 79 + 47-47+15, 470 - 50+300))  # writes RED
    screen.blit(text2, ((WIDTH // 2 - text2.get_width() // 2) + 172 + 47-10, 470 - 50+300))  # writes BLUE

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            if 875 <= mouse_pos[0] <= play_text.get_width()+890 and 853-45 <= mouse_pos[1] <= 853-45+play_text.get_height()-5:
                play_text = MEDIUM_FONT.render("PLAY", 1, GREEN)
                pygame.draw.rect(screen, GREEN, (875, 853-45, play_text.get_width() + 15, play_text.get_height() - 5), 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game(time, power_ups, num_rounds, speed, [0, 0], chaser, 0)
            else:
                play_text = MEDIUM_FONT.render("PLAY", 1, RED)
                pygame.draw.rect(screen, RED, (875, 853-45, play_text.get_width() + 15, play_text.get_height() - 5), 1)
            screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 850-45))
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONUP:
                # print(event.pos)
                if time < HIGHEST_TIME and 990+47 < event.pos[0] < 1085+47 and 355-50 < event.pos[1] < 430-50:  # click plus
                    game_screen(time + 5, power_ups, num_rounds, speed, chaser)
                elif time > LOWEST_TIME and 1085+47 < event.pos[0] < 1180+47 and 355-50 < event.pos[1] < 430-50:  # click minus
                    game_screen(time - 5, power_ups, num_rounds, speed, chaser)
                elif not power_ups and 990+47 < event.pos[0] < 1085+47 and 455-50 < event.pos[1] < 530-50:  # click ON rect
                    game_screen(time, True, num_rounds, speed, chaser)
                elif power_ups and 1085+47 < event.pos[0] < 1180+47 and 455-50 < event.pos[1] < 530-50:  # click OFF rect
                    game_screen(time, False, num_rounds, speed, chaser)
                elif num_rounds != 1 and 943 < event.pos[0] < 1038 and 555-50 < event.pos[1] < 555+75-50:  # click 1
                    game_screen(time, power_ups, 1, speed, chaser)
                elif num_rounds != 3 and 1038 < event.pos[0] < 1133 and 555-50 < event.pos[1] < 555+75-50:  # click 3
                    game_screen(time, power_ups, 3, speed, chaser)
                elif 1133 < event.pos[0] < 1228 and 555-50 < event.pos[1] < 555+75-50:  # click 5
                    game_screen(time, power_ups, 5, speed, chaser)
                elif 1228 < event.pos[0] < 1323 and 555-50 < event.pos[1] < 555+75-50:  # click 7
                    game_screen(time, power_ups, 7, speed, chaser)
                elif speed != "LO" and 989 < event.pos[0] < 989+95 and 650-50 < event.pos[1] < 650+75-50:
                    game_screen(time, power_ups, num_rounds, "LO", chaser)
                elif speed != "MED" and 1084 < event.pos[0] < 1084+95 and 650-50 < event.pos[1] < 650+75-50:
                    game_screen(time, power_ups, num_rounds, "MED", chaser)
                elif speed != "HI" and 1179 < event.pos[0] < 1179+95 and 650-50 < event.pos[1] < 650+75-50:
                    game_screen(time, power_ups, num_rounds, "HI", chaser)
                elif chaser != "RED" and 990 < event.pos[0] < 1108 and 705 < event.pos[1] < 705+75:
                    game_screen(time, power_ups, num_rounds, speed, "RED")
                elif chaser != "BLUE" and 1108 < event.pos[0] < 1227 and 705 < event.pos[1] < 705+75:
                    game_screen(time, power_ups, num_rounds, speed, "BLUE")
                # pygame.draw.rect(screen, WHITE, (990 + 47-47, 455 - 50+300, 190+47, 75), 1)  # box containing RED and BLUE
                #pygame.draw.line(screen, WHITE, (1085 + 47-47+23, 455 - 50+300), (1085 + 47-47+23, 530 - 50+300), 1)
                # pygame.display.flip()
                #  for x_coord in [989+95, 989+(95*2)]:
                #  pygame.draw.line(screen, WHITE, (x_coord, 650), (x_coord, 725), 1)
                # for num, x_c in [(1, 943), (3, 1038), (5, 1133), (7, 1228)]:
                 #   if x_c < event.pos[0] < x_c + 95 and 555 < event.pos[1] < 555+75:
                  #      game_screen(time, power_ups, num_rounds=num)
                   #     print(num)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()


def main_menu():
    print("Instructions:")
    print("The game is quite simple: the chaser must tag the other player before the timer runs out.")
    print("Controls for red: WASD")
    print("Controls for blue: 4, 5, 6, 8 (numpad) or arrow keys")

    screen.fill(BLACK)
    this_page = True
    title_text = TITLE_FONT.render("Tag", 1, WHITE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 250))

    #  pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    instructions_text = MEDIUM_FONT.render("INSTRUCTIONS", 1, GREEN)
    pygame.draw.rect(screen, GREEN, (735, 450, instructions_text.get_width() + 15,instructions_text.get_height()), 1)
    play_text = MEDIUM_FONT.render("PLAY", 1, RED)
    pygame.draw.rect(screen, RED, (875, 753, play_text.get_width()+15, play_text.get_height()-5), 1)
    screen.blit(play_text, (WIDTH//2 - play_text.get_width()//2, 750))
    exit_text = MEDIUM_FONT.render("Exit", 1, WHITE)
    screen.blit(exit_text, (210, 910))  # bottom left
    pygame.draw.rect(screen, WHITE, (205, 910, exit_text.get_width() + 15, exit_text.get_height() - 5), 1)
    pygame.display.flip()
    while this_page:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            # print(mouse_pos)
            if 205 <= mouse_pos[0] <= 220+exit_text.get_width() and 910 <= mouse_pos[1] <= 905+exit_text.get_height():
                exit_text = MEDIUM_FONT.render("Exit", 1, NAVY_BLUE)
                pygame.draw.rect(screen, NAVY_BLUE, (205, 910, exit_text.get_width() + 15, exit_text.get_height() - 5), 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sys.exit()
                # 205, 910, exit_text.get_width() + 15, exit_text.get_height() - 5
            else:
                exit_text = MEDIUM_FONT.render("Exit", 1, WHITE)
                pygame.draw.rect(screen, WHITE, (205, 910, exit_text.get_width() + 15, exit_text.get_height() - 5), 1)
            if 735 <= mouse_pos[0] <= instructions_text.get_width()+750 and 450 <= mouse_pos[1] <= 515: #instructions box
                instructions_text = MEDIUM_FONT.render("INSTRUCTIONS", 1, GREEN)
                pygame.draw.rect(screen, GREEN, (735, 450, instructions_text.get_width() + 15, instructions_text.get_height()), 1)
            else:
                instructions_text = MEDIUM_FONT.render("INSTRUCTIONS", 1, BLUE)
                pygame.draw.rect(screen, BLUE, (735, 450, instructions_text.get_width() + 15, instructions_text.get_height()),1)  # box around Instructions
            if 875 <= mouse_pos[0] <= play_text.get_width()+890 and 753 <= mouse_pos[1] <= 748+play_text.get_height():
                play_text = MEDIUM_FONT.render("PLAY", 1, GREEN)
                pygame.draw.rect(screen, GREEN, (875, 753, play_text.get_width() + 15, play_text.get_height() - 5), 1)
                if event.type== pygame.MOUSEBUTTONDOWN:
                    this_page = False
                    game_screen()
            else:
                play_text = MEDIUM_FONT.render("PLAY", 1, RED)
                pygame.draw.rect(screen, RED, (875, 753, play_text.get_width() + 15, play_text.get_height() - 5), 1)

            # if event.type == pygame.MOUSEBUTTONDOWN:  # testing
                # print(mouse_pos)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 750))
        screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, 450))
        screen.blit(exit_text, (210, 910))  # bottom left
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
