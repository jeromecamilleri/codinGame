import sys
import math
# Création d'un tableau racine
racine = []

def chercheNum(tab, num):
    i=0 
    for elt in tab: 
      if elt == []:
        return -1
      elif elt[0]==num:
         return i
      else:
         i += 1
    return -1

n = int(input())
nbAjout = 0

for i in range(n):
    telephone = input()
    print("Debug telephone... " + telephone , file=sys.stderr, flush=True)
    tab = racine # on réinitialise à chaque numero
    for car in telephone:
        indNum = chercheNum(tab, car)
        if indNum == -1:
           tab.append([car, []])
           nbAjout += 1
           tab = tab[-1][1]
        else:
           tab = tab[indNum][1]
        
print(str(nbAjout))
#Sortie standard :
#Debug telephone... 0412578440
#Debug telephone... 0412199803
#Debug telephone... 0468892011
#Debug telephone... 112
#Debug telephone... 15
#28
#Success
