![](//cdn.codingame.com/smash-the-code/statement/league_wood_04.png)

Ce challenge est basé sur un système de ligues.

Pour ce challenge, plusieurs ligues pour le même jeu seront disponibles. Quand vous aurez prouvé votre valeur contre le premier Boss, vous accéderez à la ligue supérieure et débloquerez de nouveaux adversaires.

**NOUVEAU :** votre bot se battera uniquement avec le Boss une fois dans l'arène. Gagnez plus souvent que lui sur 5 matchs pour avancer jusqu'à la ligue finale.

## Congratulations

Votre organisme peut **croître** !

Cependant, les **sources de protéines** sur la grille sont limitées, et une fois que vous les absorbez, celles-ci disparaissent. C'est là que le type d'organe `HARVESTER` entre en jeu.

![Grow your organism to become the largest!](https://static.codingame.com/servlet/fileservlet?id=132395829688056)

*L'organe HARVESTER.*

## Règles du HARVESTER

À partir de cette ligue, les organes que vous placez auront une `direction`.

![](https://static.codingame.com/servlet/fileservlet?id=132395760074979)

*Cette commande crééra un nouveau `HARVESTER` faisant face à `N` (Nord).*

Si un `HARVESTER` fait face à une case avec une **source de protéines**, vous recevrez `1` de cette protéine à **chaque fin de tour**.

*Note : chaque joueur gagne seulement `1` protéine par source par tour, même si plusieurs `HARVESTER` sont dirigés vers cette source.*

Pour faire pousser un `HARVESTER`, vous avez besoin de `1` protéine de type `C` et `1` protéine de type `D`.

Dans cette ligue, on vous fourni `1` protéine de type `C` et `1` protéine de type `D`, **utilisez-les pour faire pousser un `HARVESTER` à l'endroit adapté pour faire croître votre organisme indéfiniment !**

*De nouvelles informations ont été ajoutées à la section **Protocole de jeu.***

## Règles

Le jeu se déroule sur une grille.

Pour les premières ligues, il suffit de battre le Boss dans des situations spécifiques.

### 🔵🔴 Les Organismes

Les **Organismes** sont composés d'**organes** occupant `une` case d'espace sur la grille de jeu.

Chaque joueur commence avec un organe de type `ROOT`. Votre organisme peut faire pousser (`GROW`) un nouvel organe à chaque tour afin de couvrir une plus large surface.

Un nouvel organe peut pousser **depuis** n'importe quel **organe** existant, vers un **emplacement adjacent libre**.

Afin d'utiliser l'action `GROW`, votre organisme a besoin de **protéines**. Faire pousser 1 organe `BASIC` nécessite `1` protéine de type A.

Vous pouvez obtenir plus de **protéines** en faisant pousser un organe sur une case de la grille contenant une **source de protéine** ; celles-ci sont des cases avec une lettre à l'intérieur. Faire ceci vous octroiera `3` protéines du type correspondant.

Votre organisme peut recevoir les commandes suivantes:

- `GROW id x y type`: créé un nouvel organe à la position `x`, `y` depuis un organe ayant l'id `id`. Si la position cible n'est pas voisine de `id`, l'organe sera créé sur le plus court chemin vers `x`, `y`.

  ![](https://static.codingame.com/servlet/fileservlet?id=132395721182727)

  *Cette commande va créer un nouvel organe `BASIC` depuis l'organe `ROOT` parent.*

Voir la section **Protocole de jeu** pour plus d'informations sur l'envoi de commandes à votre organisme.

### ⛔ Fin du jeu

Le jeu se termine quand il détecte qu'aucun progrès ne peut plus être fait ou après `100` tours.

### Conditions de victoire

### Conditions de défaite

### 🐞 Conseils de débogage

- Survolez la grille pour voir plus d'informations sur les organes sous votre curseur.
- Ajoutez du texte à la fin d'une instruction pour afficher ce texte au dessus de votre organisme.
- Cliquez sur la roue dentée pour afficher les options visuelles supplémentaires.
- Utilisez le clavier pour contrôler l'action : espace pour play / pause, les flèches pour avancer pas à pas.

Cliquez pour agrandir
## Protocole de jeu

### Entrées d'Initialisation

Première ligne : deux entiers `width` et `height` pour la taille de la grille.

### Entrées pour un tour de jeu

Première ligne : un entier `entityCount` pour le nombre d'entités sur la grille.
Prochaines `entityCount` lignes : Les `7` entrées suivantes pour chaque entité :

- `x` : Position X (`0` commence à gauche)
- `y` : Position Y (`0` commence en haut)
- `type` :

- `WALL` pour un mur
- `ROOT` pour un organe de type ROOT
- `BASIC` pour un organe de type BASIC
- `HARVESTER` pour un organe de type HARVESTER
- `A` pour une source de protéine A
- `owner` :

- `1` si vous êtes le propriétaire de cet organe
- `0` si votre adversaire est le propriétaire de cet organe
- `-1` si cette entité n'est pas un organe
- `organId` : id unique de cette entité si c'est un organe, `0` sinon.
- `organDir` : `N`, `W`, `S`, ou `E` pour la direction vers laquelle cet organe fait face
- `organParentId` : si c'est un organe, l'`organId` de l'organe dont cet organe est issu (0 pour les organes `ROOT`), `0` sinon.
- `organRootId` : si c'est un organe, l'`organId` de l'organe `ROOT` ancêtre de cet organe, `0` sinon.

Prochaine ligne : `4` entiers : `myA`,`myB`,`myC`,`myD` pour les quantités de chaque protéine que vous possédez.
Prochaine ligne : `4` entiers : `oppA`,`oppB`,`oppC`,`oppD` pour les quantités de chaque protéine que votre adversaire possède.
Prochaine ligne : un entier `requiredActionsCount` égal à `1` *pour cette ligue*.

### Sortie

Une ligne par organisme avec son action :

- `GROW id x y type direction` : tenter de faire pousser un nouvel organe de type `type` à la position `x`, `y` depuis l'organe `id`. Si la position cible n'est pas voisine de `id`, l'organe sera créé sur le plus court chemin vers `x`, `y`.
- `WAIT` : ne rien faire.

Ajoutez du texte après votre commande et celui-ci sera affiché sur le viewer.

### Contraintes

Temps de réponse par tour ≤ `50`ms
Temps de réponse pour le premier tour ≤ `1000`ms

![](//cdn.codingame.com/smash-the-code/statement/league_wood_04.png)

Qu'est-ce qui m'attend dans les ligues suivantes ?

Les règles supplémentaires disponibles dans les ligues supérieures seront les suivantes:

- Un type d'organe pour attaquer votre adversaire
- Un type d'organe pour engendrer d'autres organismes

## Pour Démarrer

Pourquoi ne pas se lancer dans la bataille avec l'un de ces **bots de base**, fournis par l'équipe :

- JavaScript https://gist.github.com/CGjupoulton/8c9f5b64a5d4967402b53a0bb526e167
- Java https://gist.github.com/CGjupoulton/6bfad6a5e62d61bdfe36a593f21833a4
- Python https://gist.github.com/CGjupoulton/9b15eca86001975297e6a1290a301dd1
- TypeScript https://gist.github.com/CGjupoulton/76039cf5cccb9811a04f83c2f14bced6

Vous pouvez les modifier selon votre style, ou les prendre comme exemple pour tout coder à partir de zero.

Une seule ligne avec votre action :
