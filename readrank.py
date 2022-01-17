with open('rank.txt', 'r') as f:
    lines = f.readlines()

ranklist = []

for line in lines:
    count = 0
    name = ""
    score = ""
    for s in line.split():
        if count == 1:
            name = s
        elif count == 2:
            score = int(s)
        count += 1
    ranklist.append((name, score))
ranklist.sort(key= lambda k:k[1], reverse = True)

f = open("rank.txt", 'w')
for i in range(len(ranklist)):
    if i < 5:
        new_context = str(i + 1) + " " + ranklist[i][0] + " " + str(ranklist[i][1]) + '\n'
        f.write(new_context)
        
f.close()

