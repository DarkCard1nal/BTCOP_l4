import sys
import math
import matplotlib.pyplot as plt

# args = [qStart, qCount, qStep, maxStart, maxStop]
args = [0.1, 8, 0.05, 3, 6]


def convert_argument(arg):
	try:
		return int(arg)
	except ValueError:
		try:
			return float(arg)
		except ValueError:
			raise ValueError(
			    f"{arg} - argument could not be converted, default values will be used"
			)


def attacker_success_probability(q, max, limit=1_000_000_000):
	p = 1.0 - q
	z = 0

	while True:
		lambd = z * (q / p)
		total = 1.0

		for k in range(z + 1):
			poisson = math.exp(-lambd)
			for i in range(1, k + 1):
				poisson *= lambd / i
			total -= poisson * (1 - (q / p)**(z - k))

		if abs(total) > max:
			z += 1
			if (z > limit):
				return -1
		else:
			return z


if len(sys.argv) > 1:
	try:
		args = [convert_argument(arg) for arg in sys.argv[1:]]
	except ValueError as e:
		print(e)

print(
    'l4 "Probability of success of a double-cost attack according to the Nakamoto model" by Shkilnyi V. CS31'
)
print(
    f"qStart: {args[0]}, qCount: {args[1]}, qStep: {args[2]}, maxStart: {args[3]}, maxStop: {args[4]}"
)

# an array of attacker shares (the probability that attackers will create the next block faster than honest miners)
qArr = [round(x * args[2] + args[0], 8) for x in range(args[1])]
# the array of attack probabilities is less than
maxArr = [(10**-x) for x in range(args[3], args[4])]
# results number of blocks
zArr = []

print(f"q: {qArr}")
print(f"max: {maxArr}")
print()

print(f"{'q':<10} {'p':<10}", end='')
for max in maxArr:
	print(f" {('{:.5f}'.format(max)).rstrip('0').rstrip('.'):<10}", end='')

print()
for q in qArr:
	z = []
	print(f"{q:<10} {round(1-q, 8):<10}", end='')
	for max in maxArr:
		z.append(attacker_success_probability(q, max))
		print(f" {z[-1]:<10}", end='')

	print()
	zArr.append(z)

plt.figure(figsize=(10, 6))

for i, max in enumerate(maxArr):
	plt.plot(
	    qArr, [z[i] for z in zArr],
	    label=
	    f"Ймовірність атаки менше ніж {('{:.5f}'.format(max)).rstrip('0').rstrip('.')}",
	    marker='o')

plt.xlabel('Частка зловмисників (q)')
plt.ylabel('Кількість блоків підтвердження')
plt.title(
    'Залежність кількості блоків підтвердження від частки зловмисників для різних порогів ймовірності'
)
plt.legend()
plt.grid(True)
plt.show()
