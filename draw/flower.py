import turtle as t
t.color('red')
for i in range(270):
    t.fd(i)
    t.left(70)

ts = t.getscreen()
ts.getcanvas().postscript(file = str(__name__) + ".eps")
t.done