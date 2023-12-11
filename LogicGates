# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

## Version Bash
## extrement pénible/long/fastidieux a ecrire (et abandonner après le premier test passe !!)
## pas de possibilite de donner un tableau en parametre de fonctions
## uniquement des chaines => oblige a utiliser des variables globales
## Idem pour le retour de fonctions pas prévu autre chose que le code retour (0 ou 1)
## ecriture avec des espaces qui sont importants pour les conditions de IF ou affectarion (sans espace)


read -r n
read -r m
echo "Debug messages...n="  $n " / m="  $m>&2
for (( i=0; i<$n; i++ )); do
    read -r inputName inputSignal
    #tab_in[${#tab_in[*]}]=[$inputName]=$inputSignal
    tab_in[${#tab_in[*]}]=$inputName
    tab_in[${#tab_in[*]}]=$inputSignal
done
for (( i=0; i<$m; i++ )); do
    read -r outputName _type inputName1 inputName2
    declare -a tab_ind
    tab_out[${#tab_out[*]}]=$outputName
    tab_out[${#tab_out[*]}]=$_type
    tab_out[${#tab_out[*]}]=$inputName1
    tab_out[${#tab_out[*]}]=$inputName2
    #echo "Debug output..."  $outputName " / "  $_type " / " $inputName1 " / " $inputName2  >&2
done


function afficheTab() { # impossible de passer des arguments autre que chaine a cette fonction
                        # on utilise le nom de la variable tableau de type global !!!!
  if [ $1 ]; then
    z=($(eval echo $(echo \${$1[@]})))  # magique mais j'avoue n'y rien comprendre
    for i in ${!z[*]}; do
       echo "tab $1 $i => "  ${z[i]}>&2
    done
  else
     return 1
  fi
  return 0
}


function convertieChaineBooleen() {
   # $1 est la chaine de _ et - a traduire en booleen
    if [ $1 ]; then
      entree=$1
      sortie="${entree//_/0}"  # enfin le cote pratique de la substitution
      sortie="${sortie//-/1}"
    else
       return 1
    fi
    return 0
}


function convertieBooleenChaine() {
   # $1 est la chaine de 0 et 1 en _ et -
    if [ $1 ]; then
      entree=$1
      sortie="${entree//0/_}"
      sortie="${sortie//1/-}"
    else
       return 1
    fi
    return 0
}


function opLogiqueChaines() {
   # $1 $1 deux chaines booleen a operer avec l operateur $3 logiquement
    if [ $1 ] && [ $2 ]; then
      entree1=$1
      entree2=$2
      op=$3
      sortie=""
      for L in $(seq 1 ${#entree1}); do
         car1="$(echo $entree1 | cut -c$L)"
         car2="$(echo $entree2 | cut -c$L)"
         if [ $op = "OR" ]; then  ### attention aux espaces autour du = et des []
            if [ $car1 = "0" ] && [ $car2 = "0" ]; then
               car3="0"
            else
               car3="1"
            fi
         elif [ $op = "AND" ]; then
            if [ $car1 = "1" ] && [ $car2 = "1" ]; then
               car3="1"
            else
               car3="0"
            fi
         elif [ $op = "XOR" ]; then
            if [ $car1 = "1" ] && [ $car2 = "1" ]; then
               car3="0"
            elif [ $car1 = "0" ] && [ $car2 = "0" ]; then
               car3="0"
            else
               car3="1"
            fi
         fi
         sortie=$sortie$car3
         #echo "car" $car1 $car2 $car3 $op>&2
       done
    else
       return 1
    fi
    return 0
}


afficheTab tab_in || echo "erreur">&2
afficheTab tab_out || echo "erreur">&2


#echo "C ____-_____-_____-_____-___"
#echo "D __-----_-----_-----_-----_"      
#echo "E __--_--_--_--_--_--_--_--_"


convertieChaineBooleen ${tab_in[1]} # valeur de A simplication !
chaine1=$sortie
convertieChaineBooleen ${tab_in[3]} # valeur de B simplication
chaine2=$sortie


for (( i=0; i<$m; i++ )); do


    # Write an answer using echo
    # To debug: echo "Debug messages..." >&2


    opLogiqueChaines $chaine1 $chaine2 ${tab_out[4*i+1]}
    convertieBooleenChaine $sortie    
    echo -e "${tab_out[i*4]} $sortie"
done


##Debug messages...n= 2  / m= 3
##tab tab_in 0 =>  __---___---___---___---___
##tab tab_in 1 =>  ____---___---___---___---_
##tab tab_out 0 =>  C
##tab tab_out 1 =>  AND
##tab tab_out 2 =>  A
##tab tab_out 3 =>  B
##tab tab_out 4 =>  D
##tab tab_out 5 =>  OR
##tab tab_out 6 =>  A
##tab tab_out 7 =>  B
##tab tab_out 8 =>  E
##tab tab_out 9 =>  XOR
##tab tab_out 10 =>  A
##tab tab_out 11 =>  B
##C ____-_____-_____-_____-___
##D __-----_-----_-----_-----_
##E __--_--_--_--_--_--_--_--_
##Success
