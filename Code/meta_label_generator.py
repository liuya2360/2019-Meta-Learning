import os, csv 
import numpy as np 
from scipy import stats 

n_ins = 2824 #number of instances 

with open("10xfcv-knnallrew-ar2824-accuracy.csv") as f: 
	reader = csv.reader(f) 
	knn_acc = [row for row in reader] 

with open("10xfcv-nbpkid-ar2824-accuracy.csv") as f: 
	reader = csv.reader(f) 
	nb_acc = [row for row in reader] 

with open("10xfcv-dtc44-ar2824-accuracy.csv") as f: 
	reader = csv.reader(f) 
	dt_acc =  [row for row in reader] 

check = [0 for i in range(n_ins)] 

#all accuracies are arranged in the same order 

t_test_results = [[None for i in range(3)] for j in range(n_ins)] 

with open("t_test_error.txt", "w") as f: 
	pass 

def paired_t_test(algo1, algo2, dataset): 
	algo1_acc = algo1[dataset][1:] 
	algo2_acc = algo2[dataset][1:] 

	algo1_acc = np.array(algo1_acc).astype(np.float) 
	algo2_acc = np.array(algo2_acc).astype(np.float)

	t_test = stats.ttest_ind(algo1_acc, algo2_acc) 

	t_test_value = t_test[0]

	#cannot reject null hypothesis 
	if t_test[1] > 0.05:
		t_test_value = 0 

	#if t test result is positive, algo1 is better, if t test result is negative, algo2 is better, if t test result is 0, then draw
	if t_test_value == 0:
		label = 0
	elif t_test_value > 0:
		label = 1
	elif t_test_value < 0:
		label = 2 
	else: 
		label = t_test_value 
		with open("t_test_error.txt", "a") as f: 
			f.write(algo1[dataset][0] + ",") 

	return label 

#knn vs nb 
for dataset in range(1, n_ins+1): 
	label_temp = paired_t_test(knn_acc, nb_acc, dataset) 
	t_test_results[dataset-1][0] = label_temp

print("knn vs nb t-test DONE")

#knn vs dt 
for dataset in range(1, n_ins+1): 
	label_temp = paired_t_test(knn_acc, dt_acc, dataset) 
	t_test_results[dataset-1][1] = label_temp

print("knn vs dt t-test DONE") 

#nb vs dt 
for dataset in range(1, n_ins+1): 
	label_temp = paired_t_test(nb_acc, dt_acc, dataset) 
	t_test_results[dataset-1][2] = label_temp

print("nb vs dt t-test DONE")

with open("paired_t_test_raw_results.csv", "w") as f: 
	writer = csv.writer(f) 
	writer.writerows(t_test_results) 

#check contradictions and generate labels 
labels_check = [[[-1 for i in range(3)] for j in range(3)] for k in range(3)] 
labels_check[0][0][0] = 0 
labels_check[1][1][0] = 1 
labels_check[1][1][1] = 1 
labels_check[1][1][2] = 1 
labels_check[2][0][1] = 2
labels_check[2][1][1] = 2 
labels_check[2][2][1] = 2 
labels_check[0][2][2] = 3 
labels_check[1][2][2] = 3 
labels_check[2][2][2] = 3 
labels_check[0][1][1] = 4
labels_check[1][0][2] = 5 
labels_check[2][2][0] = 6 

with open("contradictions.txt", "w") as f: 
	pass 

labels = []

for dataset in range(n_ins): 
	t_test_temp = t_test_results[dataset] 
	if not t_test_temp[0] in [0,1,2] or not t_test_temp[1] in [0,1,2] or not t_test_temp[2] in [0,1,2]: 
		continue 
	if labels_check[t_test_temp[0]][t_test_temp[1]][t_test_temp[2]] == -1: 
		with open("contradictions", "a") as f: 
			f.write(knn_acc[dataset+1][0] + ",") 
	else: 
		temp = []
		temp.append(knn_acc[dataset+1][0]) 
		temp.append(labels_check[t_test_temp[0]][t_test_temp[1]][t_test_temp[2]]) 
		labels.append(temp) 

with open("labels.csv", "w") as f: 
	writer = csv.writer(f) 
	writer.writerows(labels) 

