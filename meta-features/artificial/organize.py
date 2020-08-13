import csv 

l =  'ClassEnt, AttrEntMin, AttrEntMean, AttrEntMax, JointEnt, MutInfoMin, MutInfoMean, MutInfoMax, EquiAttr,' + \
             'NoiseRatio, StandardDevMin, StandardDevMean, StandardDevMax, SkewnessMin, SkewnessMean, SkewnessMax,' + \
             'KurtosisMin, KurtosisMean, KurtosisMax, treewidth, treeheight, NoNode, NoLeave, maxLevel, meanLevel, devLevel,' + \
             'ShortBranch, meanBranch, devBranch, maxAtt, minAtt, meanAtt, devAtt'
with open("names.csv", "w") as f: 
	f.write(l) 

'''
with open("complexity_uci.txt") as f: 
	reader = csv.reader(f) 
	line = [row for row in reader] 

temp = [] 
for row in line: 
	if len(row) == 0: 
		continue 
	else: 
		temp.append(row) 

with open("complexity.csv", "w", newline="") as f: 
	writer = csv.writer(f) 
	writer.writerows(temp) 
'''