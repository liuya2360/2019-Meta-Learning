import os, csv 
import numpy as np 
from scipy import stats 

with open("10xfcv-knnallrew-ar2824-accuracy.csv") as f: 
	reader = csv.reader(f) 
	knn_all = [row for row in reader] 

with open("10xfcv-knnsqrt-ar2824-accuracy.csv") as f: 
	reader = csv.reader(f) 
	knn_sqrt = [row for row in reader] 

names = []

for i in range(1, len(knn_all)):
	names.append(knn_all[i][0]) 

labels = [None for i in range(2824)]

knn_sqrt_cnt = 1
for dataset in range(1, len(knn_all)): 
	name = knn_all[dataset][0] 
	if name == knn_sqrt[knn_sqrt_cnt][0]: 
		all_acc = knn_all[dataset][1:] 
		sqrt_acc = knn_sqrt[knn_sqrt_cnt][1:] 

		all_acc = np.array(all_acc).astype(np.float) 
		sqrt_acc = np.array(sqrt_acc).astype(np.float)

		t_test = stats.ttest_ind(all_acc,sqrt_acc) 

		t_test_value = t_test[0]

		#cannot reject null hypothesis 
		if t_test[1] > 0.05:
			t_test_value = 0 

		#if t test result is positive, algo1 is better, if t test result is negative, algo2 is better, if t test result is 0, then draw
		if t_test_value == 0:
			labels[dataset-1] = 0
		elif t_test_value > 0:
			labels[dataset-1] = 1
		elif t_test_value < 0:
			labels[dataset-1] = 2  

		knn_sqrt_cnt += 1


cnt0 = 0 
cnt1 = 0 
cnt2 = 0 

for i in range(len(labels)): 
	if labels[i] == 0: 
		cnt0 += 1 
	elif labels[i] == 1: 
		cnt1 += 1 
	else: 
		cnt2 += 1 

print(cnt0) 
print(cnt1) 
print(cnt2) 

with open("knn_t_test.csv", "w") as f: 
	writer = csv.writer(f) 
	writer.writerow(labels) 

