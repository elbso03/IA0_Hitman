from itertools import combinations
from pprint import pprint
from typing import *

GridClear = List[List[str]]
Grid = List[List[int]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

hauteur_mat = 6
largeur_mat = 7
taille_mat = hauteur_mat * largeur_mat
nb_variables = 8 # pour le moment


def cell_to_ClearCell(val: int) -> str:
    """Transforme une cellule en variable sous format DIMACS (entier)"""
    if(val == 0):
        # Cellule vide
        return "_"
    elif (val == 1):
        # Hitman
        return "H"
    elif (val == 2):
        # Corde
        return "CO"
    elif(val== 3):
        # Déguisement
        return "D"
    elif (val == 4):
        # Cible
        return "CI"
    elif (val == 5):
        # Garde
        return "G"
    elif (val == 6):
        # Invité
        return "I"
    elif (val == 7):
        # Mur
        return "M"


def cell_to_variable(m: int, n: int, val: int) -> PropositionnalVariable:
    """Transforme une cellule en variable sous format DIMACS (entier)"""
    # définie de 0 à m*n -1 (m*n taille de la matrice)
    return taille_mat*val + m*largeur_mat + n + 1

def variable_to_cell(i: int) -> Tuple[int, int, int]:
    """Transforme une variable en cellule"""
    return (((i - 1) % taille_mat) // largeur_mat, (i - 1) % largeur_mat,(i - 1) // taille_mat)


def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    clause = variables[:]
    return clause

def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    #kb = [at_least_one(variables)]
    kb = []
    for v1,v2 in list(combinations(variables, 2)) :
        #kb.append([v1, v2])
         kb.append([-v1,-v2])
    return kb

def simple_implication(variables: List[PropositionnalVariable]) -> ClauseBase:
    kb = []
    for v2 in list(variables[1:]) :
        # kb.append([variables[0], v2]) pour verif
        kb.append([-variables[0],-v2])
    return kb

def create_cell_constraints() -> ClauseBase:
    kb = []
    for row in range(hauteur_mat):
        for col in range(largeur_mat):
            list = []
            for val in range(2,8):
                # on a exclu Hitman
                list.append(cell_to_variable(row, col, val))
            kb += unique(list)
            # on inclut Hitman dans les contraintes des gardes
            kb +=unique([cell_to_variable(row, col, 1),cell_to_variable(row, col, 5)])
            # on inclut Hitman dans les contraintes des murs
            kb += unique([cell_to_variable(row, col, 1), cell_to_variable(row, col, 7)])

    return kb

def create_objects_constraints()  -> ClauseBase :
    kb = []
    for obj in (1,2,3,4) :
        list = []
        for row in range(hauteur_mat):
            for col in range(largeur_mat):
                list.append(cell_to_variable(row, col, obj))
        kb.append(at_least_one(list))
        kb += unique(list)
    return kb




exampleClear: GridClear = [
    ["_" ,"_" ,"_" ,"D" ,"G" ,"M" ,"M"],
    ["_" ,"M" ,"_" ,"_" ,"_" ,"_" ,"_"],
    ["CI","M" ,"_" ,"_" ,"_" ,"G" ,"_"],
    ["M" ,"M" ,"_" ,"I" ,"_" ,"I" ,"I"],
    ["_" ,"_" ,"_" ,"_" ,"_" ,"_" ,"_"],
    ["_" ,"H" ,"M" ,"M" ,"_" ,"CO" ,"_"]
]

example: Grid = [
    [0, 0, 0, 3, 5, 7, 7],
    [0, 7, 0, 0, 0, 0, 0],
    [4, 7, 0, 0, 0, 5, 0],
    [7, 7, 0, 6, 0, 6, 6],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 7, 7, 0, 2, 0],
]

def verif():

    output2 = [[0] * largeur_mat for _ in range(hauteur_mat)]
    for i in range(hauteur_mat):
        for j in range(largeur_mat):
            output2[i][j] = cell_to_variable(i, j, example[i][j])
    pprint(output2)

    # Test transformation variable -> cellule
    output3 = [[0] * largeur_mat for _ in range(hauteur_mat)]
    for i in range(hauteur_mat):
        for j in range(largeur_mat):
            tmp = variable_to_cell(output2[i][j])
            output3[tmp[0]][tmp[1]] = tmp[2]
    pprint(output3)

    # Test affichage en clair
    output4 = [[0] * largeur_mat for _ in range(hauteur_mat)]
    for i in range(hauteur_mat):
        for j in range(largeur_mat):
            output4[i][j] = cell_to_ClearCell(output3[i][j])
    pprint(output4)
"""
    # verification contraintes cellule
    tab = create_cell_constraints()
    tab2 = [[0] * len(tab[row]) for row in range(len(tab))]
    for row in range(len(tab)):
        for col in range(len(tab[row])):
            tmp = variable_to_cell(tab[row][col])
            tab2[row][col] = (f"-{cell_to_ClearCell(tmp[2])}", tmp[0], tmp[1])
    pprint(tab2)

    # verification contraintes des objets/personnages
    tab = create_objects_constraints()
    print(tab)
    tab2 = [[0] * len(tab[row]) for row in range(len(tab))]
    for row in range(len(tab)):
        for col in range(len(tab[row])):
            tmp = variable_to_cell(tab[row][col])
            tab2[row][col] = (f"{cell_to_ClearCell(tmp[2])}", tmp[0], tmp[1])
    pprint(tab2)

"""
if __name__=="__main__":
    #verif()
    pprint(create_objects_constraints()+create_cell_constraints())


