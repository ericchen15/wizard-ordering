"""
techniques
swap random
swap best
simulated annealing
only swap adjacent
"""

import random
import sys

with open("phase2_inputs/inputs20/input20_0.in", "r") as f:
	lines = [line.strip() for line in f]
	num_wizards = int(lines[0])
	num_constraints = int(lines[1])
	wizards = set()
	constraints = []
	for line in lines[2:]:
		constraint = line.split()
		constraints.append(constraint)
		wizards.update(constraint)

wizards = list(wizards)

def distance_heuristic(constraint, wizards):
	x0 = wizards.index(constraint[0])
	x1 = wizards.index(constraint[1])
	x2 = wizards.index(constraint[2])
	if x0 < x2 < x1 or x1 < x2 < x0:
		return min(abs(x2 - x0), abs(x1 - x2))
	else:
		return 0

def satisfied(constraint, wizards):
	x0 = wizards.index(constraint[0])
	x1 = wizards.index(constraint[1])
	x2 = wizards.index(constraint[2])
	if x0 < x2 < x1 or x1 < x2 < x0:
		return 0
	else:
		return 1

def swap(A, index0, index1):
	A[index0], A[index1] = A[index1], A[index0]

def list_distance(constraints, wizards):
	return sum([distance_heuristic(constraint, wizards) for constraint in constraints])

def bad_constraints(constraints, wizards):
	return [constraint for constraint in constraints if not satisfied(constraint, wizards)]

def examine_moves(constraints, wizards):
	value = {}
	for i in range(len(wizards)):
		for j in range(len(wizards)):
			if i != j:
				value[(i, j)] = 0
	indices = get_indices(wizards)
	for constraint in constraints:
		x0 = indices[constraint[0]]
		x1 = indices[constraint[1]]
		x2 = indices[constraint[2]]
		if x0 < x2 and x1 < x2:
			for j in range(x2, len(wizards)):
				value[(x0, j)] -= 1
				value[(x1, j)] -= 1
			for j in range(min(x0, x1) + 1, max(x0, x1) + 1):
				value[(x2, j)] -= 1
		elif x0 > x2 and x1 > x2:
			for j in range(x2 + 1):
				value[(x0, j)] -= 1
				value[(x1, j)] -= 1
			for j in range(min(x0, x1), max(x0, x1)):
				value[(x2, j)] -= 1
		else:
			for j in range(x2, len(wizards)):
				value[(min(x0, x1), j)] += 1
			for j in range(x2 + 1):
				value[(max(x0, x1), j)] += 1
			for j in range(min(x0, x1) + 1):
				value[(x2, j)] += 1
			for j in range(max(x0, x1), len(wizards)):
				value[(x2, j)] += 1
	best_key = max(value, key=lambda x: value[x] + random.random())
	return best_key, value[best_key]

loops = 0

"""
using distance heuristic, seems pretty bad
while list_distance(constraints, wizards) > 0:
	print(list_distance(constraints, wizards))
	sys.stdout.flush()
	swap_lists = []
	for i in range(num_wizards - 1):
		swap_list = list(wizards)
		swap(swap_list, i, i+1)
		swap_lists.append(swap_list)
	list_distances = [list_distance(constraints, swap_list) for swap_list in swap_lists]
	min_distance = min(list_distances)
	if min_distance < list_distance(constraints, wizards):
		wizards = swap_lists[list_distances.index(min_distance)]
	else:
		random_indices = random.sample(range(num_wizards), 2)
		swap(wizards, random_indices[0], random_indices[1])
	loops += 1
"""

"""
using num unsatisfied heuristic, seems pretty bad
unsatisfied = bad_constraints(constraints, wizards)
while len(unsatisfied) > 0:
	print(len(unsatisfied))
	sys.stdout.flush()
	swap_lists = []
	for bad_constraint in unsatisfied:
		swap_list = list(wizards)
		swap(swap_list, swap_list.index(bad_constraint[0]), swap_list.index(bad_constraint[2]))
		swap_lists.append(swap_list)
		swap_list = list(wizards)
		swap(swap_list, swap_list.index(bad_constraint[1]), swap_list.index(bad_constraint[2]))
		swap_lists.append(swap_list)
	for i in range(num_wizards - 1):
		swap_list = list(wizards)
		swap(swap_list, i, i+1)
		swap_lists.append(swap_list)
	num_unsatisfied = [len(bad_constraints(constraints, swap_list)) for swap_list in swap_lists]
	min_unsatisfied = min(num_unsatisfied)
	if min_unsatisfied < len(unsatisfied):
		wizards = swap_lists[num_unsatisfied.index(min_unsatisfied)]
	else:
		random_indices = random.sample(range(num_wizards), 2)
		swap(wizards, random_indices[0], random_indices[1])
	unsatisfied = bad_constraints(constraints, wizards)
	loops += 1
"""

def count_unsatisfied(unsatisfied, wizard):
	return sum([1 for constraint in unsatisfied if wizard in constraint])

def worst_wizard(unsatisfied, wizards):
	num_unsatisfied = [count_unsatisfied(unsatisfied, wizard) for wizard in wizards]
	max_unsatisfied = max(num_unsatisfied)
	return num_unsatisfied.index(max_unsatisfied)

unsatisfied = bad_constraints(constraints, wizards)
while len(unsatisfied) > 0:
	worst = worst_wizard(unsatisfied, wizards)
	print(len(unsatisfied), worst)
	swap_lists = []
	for i in range(worst):
		swap_list = wizards[:i] + [wizards[worst]] + wizards[i:worst] + wizards[worst + 1:]
		swap_lists.append(swap_list)
	for i in range(worst + 1, num_wizards):
		swap_list = wizards[:worst] + wizards[worst + 1:i + 1] + [wizards[worst]] + wizards[i + 1:]
		swap_lists.append(swap_list)
	num_unsatisfied = [len(bad_constraints(constraints, swap_list)) for swap_list in swap_lists]
	min_unsatisfied = min(num_unsatisfied)
	if min_unsatisfied < len(unsatisfied):
		wizards = swap_lists[num_unsatisfied.index(min_unsatisfied)]
	else:
		wizards = random.choice(swap_lists)
	unsatisfied = bad_constraints(constraints, wizards)
	loops += 1
	sys.stdout.flush()

print(loops)
print(wizards)