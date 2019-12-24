import csv, os 

debug = False 

home = os.getcwd() 
dataset_path = os.path.join(home, "level1-CVresults") 
acc_path = os.path.join(home, "level1-CV-acc-LS")

if not os.path.exists(acc_path): 
	os.mkdir(acc_path)

os.chdir(dataset_path) 

dataset_cnt = 0
for dataset in os.listdir(dataset_path): 
	if dataset[:2] == "LS": 
		print("dataset " + str(dataset_cnt))
		dataset_cnt += 1
		with open(dataset) as f: 
			reader = csv.reader(f)
			line = [row for row in reader] 
		line = line[1:]

		label = 2 
		res = []
		fold_cnt = 0 
		for outer_fold in range(4, len(line[0]), 3): 
			fold_cnt += 1
			if debug: 
				print("fold cnt: " + str(fold_cnt))
			fold_res = [0 for i in range(10)]
			fold_tst_cnt = [0 for i in range(10)]
			for row in range(len(line)): 
				fold_tst_cnt[int(line[row][outer_fold])] += 1
				if float(line[row][outer_fold+1]) > float(line[row][outer_fold+2]): 
					if float(line[row][label]) == 0.0: 
						fold_res[int(line[row][outer_fold])] += 1
				if float(line[row][outer_fold+1]) < float(line[row][outer_fold+2]): 
					if float(line[row][label]) == 1.0: 
						fold_res[int(line[row][outer_fold])] += 1
			for i in range(10): 
				res.append(fold_res[i]/fold_tst_cnt[i])
			if debug: 
				print(fold_res)
				print(fold_tst_cnt)
		if debug: 
			print(res)

		os.chdir(acc_path)
		result_file_name = dataset[:len(dataset)-4] + ".csv" 
		with open(result_file_name, "w") as f: 
			writer = csv.writer(f)
			writer.writerow(res)
		os.chdir(dataset_path)

	if dataset_cnt == 1800: 
		break 

