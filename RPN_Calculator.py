import tkinter as tk
import math as m
import Pile as p


TOUCHES = {'OFF': {'x1': 326, 'y1': 608, 'x2': 377, 'y2': 658},
           '+/-': {'x1': 18, 'y1': 606, 'x2': 71, 'y2': 657},
           '0': {'x1': 89, 'y1': 606, 'x2': 141, 'y2': 657},
           '.': {'x1': 157, 'y1': 606, 'x2': 212, 'y2': 657},
           '1': {'x1': 18, 'y1': 540, 'x2': 71, 'y2': 591},
           '2': {'x1': 89, 'y1': 540, 'x2': 141, 'y2': 591},
           '3': {'x1': 157, 'y1': 540, 'x2': 212, 'y2': 591},
           '4': {'x1': 18, 'y1': 474, 'x2': 71, 'y2': 524},
           '5': {'x1': 89, 'y1': 474, 'x2': 141, 'y2': 524},
           '6': {'x1': 157, 'y1': 474, 'x2': 212, 'y2': 524},
           '7': {'x1': 18, 'y1': 408, 'x2': 71, 'y2': 458},
           '8': {'x1': 89, 'y1': 408, 'x2': 141, 'y2': 458},
           '9': {'x1': 157, 'y1': 408, 'x2': 212, 'y2': 458},
           '+': {'x1': 245, 'y1': 474, 'x2': 289, 'y2': 524},
           '*': {'x1': 245, 'y1': 540, 'x2': 289, 'y2': 591},
           '-': {'x1': 322, 'y1': 474, 'x2': 376, 'y2': 524},
           '/': {'x1': 322, 'y1': 540, 'x2': 376, 'y2': 591},
           'ENTER': {'x1': 240, 'y1': 409, 'x2': 384, 'y2': 455},
           'CLEAR': {'x1': 24, 'y1': 343, 'x2': 79, 'y2': 394},
           'xy': {'x1': 245, 'y1': 343, 'x2': 299, 'y2': 394},
           '<-': {'x1': 319, 'y1': 343, 'x2': 372, 'y2': 394},
           'x^2': {'x1': 24, 'y1': 281, 'x2': 79, 'y2': 332},
           'sqrt': {'x1': 24, 'y1': 212, 'x2': 79, 'y2': 261},
           'y^x': {'x1': 98, 'y1': 281, 'x2': 152, 'y2': 332},
           '1/x': {'x1': 98, 'y1': 212, 'x2': 152, 'y2': 261},
           'LOG': {'x1': 171, 'y1': 3281, 'x2': 225, 'y2': 332},
           '10^x': {'x1': 171, 'y1': 212, 'x2': 225, 'y2': 261},
           'LN': {'x1': 245, 'y1': 281, 'x2': 299, 'y2': 332},
           'e^x': {'x1': 245, 'y1': 212, 'x2': 299, 'y2': 261},
           'RCL': {'x1': 319, 'y1': 332, 'x2': 372, 'y2': 332},
           'STO': {'x1': 319, 'y1': 212, 'x2': 372, 'y2': 261}
           }

def clicMouse(event):
    """Détecte les clics de la souris dans la calcualtrice"""
    global pile
    for t in TOUCHES:
        x1 = TOUCHES[t]['x1']
        x2 = TOUCHES[t]['x2']
        y1 = TOUCHES[t]['y1']
        y2 = TOUCHES[t]['y2']
        if x1 < event.x < x2 and y1 < event.y < y2:
                touchePressee(t, pile)
                break

def val(chaine):
    return float(chaine) if '.' in chaine else int(chaine)

def values_for_op(p, n, X):
    """Renvoie deux valeurs: soit la valeur en cours d'entrée et la première valeur
    de la pile, soit les deux premières valeurs de la pile si aucune n'est en cours
    d'entrée
    p : pile
    n : nombre de valeurs à renvoyer (n peut-être égal à 1 ou 2)
    X : valeur en cours d'entrée. Si elle est vide, on prend toutes les
        valeurs dans la pile"""
    if X == '':
        X = p.depiler() if not p.est_vide() else '0'
    if n == 2:
        Y = p.depiler() if not p.est_vide() else '0'
        return X, Y
    return X


def touchePressee(t, p):
    global enter, op, X, M
    if t in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}:
        if enter or X == '0' or op:
            enter = False
            op = False
            X = ''
        if t == '.' and X == '':
            X = '0.'
        elif t != '.' or (t == '.' and '.'  not in X):
            X += t
    if t in {'+', '*', '-'}:
        op  = True
        X, Y = values_for_op(p, 2, X)
        p.empiler(str(round(eval(Y+t+X),10)))
        X = ''
    if t == '/':
        op = True
        X, Y = values_for_op(p, 2, X)
        if '.' not in X and '.' not in Y and val(Y) % val(X) == 0:
            p.empiler(str(round(eval(Y+'//'+X),10)))
        else:
            p.empiler(str(round(eval(Y+'/'+X),10)))
        X = ''
    if t == 'CLEAR':
        while not p.est_vide():
            X = p.depiler()
        X = '0'
        M = '0'
    if t == 'xy':
        enter = True
        X, Y = values_for_op(p, 2, X)
        p.empiler(X)
        p.empiler(Y)
    if t == '<-':
        X = X[:-1] if len(X) > 1 else '0'
        if X[-1] == '.':
            X = X[:-1]
    if t == 'x^2':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(val(X)**2, 10)))
        X = ''
    if t == 'sqrt':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(m.sqrt(val(X)), 10)))
        X = ''
    if t == 'y^x':
        op = True
        X, Y = values_for_op(p, 2, X)
        p.empiler(str(round(val(Y) ** val(X), 10)))
        X = ''
    if t == '1/x':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(1/val(X), 10)))
        X = ''
    if t == 'LOG':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(m.log10(val(X)), 10)))
        X = ''
    if t == '10^x':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(10**val(X), 10)))
        X = ''
    if t == 'LN':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(m.log(val(X)), 10)))
        X = ''
    if t == 'e^x':
        op = True
        X = values_for_op(p, 1, X)
        p.empiler(str(round(m.e**val(X), 10)))
        X = ''
    if t == '+/-':
        if X == '':
            X = p.depiler() if not p.est_vide() else '0'
            p.empiler(str(- val(X)))
        else:
            X = str(-val(X))
    if t == 'RCL':
        op = True
        p.empiler(M)
    if X == '':
        X = p.depiler()
        p.empiler(X)
    ecran.config(text = X)
    if op:
        X = ''
    if t == 'ENTER':
        enter = True
        p.empiler(X)
        X = ''
    if t == 'STO':
        op = True
        if X == '':
            M = p.depiler() if not p.est_vide() else '0'
            p.empiler(M)
        else:
            M = X
    if t == 'OFF':
        quit()
    print(p)

root = tk.Tk()
root.title("RPN Calculator")
root.geometry('400x677+50+25')

calculatrice = tk.PhotoImage(file="CalcRPN.png")

canevas = tk.Canvas(root, width = 400, height = 677)
canevas.create_image(0,0,anchor = tk.NW, image = calculatrice)
canevas.bind('<Button-1>', clicMouse)
canevas.pack()

ecran = tk.Label(canevas, text = "0", font = 'Verdana 30', bg='#CBC366',
                 justify = 'right')
ecran.pack()
canevas.create_window(355, 119, window = ecran, anchor = tk.E)

pile = p.Pile()

X = '0'
M = '0'
enter = False
op = False

root.mainloop()