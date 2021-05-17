xo = 0
yo = 1

x = xo
y = yo


h = 0.00001
e = 10**-4

def df(x, y):
    return -x * (y**4 + 1) / (2 * (x * y + y))

# Используется метод степенных рядов с модификацией Эйлера (p = 1)
def Tayl(func):
    return func

def itr(xo, yo, h, teyl):
    return yo + h * teyl

while abs(itr(x, y, h, Tayl(df(x, y)))) > e:
    y = itr(x, y, h, Tayl(df(x, y)))
    x += h

print(itr(x, y, h, Tayl(df(x, y))))
print(x)