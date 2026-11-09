LA RÉSISTANCE - CODE GOLF (the-resistance-codesize)
====================================================

Page : https://www.codingame.com/codegolf/expert/the-resistance-codesize
Principe : compter les messages obtenus en découpant une séquence Morse avec les mots d'un dictionnaire.
Score code golf = nombre de caractères du code, le plus court gagne (classement par langage).

Dossier : laResistance-codegolf/
  golf.py          solution golfée (Python 3) ; 345 octets au dernier essai, 6/6 tests CodinGame OK
  ref.py           version lisible de référence (même algorithme : programmation dynamique sur les préfixes)
  run_tests.py     tests locaux : exemple du sujet + 200 cas aléatoires vs force brute + grand cas (99 999 car.)
  run-api-tests.sh test games CodinGame (6 cas, vrai validateur)
  run-view.sh      visualiseur web local -> http://localhost:8888/viewer.html
  viewer.html      page graphique : tableau de comptage f[i] et découpages mot par mot
  statement.md, puzzle.json   énoncé et métadonnées (API CodinGame)

Un code golf n'a pas de referee de jeu : "local" = tests de sortie + visualiseur maison (pas de simulateur officiel).

1) Tests locaux
   python3 run_tests.py                 # golf.py et ref.py
   python3 run_tests.py autre.py        # un autre fichier
   - affiche "N/N OK, plus lent X s, Y octets" ; le compte d'octets est celui du fichier (retour final compris)

2) Visualiseur graphique
   ./run-view.sh [port]  puis ouvrir http://localhost:8888/viewer.html
   - coller une entrée au format du jeu (séquence, N, N mots) puis "Calculer"
   - vert = préfixes atteignables ; les blocs affichent les mots et leur code Morse

3) Tests sur CodinGame (un test à la fois, 30 par minute max)
   ./run-api-tests.sh [fichier.py] [N ...]     # défaut golf.py sur les cas 1 à 6
   - sortie : success, found/expected (première ligne différente), erreur ou timeout
   - cas : 1 lettre, 2 mot, 3 simples messages, 4 séquence longue + grand dictionnaire, 5 même code pour différents mots, 6 nombreuses possibilités

4) Soumettre (classement code golf) - seulement quand une version est plus courte
   jq -n --rawfile code golf.py '{language:"Python3",code:$code}' | curl -s -X POST \
     -H "Authorization: Bearer $(cat ~/.config/codingame/token)" -H 'Content-Type: application/json' \
     --data-binary @- https://www.codingame.com/api/v1/puzzles/the-resistance-codesize/submissions
   - suivi : GET /puzzles/the-resistance-codesize/progress (score, rank, in_progress)
   - rien n'a été soumis pour l'instant

Contraintes du sujet : séquence < 100 000 caractères, N < 100 000 mots, mots < 20 lettres, R < 2^63.
Pistes de golf : raccourcir la table Morse, supprimer le dictionnaire de comptage, autres langages (le classement est par langage).

Voir aussi : ../README.md (outils partagés)

ALGORITHME A MAITRISER (analyse du problème)
  - Programmation dynamique sur préfixes : f[i] = nombre de découpages du préfixe de longueur i ; f[i+len(m)] += f[i] pour chaque mot m codé en Morse qui commence en i. Complexité O(L x K) avec K = longueur max d'un code Morse de mot (<= 76), grâce à une table code -> nombre de mots.
  - Hachage / dictionnaire : traduire chaque mot en Morse et compter les mots ayant le même code (plusieurs mots de même code : on additionne leur nombre dans la table).
  - Comptage de chemins dans un DAG ; débordement d'entiers (R < 2^63).
  - Code golf : en plus, choix des structures les plus courtes du langage (table Morse compacte, expressions, boucle minimale).
