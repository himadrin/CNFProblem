#SAT.py - Himadri Narasimhamurthy
#2/14/19
#generic cnf problem solver implemented in gsat and walksat

import random


class SAT:

    #the init method also populates many of the self variables from the cnf file
    def __init__(self, file_name, limit = 100000):

        # generic init for all cnf problems
        self.variables = set()      #no repeats!
        self.clauses = []
        self.solution = {}

        #read cnf lines from .cnf file
        file = file_name[:-4] + ".cnf"
        f = open(file, "r")
        cnfs = f.readlines()   #all lines in file as a list

        #populate variables and clauses needed for SAT
        for c in cnfs:
            vars = []
            for v in c.split():
                vars.append(v)

                #update variable list
                if v not in self.variables:
                    stripped_v = v.strip().strip("-")
                    self.variables.add(stripped_v)

            #populate clause list - each line with or and each clause with and
            self.clauses.append(vars)

        f.close()

        #for use in SATs
        self.satisfied = []
        self.unsatisfied = []

        self.runs = 0
        self.limit = limit
        self.threshold = 0.7


    # gsat goes until no more unsatisfied and flips the value of either highest val var or random var
    def GSAT(self):

        # generates a random boolean for each variable - will change later
        for v in self.variables:
            # got code to generate rand boolean from here (https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python)
            self.solution[v] = bool(random.getrandbits(1))

        # update lists for each iteration and check if all constraints satisfied
        while not self.end_sat():

            self.runs = self.runs + 1

            # run until limit
            if self.runs < self.limit:
                # print(len(self.unsatisfied)) #to whether the algorithm is working

                # if random frac is above threshold
                if random.uniform(0, 1) > self.threshold:

                    # choose a random variable
                    r = random.randint(0, len(self.variables) - 1)
                    var = str(list(self.variables)[r])

                else:
                    # if below threshold, then get the var with highest val
                    var = self.highest_var(self.variables)

                # flip the variable's boolean
                self.solution[var] = not self.solution[var]
            else:
                return False

        return True


    # similar to gsat but instead of choosing random vars - we choose a random var from inside a random unsatisfied clause
    # then we flip its value based on either random or highest var val
    def WalkSAT(self):

        # generates a random boolean for each variable - will change later
        for v in self.variables:
            # got code to generate rand boolean from here (https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python)
            self.solution[v] = bool(random.getrandbits(1))

        #print(self.solution)

        while not self.end_sat():
            self.runs = self.runs + 1

            # run until limit
            if self.runs < self.limit:
                print(len(self.unsatisfied)) #see whether algorithm is working

                # pick random unsatisfied clause
                r = random.randint(0, len(self.unsatisfied) - 1)
                clause = self.unsatisfied[r]
                #print(clause)

                # from gsat - now we choose a variable from that clause based on threshold
                if random.uniform(0, 1) > self.threshold:
                    #print("1")
                    r = random.randint(0, len(clause) - 1)
                    var = clause[r].strip().strip('-')

                else:
                    #print("2")
                    # if below threshold, then get the var with highest val
                    var = self.highest_var(clause)

                # flip the variable's boolean
                self.solution[var] = not self.solution[var]

            else:
                return False

        return True

    #def DPLL


    # loop through clauses and figures out whether all are satisfied
    def end_sat(self):

        #clear lists to remake them for each iteration
        self.unsatisfied[:] = []
        self.satisfied[:] = []

        end = True

        #loop through clauses - setting them to false before checking
        for c in self.clauses:
            sat = False

            end = self.update_clause_list(c, sat, end)

        return end


    #helper function - helps assign clauses to lists and returns end var
    def update_clause_list(self, clause, sat, end):
        #loop through constraint in clause
        for c in clause:

            #if clause is positive, or its boolean with sat, else or the negative of its boolean
            if c[0] != "-":
                sat = sat or self.solution[c.strip().strip("-")]
            else:
                sat = sat or not self.solution[c.strip().strip("-")]

        #we set end as true when we have both satisfied and end as true
        end = sat and end

        #now update sat and unsat lists based on the sat boolean
        if sat:
            self.satisfied.append(clause)
        else:
            self.unsatisfied.append(clause)

        return end


    # go through variable list
    # return variable with the highest number of clauses satisfied after flipping the boolean!
    def highest_var(self, vars):
        h_var = None
        max_score = 0

        for v in vars:
            v = v.strip('-')

            #flip the boolean to make sat and unsat for when the boolean would be flipped
            self.solution[v] = not self.solution[v]

            #updates the clause lists - satisfied and unsatisfied
            self.end_sat()

            #flip back so that we can still flip at the end of sat
            self.solution[v] = not self.solution[v]
            curr_score = len(self.satisfied)        #have greatest score as v which allows for most satisfied

            #curr vs max conditions
            if curr_score>=max_score:
                h_var = v
                max_score = curr_score
            else:
                h_var = h_var
                max_score = max_score

        return h_var


    #writes our result into a solution file in constriant form
    def sol_file(self, f):
        f = open(f, "w")
        for key in self.solution.keys():

            #is the variable a part of the solution?
            if self.solution[key]:
                sign = ""
            else:
                sign = "-"

            f.write(str(sign + key + "\n"))