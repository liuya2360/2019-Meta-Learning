import csv, os 
import numpy as np  
from scipy import stats

debug = True 

home = os.getcwd() 
acc_path = os.path.join(home, "level1-CV-acc-LS")

os.chdir(acc_path)

algo_list = ["DT", "KNN", "NB"]

acc = [[None for j in range(200)] for i in range(3)]
acc_ave = [[None for j in range(200)] for i in range(3)]

naming_list = ["A","B","V","G","D"]

dataset_cnt = 9 
for dataset in os.listdir(acc_path): 
	if dataset[:2] == "LS" and dataset[7:10] == "KNN":
		dataset_cnt += 1
		for i in range(3): 
			if algo_list[i] == dataset[len(dataset)-4-len(algo_list[i]): len(dataset)-4]: 
				algo = i 
		#print(dataset)
		dataset_n = int((int(dataset[2:4])/2-1)*20 + (naming_list.index(dataset[4])*4) + int(dataset[5]) - 1)
		#print("dataset "+ str(dataset_n)) 

		with open(dataset) as f: 
			reader = csv.reader(f) 
			line = [row for row in reader] 

		data = line[0] 
		temp = [] 
		for i in range(10): 
			ave = 0 
			for j in range(10): 
				ave += float(data[10*i+j])
			ave /= 10 
			temp.append(ave)

		acc[algo][dataset_n] = temp[:]
		line = np.array(line).astype(np.float) 
		acc_ave[algo][dataset_n] = np.sum(line)/len(line)

#print(acc_ave)
#print(dataset_cnt)

if debug: 
	print("Average calculation DONE")

meta_labels = []

for dataset in range(200): 
	if debug: 
		print("dataset " + str(dataset))
	best_algo = 0 
	try: 
		for algo in range(1,3): 
			if acc_ave[algo][dataset] > acc_ave[best_algo][dataset]: 
				best_algo = algo

		dataset_label = [None for i in range(3)]
		for algo in range(3): 
			if algo == best_algo: 
				dataset_label[algo] = 1
			else: 
				list1 = np.array(acc[best_algo][dataset]).astype(np.float)
				list2 = np.array(acc[algo][dataset]).astype(np.float)
				t_test = stats.ttest_ind(list1 , list2)
				t_test_value = t_test[0]

				if t_test[1] > 0.05:
					t_test_value = 0

				#if t test result is positive, algo1 is better, if t test result is negative, algo2 is better, if t test result is 0, then draw
				if t_test_value <= 0: 
					dataset_label[algo] = 1
				else: 
					dataset_label[algo] = 0
		meta_labels.append(dataset_label)
	except: 
		meta_labels.append([None for i in range(3)])

os.chdir(home)
with open("meta_labels_LS_KNN.csv", "w") as f: 
	writer = csv.writer(f) 
	writer.writerows(meta_labels) 