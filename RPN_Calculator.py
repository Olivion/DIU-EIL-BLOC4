import tkinter as tk
import math as m
import Pile as p

# Dictionnaire contenant les coordonnées des différentes touches
# de la calculatrice dans le canvas tkInter
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
           'Y+X': {'x1': 245, 'y1': 474, 'x2': 289, 'y2': 524},
           'Y*X': {'x1': 245, 'y1': 540, 'x2': 289, 'y2': 591},
           'Y-X': {'x1': 322, 'y1': 474, 'x2': 376, 'y2': 524},
           'Y/X': {'x1': 322, 'y1': 540, 'x2': 376, 'y2': 591},
           'ENTER': {'x1': 240, 'y1': 409, 'x2': 384, 'y2': 455},
           'CLEAR': {'x1': 24, 'y1': 343, 'x2': 79, 'y2': 394},
           'xy': {'x1': 245, 'y1': 343, 'x2': 299, 'y2': 394},
           '<-': {'x1': 319, 'y1': 343, 'x2': 372, 'y2': 394},
           'X**2': {'x1': 24, 'y1': 281, 'x2': 79, 'y2': 332},
           'm.sqrt(X)': {'x1': 24, 'y1': 212, 'x2': 79, 'y2': 261},
           'Y**X': {'x1': 98, 'y1': 281, 'x2': 152, 'y2': 332},
           '1/X': {'x1': 98, 'y1': 212, 'x2': 152, 'y2': 261},
           'm.log10(X)': {'x1': 171, 'y1': 281, 'x2': 225, 'y2': 332},
           '10**X': {'x1': 171, 'y1': 212, 'x2': 225, 'y2': 261},
           'm.log(X)': {'x1': 245, 'y1': 281, 'x2': 299, 'y2': 332},
           'm.e**X': {'x1': 245, 'y1': 212, 'x2': 299, 'y2': 261},
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

def touchePressee(t, p):
    """En fonction de la touche pressée t, effectue l'action demandée"""
    global enter, op, X, M
    operations1 = ['Y+X', 'Y*X', 'Y-X', 'Y**X']
    operations2 = ['X**2', 'm.sqrt(X)', '1/X', 'm.log10(X)', '10**X',
                   'm.log(X)', 'm.e**X']

    if t in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}:
        if enter or X == '0' or op:
            enter = False
            op = False
            X = ''
        if t == '.' and X == '':
            X = '0.'
        elif t != '.' or (t == '.' and '.'  not in X):
            X += t

    # Opérations à deux opérandes
    elif t in operations1:
        op  = True
        i = operations1.index(t)
        if X == '':
            X = p.depiler() if not p.est_vide() else '0'
        Y = p.depiler() if not p.est_vide() else '0'
        p.empiler(str(round(eval(operations1[i].replace('X',X).replace('Y', Y)),10)))
        X = ''

    # Cas spécial : division entière ou division décimale ?
    elif t == 'Y/X':
        op = True
        if X == '':
            X = p.depiler() if not p.est_vide() else '0'
        Y = p.depiler() if not p.est_vide() else '0'
        if '.' not in X and '.' not in Y and eval(Y+'%'+X) == 0:
            p.empiler(str(round(eval(Y+'//'+X),10)))
        else:
            p.empiler(str(round(eval(Y+'/'+X),10)))
        X = ''

    # Opérations sur une seule valeur

    elif t in operations2:
        op = True
        if X == '':
            X = p.depiler() if not p.est_vide() else '0'
        i = operations2.index(t)
        p.empiler(str(round(eval(operations2[i].replace('X', X)),10)))
        X = ''

    elif t == 'CLEAR':
        while not p.est_vide():
            X = p.depiler()
        X = '0'
        M = '0'

    elif t == 'xy':
        enter = True
        if X == '':
            X = p.depiler() if not p.est_vide() else '0'
        Y = p.depiler() if not p.est_vide() else '0'
        p.empiler(X)
        p.empiler(Y)

    elif t == '<-':
        X = X[:-1] if len(X) > 1 else '0'
        if X[-1] == '.':
            X = X[:-1]

    elif t == '+/-':
        if X == '':
            X = p.depiler() if not p.est_vide() else '0'
            p.empiler(str(-eval(X)))
        else:
            X = str(-eval(X))

    elif t == 'RCL':
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
        if X == '':
            X = p.depiler()
            p.empiler(X)
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

# Programme principal

root = tk.Tk()
root.title("RPN Calculator")
root.geometry('400x677+50+25')


# Affichage de la calculatrice
image = tk.PhotoImage(file="CalcRPN.png")

canevas_calc = tk.Canvas(root, width = 400, height = 677)
canevas_calc.create_image(0,0,anchor = tk.NW, image = image)
canevas_calc.bind('<Button-1>', clicMouse)
canevas_calc.pack()

ecran = tk.Label(canevas_calc, text = "0", font = 'Verdana 30', bg='#CBC366',
                 justify = 'right')
ecran.pack()
canevas_calc.create_window(355, 119, window = ecran, anchor = tk.E)

pile = p.Pile() # Création de la pile de travail

X = '0'   # La valeur en cours d'entrée
M = '0'   # L'unique mémoire de la calculatrice
enter = False # Booléen pour indiquer si la dernière touche a été ENTER
op = False # Booléen pour indiquer si la dernière touche a été une opération

root.mainloop()