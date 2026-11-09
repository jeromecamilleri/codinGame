m=".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()
s=input()
d={}
for _ in range(int(input())):
 w="".join(m[ord(c)-65]for c in input());d[w]=d.get(w,0)+1
n=len(s)
f=[1]+[0]*(n+80)
K={len(k)for k in d}
for i in range(n):
 for k in K:f[i+k]+=f[i]*d.get(s[i:i+k],0)
print(f[n])
