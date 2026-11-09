import sys
import math

# Grow and multiply your organisms to end up larger than your opponent.

# width: columns in the game grid
# height: rows in the game grid
width, height = [int(i) for i in input().split()]

bouffeAX=0
bouffeAY=0
# game loop

while True:
    trouve=False
    entity_count = int(input())
    for i in range(entity_count):
        inputs = input().split()
        x = int(inputs[0])
        y = int(inputs[1])  # grid coordinate
        _type = inputs[2]  # WALL, ROOT, BASIC, TENTACLE, HARVESTER, SPORER, A, B, C, D
        owner = int(inputs[3])  # 1 if your organ, 0 if enemy organ, -1 if neither
        organ_id = int(inputs[4])  # id of this entity if it's an organ, 0 otherwise
        organ_dir = inputs[5]  # N,E,S,W or X if not an organ
        organ_parent_id = int(inputs[6])
        organ_root_id = int(inputs[7])
        if not trouve and _type == "A" and owner != 1 and owner !=0:
            print("WHILE =" + str(x)+","+str(y), file=sys.stderr, flush=True)
            bouffeAX=x
            bouffeAY=y          
            trouve=True
            
    # my_d: your protein stock
    my_a, my_b, my_c, my_d = [int(i) for i in input().split()]
    # opp_d: opponent's protein stock
    opp_a, opp_b, opp_c, opp_d = [int(i) for i in input().split()]
    required_actions_count = int(input())  # your number of organisms, output an action for each one in any order
    print("DEBUG =" + str(entity_count) + " my_a=" +  str(my_a) +","+str(my_b) + str(my_c) + str(my_d) + "reqaccount=" + str(required_actions_count), file=sys.stderr, flush=True)
    
    for i in range(required_actions_count):
    
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        if my_a < 5:
            # bouffer des proteines A
            print("GROW 10 " + str(bouffeAX) + " "+ str(bouffeAY)+" BASIC")
        else:
            print("GROW 1" +" 16 4 BASIC")
