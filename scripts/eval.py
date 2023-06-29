
PATH = "./eval.txt"

with open(PATH, "r") as f:
    values = f.read().replace(")", "").replace("(", "").splitlines()
    values = [item.split(",") for item in values]
    values = [(float(a), float(b)) for a, b in values]

avg = sum([item[0] for item in values]) / len(values)

print(avg)
