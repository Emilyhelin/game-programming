import pygame
import copy
import random
from pygame.locals import *
import numpy as np


class Text:
    def __init__(self, text, pos, size, colour):
        self.text = text
        self.pos = pos
        self.size = size
        self.colour = colour

    def draw(self, screen):
        text = pygame.font.SysFont(None, self.size).render(self.text, True, self.colour)
        screen.blit(text, self.pos)


class Tile:
    def __init__(self):
        # self.image = pygame.image.load(image)
        self.colour = None
        self.value = None
        self.colourDict = {1: "black", 2: "red", 3: "yellow", 4: "green", 5: "blue"}

    # def draw_image(self, screen, x, y):
    # resized_image = pygame.transform.scale('tiles/blue_1.png', (50,75))
    # screen.blit(resized_image, (x, y))

    def create_tile(self, c, v):
        self.value = v
        self.colour = c

    def image_name(self):
        fn = self.colourDict[self.colour] + "_" + str(self.value) + ".png"
        return fn

    def print_tile(self):
        return (str(self.colour), str(self.value))


class Table:
    def __init__(self):
        self.table = [[''] * 28, [''] * 28, [''] * 28, [''] * 28, [''] * 28, [''] * 28, [''] * 28, [''] * 28]

    def print_table(self):
        for i in self.table:
            print(i)

    def get_space(self, h, w):
        return (self.table[h][w])

    def place_tile(self, h, w, tile):
        self.table[h][w] = tile


class Timer:
    def __init__(self):
        pygame.font.init()
        self.timer_font = pygame.font.SysFont(None, 50)
        self.start_time = None
        self.timeout = False

    def print_timer(self, screen):
        timeleft = 100
        if self.start_time is None:
            self.start_time = pygame.time.get_ticks()
        else:
            sec = (pygame.time.get_ticks() - self.start_time) // 1000
            timeleft = 100 - sec

        if not self.timeout:
            self.timer_text = self.timer_font.render(str(timeleft), True, (255, 255, 255))
        else:
            self.timer_text = self.timer_font.render("Timeout", True, (255, 255, 255))
        screen.blit(self.timer_text, (15, 15))

        if timeleft < 0:
            self.timeout = True
            return True
        else:
            return False

    def reset(self):
        self.start_time = None
        self.timeout = False


class Button:
    def __init__(self, Word, Left, Right, Top, Bottom, size):
        self.word = Word
        self.left = Left
        self.right = Right
        self.top = Top
        self.bottom = Bottom
        self.size = size

    def create_button(self):
        X, Y = pygame.mouse.get_pos()
        if (X > self.left and X < self.right) and (Y > self.top and Y < self.bottom):
            return Text(self.word, (self.left, self.top), self.size, pygame.Color('yellow'))
        else:
            return Text(self.word, (self.left, self.top), self.size, pygame.Color('darkred'))

    # check player


class ScoringBoard:
    def __init__(self):
        self.board = [[''] * 28 for _ in range(10)]

    def print_table(self):
        for row in self.board:
            print(row)

    def get_space(self, h, w):
        return self.board[h][w]


def calculate_score(player_rack):
    total_score = 0
    for move in player_rack:
        for tile in move:
            if tile !="break":
                total_score += int(tile["value"])
    return total_score
#p1_score = calculate_score(p1_moves)

class Grid:
    def __init__(self, row, col, left, top, tile, selected):
        self.row = row
        self.col = col
        self.left = left
        self.top = top
        self.tile = tile
        self.selected = selected

    def setTile(self, tile):
        self.tile = tile


def checkVaild(list):  # 判断是否是用奇数偶数在做
    list = sorted(list, key=lambda k: int(k.tile["value"]))  # int zheli kengsi
    for i in range(len(list) - 1):
        if int(list[i + 1].tile["value"]) - int(list[i].tile["value"]) != 2:
            return False
    return True


colourDict2 = {"black": 1, "red": 2, "yellow": 3, "green": 4, "blue": 5}

deck = []
for c in range(1, 6):
    for n in range(1, 16):
        tile = Tile()
        tile.create_tile(c, n)
        deck.append(tile)


def run_game():
    pygame.init()
    pygame.mixer.init()

    SCREEN_HEIGHT = 800
    SCREEN_WEIGHT = 1500
    TILE_WEIGHT = 50
    TILE_HEIGHT = 75

    START_LEFT = 700
    START_RIGHT = 780
    START_TOP = 350
    START_BOTTOM = 380

    QUIT_LEFT = 700
    QUIT_RIGHT = 780
    QUIT_TOP = 500
    QUIT_BOTTOM = 530

    screen = pygame.display.set_mode((SCREEN_WEIGHT, SCREEN_HEIGHT))
    pygame.display.set_caption('Rummikub')

    screen.fill(pygame.Color('darkgreen'))
    Text('RUMMIKUB', (550, 100), 100, pygame.Color('darkred')).draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # press X
                return
            elif event.type == MOUSEMOTION:
                pygame.display.set_caption("test:" + str(event.pos))  # show the pos of mouse for test

        x, y = pygame.mouse.get_pos()

        # start button
        Start = Button('Start', START_LEFT, START_RIGHT, START_TOP, START_BOTTOM, 50)
        Start.create_button().draw(screen)

        # quit button
        Quit = Button('Quit', QUIT_LEFT, QUIT_RIGHT, QUIT_TOP, QUIT_BOTTOM, 50)
        Quit.create_button().draw(screen)

        # press quit button
        if (x > QUIT_LEFT and x < QUIT_RIGHT) and (
                y > QUIT_TOP and y < QUIT_BOTTOM) and event.type == pygame.MOUSEBUTTONDOWN:
            return
        # press start button
        if (x > START_LEFT and x < START_RIGHT) and (
                y > START_TOP and y < START_BOTTOM) and event.type == pygame.MOUSEBUTTONDOWN:
            break

        pygame.display.flip()

    screen.fill(pygame.Color('darkgreen'))
    pygame.draw.rect(screen, 'darkred', pygame.Rect(500, 605, 500, 90))

    DRAW_LEFT = 1400
    DRAW_RIGHT = 1490
    DRAW_TOP = 750
    DRAW_BOTTOM = 780

    # play area
    PLAY_SQUARE_LEFT = 500
    PLAY_SQUARE_TOP = 590
    PLAY_SQUARE_WEIGHT = 500
    PLAY_SQUARE_HEIGHT = 100

    # play button
    PLAY_LEFT = 1020
    PLAY_RIGHT = 1095
    PLAY_TOP = PLAY_SQUARE_TOP + 30
    PLAY_BOTTOM = 665

    # change player button
    CHANGE_LEFT = 20
    CHANGE_RIGHT = 100
    CHANGE_TOP = 700
    CHANGE_BOTTOM = 730

    YELLOW_LINE_TOP = 650
    YELLOW_LINE_LEFT = 0

    # player_rack
    tile_x = 200
    tile_y = 700

    pool = copy.deepcopy(deck)

    #winner tag
    winner=False
    # build all player's tiles
    player_box = []
    # the rack show on screen
    player_rack = []
    player_rack1 = []
    player_rack2 = []
    player_rack3 = []
    player_rack4 = []
    player_rack5 = []
    player_box.append(player_rack1)
    player_box.append(player_rack2)
    player_box.append(player_rack3)
    #player_box.append(player_rack4)
    #player_box.append(player_rack5)

    # store all players' scores
    list_of_scores = []
    # the scores shown on screen
    scores = 0
    nowround_scores=0
    p1_scores = 0
    p2_scores = 0
    p3_scores = 0
    p4_scores = 0
    p5_scores = 0
    list_of_scores.append(p1_scores)
    list_of_scores.append(p2_scores)
    list_of_scores.append(p3_scores)
    list_of_scores.append(p4_scores)
    list_of_scores.append(p5_scores)
    #punish to draw card



    # 初始化所有手牌
    for player in player_box:
        for i in range(14):
            tile = random.choice(pool)  # deck_copy ==pool
            #tile = pool[i]  # test
            pool.remove(tile)
            fn = tile.image_name()
            tile_info = fn[:-4].split("_")
            # for example: blue red
            tile_color = tile_info[0]
            # for example: 1、2、3、4、5
            tile_value = tile_info[1]
            # build tile dictionary
            player.append({
                "color": tile_color,
                "value": tile_value,
                "rect": pygame.Rect(tile_x + 75 * i, tile_y, TILE_WEIGHT, TILE_HEIGHT),
                "tile_name": fn,
                "last_rect": pygame.Rect(tile_x + 75 * i, tile_y, TILE_WEIGHT, TILE_HEIGHT),
                "selected": False,
                "belong": "rack",
                "ori":tile})  # belong two value: rack or table
    # begin with player 1
    player_rack = player_rack1

    punish_draw = 0
    punish_draw_list = []
    for i in range(2):
        if punish_draw == 0:
            tile = random.choice(pool)
            # pool.remove(tile)
            fn = tile.image_name()
            tile_info = fn[:-4].split("_")
            tile_color = tile_info[0]
            tile_value = tile_info[1]
            # drawn.append({"color": tile_color, "value": tile_value,
            # "rect": pygame.Rect(1350 + 75 * i, 660, TILE_WEIGHT, TILE_HEIGHT), "tile_name": fn})
            punish_draw_list.append({
                "color": tile_color,
                "value": tile_value,
                "rect": pygame.Rect(1350 + 75 * i, 660, TILE_WEIGHT, TILE_HEIGHT),
                "tile_name": fn,
                "last_rect": pygame.Rect(1350 + 75 * i, 660, TILE_WEIGHT, TILE_HEIGHT),
                "selected": False,
                "belong": "rack",
                "ori":tile})

    scores=p1_scores
    first_turn = True
    dragging = False
    t_dragging = False
    dragged_tile_index = None
    t_dragged_tile_index = 0
    offset_x, offset_y = 0, 0
    t_offset_x, t_offset_y = 0, 0

    play_draw = 0
    drawn = []
    drawn_info = []
    play = []
    move = []
    on_table = []
    score = 0
    timer = Timer()
    # 起始的玩家位 1
    player_pos = 1
    score_pos = 1

    clock = pygame.time.Clock()

    # breakice
    break_ice = False
    # put tile on desk
    Table = []
    for i in range(6):
        top = 100 + i * 85
        for j in range(25):
            left = 0 + 60 * j
            grid = Grid(i, j, left, top, None, False)
            #print(grid.left)
            # pygame.draw.rect(screen, 'white', pygame.Rect(left, top, 50, 75))  # line
            Table.append(grid)

    Table_previous = copy.deepcopy(Table)

    # print(len(Table[5]))
    # change player function
    ChangePlayer = Button('Finish', CHANGE_LEFT, CHANGE_RIGHT, CHANGE_TOP, CHANGE_BOTTOM, 50)
    # test button
    Play = Button('Play', 20, 165, 750, 780, 50)
    #
    Draw = Button('Draw', DRAW_LEFT, DRAW_RIGHT, DRAW_TOP, DRAW_BOTTOM, 50)

    while True:
        if punish_draw_list==[]:
            for i in range(2):
                if punish_draw == 0:
                    tile = random.choice(pool)
                # pool.remove(tile)
                    fn = tile.image_name()
                    tile_info = fn[:-4].split("_")
                    tile_color = tile_info[0]
                    tile_value = tile_info[1]
                # drawn.append({"color": tile_color, "value": tile_value,
                # "rect": pygame.Rect(1350 + 75 * i, 660, TILE_WEIGHT, TILE_HEIGHT), "tile_name": fn})
                    punish_draw_list.append({
                        "color": tile_color,
                        "value": tile_value,
                        "rect": pygame.Rect(1350 + 75 * i, 660, TILE_WEIGHT, TILE_HEIGHT),
                        "tile_name": fn,
                        "last_rect": pygame.Rect(1350 + 75 * i, 660, TILE_WEIGHT, TILE_HEIGHT),
                        "selected": False,
                        "belong": "rack",
                        "ori":tile})
        clock.tick(10)
        X, Y = pygame.mouse.get_pos()

        # prints all of the images onto the screen
        screen.fill(pygame.Color('darkgreen'))
        timer.print_timer(screen)

        if winner is not True:
            # 结束惩罚或者分数大于0可以结束
            if punish_draw == 2 or nowround_scores>0:
                    ChangePlayer.create_button().draw(screen)
                    print(nowround_scores)

            #如果进入惩罚则不能再玩
            #print(len(pool))
            # print(timer.timer_text)
            # print(timer.timeout)
            if timer.timeout is False:
                if punish_draw!=2 :
                    Play.create_button().draw(screen)

            #进入惩罚事件、渲染惩罚按钮，如果等于2则已经选完牌，进入完惩罚事件，所以不再渲染
            if(punish_draw!=2 ):
                if(nowround_scores<=0):
                    Draw.create_button().draw(screen)

        Text('Now Player' + str(player_pos), (1250, 30), 50, pygame.Color('yellow')).draw(screen)
        Text('Win Rules:first get 30 scores(easy to test) or out of your tiles' , (150, 10), 30, pygame.Color('red')).draw(screen)
        Text('Scores:' + str(scores), (700, 50), 50, pygame.Color('yellow')).draw(screen)


        pygame.draw.rect(screen, 'yellow', pygame.Rect(YELLOW_LINE_LEFT, YELLOW_LINE_TOP, 1500, 5))  # line
        for i in range(25):
            pygame.draw.rect(screen, 'yellow', pygame.Rect(0 + i * 60, 100, 2, 425 + 85))  # line
        # line to see
        for i in range(7):
            pygame.draw.rect(screen, 'yellow', pygame.Rect(0, 100 + i * 85, 1500, 2))  # line
        for event in pygame.event.get():
            if event.type == QUIT:
                # print(play)
                return
            if event.type == pygame.MOUSEBUTTONDOWN :
                x, y = event.pos
                # move tile( which tiles in player's rack)
                # Check if the click is within any tile in the player's rack
                for i, rack_info in enumerate(player_rack):
                    if rack_info["rect"].collidepoint(x, y):
                        # print("value:", rack_info["value"])
                        # print("color:", rack_info["color"])
                        # print("rect:", rack_info["rect"].collidepoint(x, y))
                        # print("i",i)
                        # Start dragging the clicked tile
                        dragging = True
                        dragged_tile_index = i
                        offset_x = x - rack_info["rect"].left
                        offset_y = y - rack_info["rect"].top

                # check whether tiles on table are moved or not
                for i, table_info in enumerate(Table):
                    if table_info.tile != None:
                        if table_info.tile["rect"].collidepoint(x, y):

                            t_dragging = True
                            t_dragged_tile_index = i
                            t_offset_x = x - table_info.tile["rect"].left
                            t_offset_y = y - table_info.tile["rect"].top

                for punish_card in punish_draw_list:
                    if punish_card["rect"].collidepoint(x, y):
                        player_rack.append(punish_card)
                        pool.remove(punish_card["ori"])
                        punish_draw_list.clear()
                        punish_draw=2
                        scores = (14 - len(player_rack)) * 5
                        nowround_scores = copy.deepcopy(scores)
                        if player_pos == 1:
                            p1_scores = scores
                        elif player_pos == 2:
                            p2_scores = scores
                        elif player_pos == 3:
                            p3_scores = scores
                        elif player_pos == 4:
                            p4_scores = scores
                        elif player_pos == 5:
                            p5_scores = scores




            elif event.type == pygame.MOUSEMOTION:
                pygame.display.set_caption(str(event.pos))
                x, y = event.pos
                if dragging:
                    player_rack[dragged_tile_index]["rect"].left = x - offset_x
                    player_rack[dragged_tile_index]["rect"].top = y - offset_y
                    if y>695:#drag to rack
                        player_rack[dragged_tile_index]["last_rect"].left = x - offset_x
                        player_rack[dragged_tile_index]["last_rect"].top = y - offset_y
                    # print("rect:", player_rack[dragged_tile_index]["rect"])
                if t_dragging:
                    Table[t_dragged_tile_index].tile["rect"].left = x - t_offset_x
                    Table[t_dragged_tile_index].tile["rect"].top = y - t_offset_y
                    print("table rect MOUSEMOTION:", Table[t_dragged_tile_index].tile["rect"])

            elif event.type == pygame.MOUSEBUTTONUP:
                # Stop dragging and play the tile at the final position
                x, y = event.pos
                if dragging:
                    player_rack[dragged_tile_index]["rect"].left = x - offset_x
                    player_rack[dragged_tile_index]["rect"].top = y - offset_y
                    dragging = False
                if t_dragging:
                    Table[t_dragged_tile_index].tile["rect"].left = x - t_offset_x
                    Table[t_dragged_tile_index].tile["rect"].top = y - t_offset_y
                    left_t = Table[t_dragged_tile_index].tile["rect"].left
                    top_t = Table[t_dragged_tile_index].tile["rect"].top
                    # calculate the coordinates
                    left_t_pos = int(left_t / 60)
                    top_t_pos = int((top_t - 100) / 85)
                    Table[top_t_pos * 25 + left_t_pos].tile = copy.deepcopy(Table[t_dragged_tile_index].tile)
                    Table[t_dragged_tile_index].tile = None
                    # print("left ", left, int(left / 60))
                    # print("top ", top, int((top - 100) / 85))
                    # print("new",Table[top_pos*25+left_pos].tile==None)
                    # print("orginal",Table[t_dragged_tile_index].tile==None)
                    # print("table rect MOUSEBUTTONUP:", Table[t_dragged_tile_index].tile["rect"])

                    t_dragging = False

        MOVE_LEFT = 520
        MOVE_TOP = PLAY_SQUARE_TOP + 7
        LINE1 = 100
        LINE2 = LINE1 + 90
        LINE3 = LINE2 + 90
        LINE4 = LINE3 + 90
        LINE5 = LINE4 + 90
        TABLE_LEFT = 30
        TABLE_LEFT2 = 745 + 20

        for gird in Table:
            item = gird.tile
            if item is not None:
                tile_image = pygame.image.load("tiles/" + item["tile_name"])
                resized_image = pygame.transform.scale(tile_image, (TILE_WEIGHT, TILE_HEIGHT))
                screen.blit(resized_image, (item["rect"].left, item["rect"].top))

        for item in player_rack:
            tile_image = pygame.image.load("tiles/" + item["tile_name"])
            resized_image = pygame.transform.scale(tile_image, (TILE_WEIGHT, TILE_HEIGHT))
            screen.blit(resized_image, (item["rect"].left, item["rect"].top))

        # prints tiles in the move section
        for item in move:
            tile_image = pygame.image.load("tiles/" + item["tile_name"])
            resized_image = pygame.transform.scale(tile_image, (TILE_WEIGHT, TILE_HEIGHT))
            screen.blit(resized_image, (MOVE_LEFT, MOVE_TOP))
            item["rect"] = pygame.Rect(MOVE_LEFT, MOVE_TOP, TILE_WEIGHT, TILE_HEIGHT)
            MOVE_LEFT += 59

        #当点击完后punish_draw变为1，等于1时可以进行渲染
        if punish_draw==1:
            for item in punish_draw_list:
                tile_image = pygame.image.load("tiles/" + item["tile_name"])
                resized_image = pygame.transform.scale(tile_image, (TILE_WEIGHT, TILE_HEIGHT))
                screen.blit(resized_image, (item["rect"].left, item["rect"].top))



        pygame.display.flip()
        # press change player function
        if (CHANGE_LEFT < X < CHANGE_RIGHT) and (
                CHANGE_TOP < Y < CHANGE_BOTTOM) and event.type == pygame.MOUSEBUTTONDOWN:
            nowround_scores=0#切人当前回合变为0
            timer.reset()
            punish_draw_list=[]
            punish_draw=0
            player_pos += 1
            score_pos += 1
            print("here")
            if player_pos > 3:
                # bigger than 5 begin with 1
                player_pos = 1
                score_pos = 1

            if player_pos == 1:
                player_rack = player_rack1
                scores = p1_scores

            elif player_pos == 2:
                player_rack = player_rack2
                scores = p2_scores

            elif player_pos == 3:
                player_rack = player_rack3
                scores = p3_scores

            elif player_pos == 4:
                player_rack = player_rack4
                scores = p4_scores

            elif player_pos == 5:
                player_rack = player_rack5
                scores = p5_scores

        # 30 mark easy to test获胜或者手牌为0
        if(scores>=30 or len(player_rack)==0):
            winner=True





        # When clicking on draw button, takes 2 tile from deck and prints them on the table
        if (DRAW_LEFT < X < DRAW_RIGHT) and (
                DRAW_TOP < Y < DRAW_BOTTOM) and event.type == pygame.MOUSEBUTTONDOWN:
            punish_draw = 1
            # print drawn card before added to deck






        # play and check tile ,leave the valid groups and runs on table
        if (20 < X < 165) and (750 < Y < 780) and event.type == pygame.MOUSEBUTTONDOWN:
            remove_rack_list = []
            print("player_rack:", len(player_rack))
            for tile in player_rack:
                print(tile["rect"].top)
                if tile["rect"].top < 610:
                    left = tile["rect"].left
                    top = tile["rect"].top
                    left_pos = int(left / 60)
                    top_pos = int((top - 100) / 85)
                    print("left ", left, int(left / 60))
                    print("top ", top, int((top - 100) / 85))

                    # table check and add
                    print(top_pos * 25 + left_pos)
                    gridNow = Table[top_pos * 25 + left_pos]
                    print(gridNow.left, gridNow.top)
                    # check  outline or not
                    print(tile["rect"].left >= gridNow.left)
                    print(tile["rect"].top >= gridNow.top)
                    print(tile["rect"].top + 75 <= gridNow.top + 85)
                    print(tile["rect"].left + 50 <= gridNow.left + 60)
                    print(tile["belong"] == "rack")
                    if (tile["rect"].left >= gridNow.left
                            and tile["rect"].top >= gridNow.top
                            and tile["rect"].top + 75 <= gridNow.top + 85
                            and tile["rect"].left + 50 <= gridNow.left + 60
                            and tile["belong"] == "rack"):

                        Table[top_pos * 25 + left_pos].tile = copy.deepcopy(tile)  # rack put to table (not doing check)
                        # Table[top_pos * 25 + left_pos].tile["rect"].left=
                        print("in table_tile rect", Table[top_pos * 25 + left_pos].tile["rect"])
                        remove_rack_list.append(tile)
                        # player_rack.remove(tile)
                    else:
                        print(tile["last_rect"])
                        tile["rect"] = copy.deepcopy(tile["last_rect"])
            for remove_rack in remove_rack_list:
                player_rack.remove(remove_rack)
            print("player_rack after:", len(player_rack))

            # 开始对每行检测 check
            total_list = []

            for i in range(6):
                print("into for", i * 25)
                row = copy.deepcopy(Table[i * 25:i * 25 + 25])
                while True:
                    check_list = []
                    for check in row:
                        if check.tile is not None and check.tile["selected"] == False:
                            check_list.append(check)
                            check.tile["selected"] = True
                            continue
                        else:
                            if len(check_list) > 0:
                                total_list.append(check_list)
                            row.remove(check)
                            break
                        # 加完一组重置
                    if len(row) == 0:
                        break
            final_result=True
            # final judge tag
            for check_list in total_list:
                valid_group_tag = True
                # init judge tag
                valid_runs_tag = True
                if len(check_list) < 3:
                    valid_runs_tag = False
                    valid_group_tag = False
                    final_result=False
                    break
                else:
                    firstValue = int(check_list[0].tile["value"])
                    print("firstValue")
                    firstColor = check_list[0].tile["color"]
                    print("firstColor")
                    for item in check_list:
                        if firstValue != int(item.tile["value"]):  # check group
                            valid_group_tag = False
                        if firstColor != item.tile["color"]:  # check runs color
                            valid_runs_tag = False

                    if valid_runs_tag is True:  # check runs rules
                        if checkVaild(check_list) is False:
                            valid_runs_tag = False
                if valid_group_tag == False and valid_runs_tag == False:
                        final_result==False

                    # no break ice, <3 \not valid ,so back 一行没有三张牌没破冰直接退  #(break_ice is False and len(check_list) < 3)or
            if len(total_list) > 0:
                if final_result==False:
                    print("bad job")
                    pygame.mixer.music.load('fail.mp3')
                    pygame.mixer.music.play()
                    for check_list in total_list:
                        for item in check_list:
                            if (item.tile["belong"] == "rack"):
                                print("back rack card")
                                item.tile["rect"] = copy.deepcopy(item.tile["last_rect"])
                                item.tile["selected"] = False  #reck status back ,for next time to use
                                player_rack.append(item.tile)
                                print(item.tile)
                    # back to pervious table
                    Table = copy.deepcopy(Table_previous)
                    print("not break ice ,cant play less than 3,invalid group or runs")
                else:
                    pygame.mixer.music.load('success.mp3')
                    pygame.mixer.music.play()
                    print("good job")
                    for check_list in total_list:
                        for valid_item in check_list:
                            # valid tile keep in table set belong=table and set last_rect=rect, it change rack to table
                            Table[valid_item.row * 25 + valid_item.col].tile["belong"] = "table"
                            Table[valid_item.row * 25 + valid_item.col].tile["last_rect"] = copy.deepcopy(
                                Table[valid_item.row * 25 + valid_item.col].tile["rect"])
                            print(valid_item.tile)
                        scores = (14 - len(player_rack)) * 5
                        nowround_scores = copy.deepcopy(scores)
                        if player_pos == 1:
                            p1_scores=scores
                        elif player_pos == 2:
                            p2_scores = scores
                        elif player_pos == 3:
                            p3_scores = scores
                        elif player_pos == 4:
                            p4_scores = scores
                        elif player_pos == 5:
                            p5_scores = scores
                    # save valid table
                    Table_previous = copy.deepcopy(Table)

            else:
                print("no job")

        pygame.display.flip()



        if winner is True :
            pygame.mixer.music.load('victory.mp3')
            pygame.mixer.music.play()
            break
    while True:
        Text('You Win Player:'+str(player_pos), (150, 300), 200, pygame.Color('darkred')).draw(screen)
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == QUIT:
                return


run_game()
pygame.quit()
