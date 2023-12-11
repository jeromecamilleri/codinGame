import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def afficherTabSortieErr(name,tab):
   print(name+ " len :" + str(len(tab)) , file=sys.stderr, flush=True)
   i=0
   for elt in tab:
      print(name+ " " + str(i) + ":"+str(elt), file=sys.stderr, flush=True)
      i=i+1

def cherche_tous_chemins(graphe, depart,arrivee):
    """
    recherche tous les chemins dans un graphe depuis un sommet de départ vers un sommet d'arrivée
    :param graphe: une liste d'adajence du graphe étudié (un dictionnaire)
    :param depart: le sommet de départ pour le chemin recherché
    :param arrivee: le sommet d'arrivée pur le chemin recherché
    :return: la liste des sommets du graphe
    """
    chemins = []
    print("cherche_tous_chemins...len(graphe)"+str(len(graphe)) + "/" + str(depart) + "/" +str(arrivee), file=sys.stderr, flush=True)
    if depart <0 | arrivee <0 | arrivee >= len(graphe) | depart >= len(graphe):
        return chemins
    pile = [(depart,[depart])]
    chemin = []
    while len(pile) != 0:
        sommet,chemin = pile.pop()
        #print("cherche_tous_chemins)"+str(sommet) + "/" + str(chemin) , file=sys.stderr, flush=True)
        liste_nouveaux_sommets_voisins = [voisin for voisin in graphe[sommet] if not(voisin in chemin)]
        for voisin in liste_nouveaux_sommets_voisins:
            if voisin == arrivee:
                chemins.append(chemin + [arrivee])
                return chemins
            pile.append((voisin,chemin + [voisin]))
    return chemins

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]
print("Debug messages..."+str(n)+"/"+str(l)+"/"+str(e), file=sys.stderr, flush=True)

nodes=[[]]*n # initialisation tableau de tableau pour stocker le graphe (pas le plus économe)
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1,n2 = [int(j) for j in input().split()]
   
    nodes[n1] = nodes[n1] + [n2]  
    nodes[n2] = nodes[n2] + [n1] # chemins bi-directionels

afficherTabSortieErr("nodes",nodes)

sorties=[]
for i in range(e):
    sorties.append(int(input()))  # the index of a gateway node
afficherTabSortieErr("sorties",sorties)

# game loop
while True:
    si = int(input())  # The index of the node on which the Bobnet agent is positioned this turn
    print("Debug si..."+str(si), file=sys.stderr, flush=True)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    sortiesProche=sorties[0]
    for sortie in sorties:
        if sortie in nodes[si]:
           sortiesProche = sortie

    print("sortie proche = "+str(sortiesProche), file=sys.stderr, flush=True)        
    chemins = cherche_tous_chemins(nodes, si, sortiesProche)
    afficherTabSortieErr("Chemins trouvés :",chemins)
    if len(chemins) != 0:
         print(str(chemins[0][0]) + " " + str(chemins[0][1]))
   

