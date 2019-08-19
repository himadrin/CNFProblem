#solve_australia.py - Himadri Narasimhamurthy
#2/14/19
#EC - australia map coloring as a cnf problem
#solved by gsat

import random
from SAT import SAT


def solve_aus(puzzle):
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(41)

    puzzle_name = str(puzzle)
    sol_filename = puzzle_name[:-4] + ".sol"

    sat = SAT(puzzle, 300)

    result = sat.GSAT()

    if result:
        sat.sol_file(sol_filename)
        print("solution found in " + str(sat.runs) + " iterations of SAT")
        display_aus_sol(sol_filename)
    else:
        print("no solution found by SAT in " + str(sat.limit) + " iterations of SAT")


#reads in .sol file and outputs to console
def display_aus_sol(sol_filename):
    f = open(sol_filename, "r")
    for line in f:

        l = line.strip()[:-1]
        col = line[len(l):len(l)+1]

        if col == "r":
            s = "red"
        elif col == "g":
            s = "green"
        else:
            s = "blue"

        if line[0] != "-":
            print (str(l) + " maps to " + s + "\n")

    f.close()

#this is an impossible puzzle
print('Impossible Case\n')

solve_aus('aus.cnf')

print("\n---------------------------------------\n")

solve_aus('australia.cnf')

