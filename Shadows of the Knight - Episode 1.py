import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in input().split()]
print("Debug messages..." + str(x0) + " / " + str(y0) + " / w=" + str(w) + ", h=" + str(h), file=sys.stderr, flush=True)
# game loop
x = x0
y = y0
x1 = 0
y1 = 0
x2 = w - 1
y2 = h - 1
while True:
    BOMB_DIR = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print("Direction bombe :" + BOMB_DIR, file=sys.stderr, flush=True)

    if "U" in BOMB_DIR:
       y2 = y - 1
    elif "D" in BOMB_DIR:
       y1 = y + 1

    if "L" in BOMB_DIR:
       x2 = x - 1
    elif "R" in BOMB_DIR:
       x1 = x + 1

    x = round(x1 + (x2 - x1) / 2)
    y = round(y1 + (y2 - y1) / 2)

    if y < 0:
        y = 0
    if x < 0:
        x = 0
    if y >= h:
       y = h - 1
    if x >= w:
        x = w - 1  
   
    print(str(x) + " " + str(y))  
#    print("Debug messages..." + "xp=" + str(xp) + ", yp=" + str(yp), file=sys.stderr, flush=True)
 
    # the location of the next window Batman should jump to.
