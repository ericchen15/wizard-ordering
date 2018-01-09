from string import ascii_lowercase
from random import shuffle
from numpy.random import choice

names = []
for c in ascii_lowercase:
	names.append(c)
	names.append(c.upper())

size = 50
num_constraints = 366

names = names[:size]
shuffle(names)

def random_constraint(names):
	sample = choice(len(names), 3, replace=False)
	if sample[0] < sample[2] < sample[1] or sample[0] > sample[2] > sample[1]:
		temp = sample[0]
		sample[0] = sample[2]
		sample[2] = temp
	return [names[sample[0]], names[sample[1]], names[sample[2]]]

with open('input50.in', 'w') as f:
	f.write(str(size) + '\n')
	f.write(names[0])
	for name in names[1:]:
		f.write(' ' + name)
	f.write('\n')
	f.write(str(num_constraints))
	for _ in range(num_constraints):
		constraint = random_constraint(names)
		f.write('\n' + constraint[0] + ' ' + constraint[1] + ' ' + constraint[2])