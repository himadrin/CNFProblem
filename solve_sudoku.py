#solve_sudoku.py - Himadri Narasimhamurthy
#2/14/19

from display import display_sudoku_solution
import random, sys
import time
from SAT import SAT
from Sudoku import *

def solve_sudoku(puzzle):
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(41)

    puzzle_name = str(puzzle)
    sol_filename = puzzle_name[:-4] + ".sol"

    sat = SAT(puzzle)

    #https://stackoverflow.com/questions/3620943/measuring-elapsed-time-with-the-time-module
    start = time.time()
    result = sat.WalkSAT()
    total = time.time() - start

    if puzzle_name[-4:] == ".sud":
        print("original sudoku puzzle: ")
        sud = Sudoku()
        sud.load(puzzle)
        print(sud)

    if result:
        sat.sol_file(sol_filename)
        print("solution found in " + str(sat.runs) + " iterations of SAT")
        print("the code took " + str(total) + " seconds to run.")
        display_sudoku_solution(sol_filename)

    else:
        print("no solution found by SAT in " + str(sat.limit) + " iterations of SAT")

def solve_sudoku_extra(puzzle):
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(41)

    puzzle_name = str(puzzle)
    sol_filename = puzzle_name[:-4] + ".sol"

    sat = SAT(puzzle)

    start = time.time()
    result = sat.WalkSAT()
    total = time.time() - start

    if puzzle_name[-4:] == ".sud":
        print("original sudoku puzzle: ")
        sud = Sudoku()
        sud.load(puzzle)
        print(sud)

    if result:
        sat.sol_file(sol_filename)
        print("solution found in " + str(sat.runs) + " iterations of SAT")
        print("the code took " + str(total) + " seconds to run.")
        display_sudoku_solution(sol_filename)

    else:
        print("no solution found by SAT in " + str(sat.limit) + " iterations of SAT")


#extraSudoku = Sudoku()
#extraSudoku.load('puzzle1.sud')
#extraSudoku.generate_extra_cnf('puzzle1ex.cnf')

solve_sudoku('rules.cnf')

#solve_sudoku_extra('puzzle1ex.cnf')


