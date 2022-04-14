# coding=utf-8
# author Cool_Breeze
 
import ctypes
import msvcrt
from time import sleep
from os import system
from random import randrange
from collections import deque
from threading import Thread
 
# 位置信息结构体
class point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_short),
                ('y', ctypes.c_short)]
 
def gotoXYPrint(coord, char):
    global MAINHANDLE
    global HEADICON
    global FOODICON
    ctypes.windll.kernel32.SetConsoleCursorPosition(
        MAINHANDLE, coord)
    if char == HEADICON:
        ctypes.windll.kernel32.SetConsoleTextAttribute(
        MAINHANDLE, 14)
    elif char == FOODICON:
        ctypes.windll.kernel32.SetConsoleTextAttribute(
        MAINHANDLE, 12)
    else:
        ctypes.windll.kernel32.SetConsoleTextAttribute(
        MAINHANDLE, 11)
    print(char, end='', flush=True)
 
 
# 边框
def side():
    for n in range(WIDTH-1):
        gotoXYPrint(point(n,0), '+')
        gotoXYPrint(point(n,HIGHT-1), '+')
    for n in range(HIGHT-1):
        gotoXYPrint(point(0,n), '+')
        gotoXYPrint(point(WIDTH-1,n), '+')
 
def createFood():
    global SNAKE
    global FOODPOINT
    off = False
    while True:
        x = randrange(1, WIDTH-1)
        y = randrange(1, HIGHT-1)
        for n in SNAKE:
            if n.x == x and n.y == y:
                continue
            else:
                FOODPOINT.x = x
                FOODPOINT.y = y
                gotoXYPrint(FOODPOINT, FOODICON)
                off = True
        if off: break
 
def createSnake():
    global SNAKE
    x, y = WIDTH//2, HIGHT//2
    for n in range(3):
        t = point(x+n, y)
        SNAKE.append(t)
        gotoXYPrint(t, HEADICON)
 
def update():
    for i in SNAKE:
        gotoXYPrint(i, HEADICON)
 
def _exit(info):
    input(info)
    exit()
     
def collision():
    global SNAKE
    head = SNAKE[0]
    count = 0
    for n in SNAKE:
        count += 1
        if count == 1: continue
        if n.x == head.x and n.y == head.y:
            _exit('游戏结束！')
             
    if head.x == 0 or head.y == 0 or \
       head.x == WIDTH-1 or head.y == HIGHT-1:
       _exit('游戏结束！')
 
def moveSnake():
    '''
    K == ←
    M == →
    H == ↑
    P == ↓
    '''
    global DIRECTION
    global SNAKE
    global FOODPOINT
     
    if DIRECTION == 'K':
        SNAKE.appendleft(point(SNAKE[0].x-1, SNAKE[0].y))
    elif DIRECTION == 'M':
        SNAKE.appendleft(point(SNAKE[0].x+1, SNAKE[0].y))
    elif DIRECTION == 'H':
        SNAKE.appendleft(point(SNAKE[0].x, SNAKE[0].y-1))
    elif DIRECTION == 'P':
        SNAKE.appendleft(point(SNAKE[0].x, SNAKE[0].y+1))
    # 其他按键不做任何动作
    else: return None
    collision()
    # 是否吃到食物
    if SNAKE[0].x != FOODPOINT.x or SNAKE[0].y != FOODPOINT.y:
        gotoXYPrint(SNAKE.pop(), ' ')
    else:
        createFood()
     
    update()
     
# 长按加速
def Speed():
    global SPEED
    global ORDKEY
    global DIRECTION
     
    while True:
        sleep(0.001)
        if msvcrt.kbhit():
            inputKey = msvcrt.getwch()
            # 特殊按键
            if inputKey == '\000' or inputKey == '\xe0':
                inputKey = msvcrt.getwch()
                if DIRECTION == 'K' and inputKey == 'M': continue
                elif DIRECTION == 'M' and inputKey == 'K': continue
                elif DIRECTION == 'H' and inputKey == 'P': continue
                elif DIRECTION == 'P' and inputKey == 'H': continue
            if DIRECTION == inputKey:
                if SPEED >= 0.02:
                    SPEED -= 0.02
            else:
                DIRECTION = inputKey
                SPEED = 0.1
 
HIGHT = 26
WIDTH = 60
MAINHANDLE = ctypes.windll.kernel32.GetStdHandle(-11)
SNAKE = deque([])
HEADICON = 'O'
FOODICON = '$'
FOODPOINT = point()
 
DIRECTION = 'K'
 
system(f'mode con cols={WIDTH} lines={HIGHT}')
system("title 贪吃蛇游戏")
# 隐藏光标
ctypes.windll.kernel32.SetConsoleCursorInfo(
    MAINHANDLE, ctypes.byref(point(1,0)))
     
SPEED = 0.1
ORDKEY = None
def main():
    global DIRECTION
    global SPEED
    side()
    createSnake()
    createFood()
    InputThead = Thread(target=Speed, daemon=True)
    InputThead.start()
    while True:
        moveSnake()
        sleep(SPEED)
 
 
if __name__ == '__main__':
    main()
