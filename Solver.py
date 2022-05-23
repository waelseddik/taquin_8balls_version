import random
import itertools
import collections
import time
from tkinter import *


class Node:
    
     
    #Une classe représentant un etat (noeud de la recherche binaire) de Puzzle
     #- 'puzzle' est une instance de Puzzle
     #- 'parent' est le noeud précédent généré par le solveur
     #- 'action' est l'action pour produire l'etat de puzzle
    

    def __init__(self, puzzle, parent=None, action=None, cout=None, heuristique=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.heuristique = heuristique
        self.cout = cout

    def calcul_h(self):
        c = 0
        for i, x in enumerate("123456780"):
            if x != self.state[i]:
                c += 1
        return (c)

    @property
    def state(self):
        return str(self)

    @property
    def path(self):
        """
        Retourne un chemin d'un noeud depuis la racine 'parent'
        """
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self): # Vérifier si le 'puzzle' est résolu
        return self.puzzle.solved

    @property
    def actions(self): #Les actions pour accéder à l'état actuel 
        return self.puzzle.actions

    def __str__(self):
        return str(self.puzzle)


class Solver:

    def __init__(self, start, fenetre):
        self.start = start
        self.fenetre = fenetre

    def solve_Larg(self):
        t_init = time.time()
        print("Recherche de solution en largeur")
        print(self.start.board)
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.solved:
                z = list(node.path)
                print("solution trouvée en", len(z), " coups")
                t_final = time.time()
                print("Durée de la recherche: " + str(t_final - t_init) + " second(s)")
                self.aff5(z)
                break
            for move, action in node.actions:
                child = Node(move(), node, action)
                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

    def solve_Long(self):
        t_init = time.time()
        print("Recherche de solution en longeur")
        queue = collections.deque([Node(self.start)])
        seen  = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.solved:
                z= list(node.path)
                self.aff5(z)
                print("solution trouvée en", len(z) , " coups")
                t_final = time.time()
                print("Durée de la recherche: " + str(t_final - t_init) + " second(s)")
                break
            for move, action in node.actions:
                child = Node(move(), node, action)
                if child.state not in seen:
                    queue.append(child)
                    seen.add(child.state)


    def solve_a_etoile(self):
        t_init = time.time()
        print("Recherche de solution en A*")
        print(self.start.board)
        départ = Node(self.start)
        départ.cout = 0
        départ.historique = départ.calcul_h()
        openList = [départ]
        closedList = set()
        closedList.add(openList[0].state)
        while len(openList) > 0:
            node = openList.pop()
            if node.solved:
                z = list(node.path)
                print("solution trouvée en ", len(z), " coups")
                t_final = time.time()
                print("Durée de la recherche: " + str(t_final - t_init) + " second(s)")
                self.aff5(z)
                break
            for move, action in node.actions:
                child = Node(move(), node, action, node.cout + 1)
                index = [i for i, x in enumerate(openList) if x.state == child.state]
                if not ((child.state in closedList) or (index != [] and openList[index[0]].cout > child.cout)):
                    child.heuristique = child.calcul_h() + child.cout
                    openList.append(child)
                    sorted(openList, key=lambda node: node.heuristique, reverse=True)
            closedList.add(node.state)

    def aff5(self, p, i=1):
        node = p[0]
        p = p[1:]
        x = node.puzzle.convL()
        print("coup", i, " : ", x)
        node.puzzle.afficher2(x)
        if p:
            self.fenetre.after(1500, self.aff5, p, i + 1)
        else:
            print("fin")


class Puzzle:
    
    """
    Une classe représentant un puzzle
    - 'table' devrait être une liste carrée de listes avec des entrées entières 0 ... largeur ^ 2 - 1
        par exemple. [[1,2,3], [4,0,6], [7,5,8]]
    """

    def __init__(self, board, root, Lph):
        self.width = len(board[0])
        self.board = board
        self.can = root
        self.Lph = Lph

    @property
    def solved(self):
        """
        Le puzzle est résolu si les nombres sont en ordre croissant de gauche à droite
        et que '0' est en dernière position sur le plateau
        """

        tab = []
        sol = True
        for i in range(self.width):
            tab.extend(self.board[i]);

        for j in range(len(tab) - 2):
            if (tab[j] != (tab[j + 1] - 1)):
                sol = False;
        if tab[-1] != 0:
            sol = False;
        return sol

    @property
    def actions(self): #            Retourner la liste de (move, action).
        def create_move(at, to):
            return lambda: self.move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width),
                                      range(self.width)):
            direcs = {'R': (i, j - 1),
                      'L': (i, j + 1),
                      'D': (i - 1, j),
                      'U': (i + 1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and \
                        self.board[r][c] == 0:
                    move = create_move((i, j), (r, c)), action
                    moves.append(move)
        return moves

    def shuffle(self): #retourne une configuration d'un puzzle mélangé(1000 coups aléatoires)
        puzzle = self   #puzzle prend self(configuration initiale)
        for k in range(1000):
            puzzle = random.choice(puzzle.actions)[0]()
        x = puzzle.convL()
        print(x)
        self.afficher2(x)
        self = puzzle
        puzzle.board = self.board
        return puzzle

    def copy(self): #Retourner un nouveau objet puzzle avec le même table que 'self'
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board, self.can, self.Lph)

    def move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def afficher2(self, liste1):
        "permet d'afficher les mouvements des images sur le canvas lors de la resolution"
        for k in range(len(liste1)):
            eff = self.can.create_image((30 + 150 * (k % self.width)), 30 + (150 * (k // self.width)), anchor=NW,
                                        image=self.Lph[0])
            aff = self.can.create_image((30 + 150 * (k % self.width)), 30 + (150 * (k // self.width)), anchor=NW,
                                        image=self.Lph[liste1[k]])

    def convL(self): #convertit l'objet puzzle en une liste composée des valeurs de table 
        L = []
        for row in self.board:
            L.extend(row)
        return L

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row

