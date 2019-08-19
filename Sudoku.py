#Majority code provided - modified by Himadri Narasimhamurthy
#2/14/19
#modifications are commented - for EC

class Sudoku:
    def __init__(self):
        self.numbers = [[0 for i in range(9)] for j in range(9)]

    def load(self, filename):
        f = open(filename, "r")
        r = 1
        for line in f:
            c = 1
            # each line contains a row
            for s in line.split():
                self.set(r, c, int(s))
                c += 1

            r += 1

    def get(self, r, c):
        return self.numbers[r - 1][c - 1]

    def set(self, r, c, value):
        self.numbers[r - 1][c - 1] = value

    def read_solution(self, filename):
        f = open(filename, "r")
        for line in f:
            # ignore unset variables
            literal = int(line)
            if literal > 0:
                r = int(line[0])
                c = int(line[1])
                v = int(line[2])
                self.set(r, c, v)

        f.close()

    def __str__(self):
        s = ""
        for r in range(1, 10):
            if r == 4 or r == 7:
                s += "---------------------\n"

            for c in range(1, 10):

                if c == 4 or c == 7:
                    s += "| "
                s = s + str(self.get(r, c))
                s += " "

            s += "\n"

        return s

    def sudoku_literal(self, r, c, v, neg=False):
        return ("-" if neg else "") + str(r) + str(c) + str(v)

    def cell_clause(self, r, c):

        s = ""

        # at least one value:
        atleastone_str = ""
        for value in range(1, 10):
            atleastone_str += self.sudoku_literal(r, c, value) + " "
        atleastone_str += " \n"

        s = atleastone_str

        for vi in range(1, 10):
            for vj in range(vi + 1, 10):
                s += self.sudoku_literal(r, c, vi, neg=True) + " "
                s += self.sudoku_literal(r, c, vj, neg=True) + " "
                s += "\n"

        return s

    #added function to add Spence's row constraints - based off cell_clause
    def row_clause2(self, r):
        #same as before
        s = ""
        for value in range(1, 10):
            for col in range(1, 10):
                s += self.sudoku_literal(r, col, value) + " "
            s += "\n"

            #added to go through each col in row and add each neg constraint
            for ci in range(1, 10):
                for cj in range(ci + 1, 10):
                    s += self.sudoku_literal(r, ci, value, neg=True) + " "
                    s += self.sudoku_literal(r, cj, value, neg=True) + " "
                    s += "\n"

        return s

    # added function to add Spence's col constraints - based off cell_clause
    def col_clause2(self, c):
        #same as before
        s = ""
        for value in range(1, 10):
            for row in range(1, 10):
                s += self.sudoku_literal(row, c, value) + " "
            s += "\n"

            # added to go through each row in col and add each neg constraint
            for ri in range(1, 10):
                for rj in range(ri + 1, 10):
                    s += self.sudoku_literal(ri, c, value, neg=True) + " "
                    s += self.sudoku_literal(rj, c, value, neg=True) + " "
                    s += "\n"

        return s

    def row_clause(self, r):
        s = ""
        for value in range(1, 10):
            for c in range(1, 10):
                s += self.sudoku_literal(r, c, value) + " "
            s += "\n"

        return s

    def col_clause(self, c):
        s = ""
        for value in range(1, 10):
            for r in range(1, 10):
                s += self.sudoku_literal(r, c, value) + " "
            s += "\n"

        return s

    def write_block_clauses(self, filehandle):

        s = ""

        for sr in range(1, 10, 3):
            for sc in range(1, 10, 3):
                for value in range(1, 10):
                    for r_offset in range(3):
                        for c_offset in range(3):
                            r = sr + r_offset
                            c = sc + c_offset
                            s += self.sudoku_literal(r, c, value) + " "

                    s += "\n"

        filehandle.write(s)

    def write_fixed_clauses(self, filehandle):
        s = ""
        for r in range(1, 10):
            for c in range(1, 10):
                value = self.get(r, c)
                if value !=  0:
                    s += self.sudoku_literal(r, c, value) + "\n"

        filehandle.write(s)


    def write_col_clauses(self, filehandle):
        for c in range(1, 10):
            clause = self.col_clause(c)
            filehandle.write(clause)

    def write_col_clauses2(self, filehandle):
        for c in range(1, 10):
            clause = self.col_clause2(c)
            filehandle.write(clause)

    def write_row_clauses(self, filehandle):
        for r in range(1, 10):
            clause = self.row_clause(r)
            filehandle.write(clause)

    def write_row_clauses2(self, filehandle):
        for r in range(1, 10):
            clause = self.row_clause2(r)
            filehandle.write(clause)

    def write_cell_clauses(self, filehandle):
        for r in range(1, 10):
            for c in range(1, 10):
                clause = self.cell_clause(r, c)
                filehandle.write(clause)

    def generate_cnf(self, filename):
        f = open(filename, "w")
        self.write_cell_clauses(f)
        self.write_row_clauses(f)
        self.write_col_clauses(f)
        self.write_block_clauses(f)
        self.write_fixed_clauses(f)
        f.close()

    #function to call to generate Spence's cnf file
    def generate_extra_cnf(self, filename):
        f = open(filename, "w")
        self.write_cell_clauses(f)
        self.write_row_clauses2(f)
        self.write_col_clauses2(f)
        self.write_block_clauses(f)
        self.write_fixed_clauses(f)
        f.close()


if __name__ == "__main__":
    test_sudoku = Sudoku()

    test_sudoku.load("puzzle_bonus.sud")
    #print(test_sudoku)
    # print(sudoku_literal(2, 3, 9, neg=True))

    # print(cell_clause(1, 1))

    test_sudoku.generate_cnf("puzzle_bonus.cnf")

    #test_sudoku.read_solution("rules.sol")
    print(test_sudoku)
