# Importing libraries
from tkinter import *
import time
from Solver import Solver
from Solver import Node
from Solver import Puzzle

global puzzl
global Lph , LAff
t=3 


# Defining interface parameters
fenetre = Tk()

board = [[1,2,3],[4,8,5],[7,0,6]]

photos=[]
for i in range(0,10):
	photos.append(PhotoImage(file="./imgs/"+str(i)+".png"))
Lph = photos[0:9]

can=Canvas( width=180*t,height=180*t,bg='white')
can.pack( side =TOP, padx =20, pady =20)
fenetre['bg']='white'
fenetre.title (' Taquin resolution IA')

puzzl = Puzzle(board,can,Lph)
s = Solver(puzzl,fenetre)


def solv_larg():
	s =Solver(puzzl,fenetre)
	s.solve_Larg()

def solv_long():
	s =Solver(puzzl,fenetre)
	s.solve_Long()

def solve_a_étoile():
        s =Solver(puzzl,fenetre)
        s.solve_a_etoile()

def mel():
	global puzzl
	puzzl = puzzl.shuffle()

def melanger():
	print(puzzl.board)

LAff = list([0,1,2,3,4,5,6,7,8])
LAff=[]
for row in board:
    LAff.extend(row)

menubar = Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="melanger", command=mel)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="melanger", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Recherche en longeur", command=solv_long)
menu2.add_command(label="Recherche en largeur", command=solv_larg)
menu2.add_command(label="A *", command=solve_a_étoile)
menubar.add_cascade(label="Résoudre", menu=menu2)
fenetre.config(menu=menubar)

Button(text='MEL',command=mel).pack(side=LEFT)
Button(text="Recherche en longeur", command=solv_long).pack(side=LEFT)
Button(text="Recherche en largeur", command=solv_larg).pack(side=LEFT)
Button(text="A *", command=solve_a_étoile).pack(side=LEFT)




for k in range(len(Lph)) :
    eff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW, image=Lph[0])
    aff = can.create_image((30+ 150*(k % t)), 30+(150*( k // t)), anchor=NW ,image = Lph[LAff[k]])

can.pack()

fenetre.mainloop()
