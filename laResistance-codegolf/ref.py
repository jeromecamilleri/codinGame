"""Version lisible (référence) : nombre de messages possibles pour une séquence Morse et un dictionnaire."""
M = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()

s = input()
d = {}
for _ in range(int(input())):
    w = "".join(M[ord(c) - 65] for c in input())
    d[w] = d.get(w, 0) + 1

n = len(s)
f = [1] + [0] * n  # f[i] = nombre de façons d'écrire le préfixe s[:i]
lengths = {len(k) for k in d}
for i in range(n):
    if f[i]:
        for L in lengths:
            if i + L <= n:
                f[i + L] += f[i] * d.get(s[i:i + L], 0)
print(f[n])
