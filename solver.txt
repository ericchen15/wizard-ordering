import argparse
import random
import sys
import math

"""
======================================================================
  Complete the following function.
======================================================================
"""

# Input: list of wizard names
# Output: dict mapping wizard names to indices
def get_indices(wizards):
	indices = {}
	for index, wizard in enumerate(wizards):
		indices[wizard] = index
	return indices

# Input: list of constraints, list of wizard names
# Output: list of unsatisfied constraints
def bad_constraints(constraints, wizards):
	indices = get_indices(wizards)
	unsatisfied = []
	for constraint in constraints:
		x0, x1, x2 = indices[constraint[0]], indices[constraint[1]], indices[constraint[2]]
		if x0 < x2 < x1 or x1 < x2 < x0:
			unsatisfied.append(constraints)
	return unsatisfied

# Input: current energy, eneregy of neighbor, temperature
# Output: probability of moving to neighbor
# used in simulated annealing, taken from en.wikipedia.org/wiki/Simulated_annealing
def P(E, E_neighbor, T):
	if E_neighbor < E:
		return 1
	else:
		return math.exp((E - E_neighbor) / T)

# Input: list of wizard names, tuple of (wizard to move, place to move it)
# Output: list of wizard names after movement
# the neighbors of the current position are defined as the positions reachable in 1 movement
# a movement only affects the constraints that include the moved wizard, the order of the other wizards is unchanged
def do_move(wizards, move):
	wizard, location = move
	if wizard > location:
		return wizards[:location] + [wizards[wizard]] + wizards[location:wizard] + wizards[wizard + 1:]
	else:
		return wizards[:wizard] + wizards[wizard + 1:location + 1] + [wizards[wizard]] + wizards[location + 1:]

def solve(num_wizards, num_constraints, wizards, constraints):
	"""
	Write your algorithm here.
	Input:
		num_wizards: Number of wizards
		num_constraints: Number of constraints
		wizards: An array of wizard names, in no particular order
		constraints: A 2D-array of constraints, where constraints[0] may take the form ['A', 'B', 'C']

	Output:
		An array of wizard names in the ordering your algorithm returns
	"""

	# ignore constraints with the same name more than once
	constraints = [constraint for constraint in constraints if len(constraint) == len(set(constraint))]

	# create a dict mapping a wizard w to the constraints that w appears in
	relevant_constraints = {}
	for wizard in wizards:
		relevant_constraints[wizard] = [constraint for constraint in constraints if wizard in constraint]

	# create a list of all possible moves
	moves = []
	for i in range(num_wizards):
		for j in range(num_wizards):
			if i != j:
				moves.append((i, j))

	random.shuffle(wizards)

	# simulated annealing, taken from katrinaeg.com/simulated-annealing.html
	T = 1 # initial temperature
	T_min = 0.0001 # minimum temperature
	while T > T_min:
		for _ in range(5000): # number of iterations at each temperature
			random_move = random.choice(moves)
			neighbor = do_move(wizards, random_move)
			# anneal on the number of bad constraints
			relevant = relevant_constraints[wizards[random_move[0]]]
			E = len(bad_constraints(relevant, wizards))
			E_neighbor = len(bad_constraints(relevant, neighbor))
			if P(E, E_neighbor, T) >= random.random():
				wizards = neighbor
		T *= .99 # temperature decay rate
		
		# print the current temperature and the number of bad constraints, used to gauge progress
		num_bad = len(bad_constraints(constraints, wizards))
		print(T, num_bad)
		# return if all constraints are satisfied
		if num_bad == 0:
			return wizards
		sys.stdout.flush()

	return wizards

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

def read_input(filename):
	with open(filename) as f:
		num_wizards = int(f.readline())
		num_constraints = int(f.readline())
		constraints = []
		wizards = set()
		for _ in range(num_constraints):
			c = f.readline().split()
			constraints.append(c)
			for w in c:
				wizards.add(w)
				
	wizards = list(wizards)
	return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
	with open(filename, "w") as f:
		for wizard in solution:
			f.write("{0} ".format(wizard))

if __name__=="__main__":
	parser = argparse.ArgumentParser(description = "Constraint Solver.")
	parser.add_argument("input_file", type=str, help = "___.in")
	parser.add_argument("output_file", type=str, help = "___.out")
	args = parser.parse_args()

	num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
	solution = solve(num_wizards, num_constraints, wizards, constraints)
	write_output(args.output_file, solution)