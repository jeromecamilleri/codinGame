import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def convert_chaine_binaire(chaineE):
    str_bin = ""
    for caractere in chaineE:
       if caractere == "_":
            str_bin = str_bin + "0"
       else:
            str_bin = str_bin + "1"
    return str_bin

def convert_binaire_chaine(chaineS):
    str_bin = ""
    for caractere in chaineS:
       if caractere == "0":
            str_bin = str_bin + "_"
       else:
            str_bin = str_bin + "-"
    return str_bin

def opBinaire_chaine(chaine1, chaine2, op):
    str_bin = ""
    i=0
    for caractere in chaine1:
        if (op=="AND"):
            if caractere == "1" and chaine2[i] == "1":
               str_bin = str_bin + "1"
            else:
                str_bin = str_bin + "0"
        if (op=="OR"):
            if caractere == "0" and chaine2[i] == "0":
               str_bin = str_bin + "0"
            else:
                str_bin = str_bin + "1"
        if (op=="XOR"):
            if caractere == "1" and chaine2[i] == "1":
               str_bin = str_bin + "0"
            elif  caractere == "0" and chaine2[i] == "0":     
                str_bin = str_bin + "0"
            else:
                str_bin = str_bin + "1" 
        if (op=="NAND"):
           if caractere == "1" and chaine2[i] == "1":
             str_bin = str_bin + "0"
           else:
             str_bin = str_bin + "1"
        if (op=="NOR"):
           if caractere == "0" and chaine2[i] == "0":
             str_bin = str_bin + "1"
           else:
             str_bin = str_bin + "0"   
        if (op=="NXOR"):
           if caractere == "1" and chaine2[i] == "1":
              str_bin = str_bin + "1"
           elif  caractere == "0" and chaine2[i] == "0":     
                str_bin = str_bin + "1"
           else:
                str_bin = str_bin + "0"                   
        i=i+1
            
    return str_bin

def valInputSignal(entrees, nom):
    for ligne in entrees:
        if (nom==ligne[0]):
            return ligne[1]

n = int(input())
m = int(input())
entrees = []*n
for i in range(n):
    input_name, input_signal = input().split()
    entrees.append([input_name, input_signal])

sorties = []*m
for i in range(m):
    output_name, _type, input_name_1, input_name_2 = input().split()
    sorties.append([output_name, _type, input_name_1, input_name_2])

for i in range(m):

    # Write an answer using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
   
    val1 = valInputSignal(entrees, sorties[i][2])
    val2 = valInputSignal(entrees, sorties[i][3])
    val3 = convert_binaire_chaine(opBinaire_chaine(convert_chaine_binaire(val1), convert_chaine_binaire(val2), sorties[i][1]))
    print(sorties[i][0]+ " " + val3)
