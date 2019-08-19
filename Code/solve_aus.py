import random
from SAT import SAT

def solve_aus(puzzle):
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(41)

    puzzle_name = str(puzzle)
    sol_filename = puzzle_name[:-4] + ".sol"

    sat = SAT(puzzle)

    result = sat.WalkSAT()

    if result:
        sat.sol_file(sol_filename)
        print("solution found in " + str(sat.runs) + " iterations of SAT")
    else:
        print("no solution found by SAT in " + str(sat.limit) + " iterations of SAT")


solve_aus("aus.cnf")

