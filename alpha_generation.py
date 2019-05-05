import csv
from matplotlib import pyplot as plt 
import os

home = os.getcwd()
dataset_folder = os.path.join(home, "artificial-results")
figure_folder = os.path.join(home, "distribution")
if not os.path.exists(figure_folder):
	os.mkdir(figure_folder)
new_dataset_folder = os.path.join(home, "new_datasets")
if not os.path.exists(new_dataset_folder): 
	os.mkdir(new_dataset_folder)

def get_dis(A, B): 
	if len(A) != len(B): 
		raise ValueError
	else: 
		dis = 0
		for i in range(len(A)): 
			dis += (A[i]+B[i])**2 
	return dis**0.5

def get_neighbours(i, n_neighbours, X): 
	neighbours = []
	vis = [0 for i in range(len(X))]
	while n_neighbours > 0:
		#print("n_neighbours",n_neighbours)
		minn = None 
		new_point = None  
		for j in range(len(X)):
			if vis[j] == 0: 
				dis = get_dis(X[i], X[j])
				if minn == None or dis < minn: 
					minn = dis
					new_point = j
		vis[new_point] = 1
		neighbours.append(new_point)
		#print(new_point)
		n_neighbours -= 1
	#print(neighbours)
	return neighbours 

cnt = 0

for dataset in os.listdir(dataset_folder):
	print("count", cnt)
	if cnt == 1:
		break 
	os.chdir(dataset_folder)
	with open(dataset, "r") as f:
		reader = csv.reader(f)
		line = [row for row in reader]

	new_dataset_file = dataset[:len(dataset)-12] + "alpha_all.csv" 

	os.chdir(new_dataset_folder)
	with open(new_dataset_file, "w") as f:
		writer = csv.writer(f)
		writer.writerows(line)
	os.chdir(dataset_folder)

	line.pop(0)

	
	#copy the class labels of the dataset
	Y = []
	class_wise_cnt = [0, 0]
	for i in range(len(line)):
		Y.append(int(float(line[i][2])))
		class_wise_cnt[Y[i]] += 1

	#plot the distribution of alpha of original dataset 
	alpha = []
	for i in range(len(line)): 
		alpha.append(float(line[i][3]))
	os.chdir(figure_folder)
	plt.clf()
	plt.hist(alpha, bins=20)
	figure_name = dataset[:len(dataset)-12] + ".png"
	plt.savefig(figure_name, dpi=300)
	os.chdir(dataset_folder)

	#for each algorithm
	for l in range(3):
		print("algorithm"+str(l+1))
		#for each cv
		alpha_all = []
		for fold in range(10):
			print("fold", fold)
			X = []
			alpha = []
			for i in range(len(line)):
				temp = []
				temp.append(float(line[i][5+10*3*l+fold*3]))
				temp.append(float(line[i][6+10*3*l+fold*3]))
				X.append(temp)
			
			for i in range(len(X)): 
				#print("instance", i)
				cnt_neighbour_same_label = 0
				for j in get_neighbours(i, class_wise_cnt[Y[i]],X):
					if Y[i] == Y[j]: 
						cnt_neighbour_same_label += 1
				alpha.append(cnt_neighbour_same_label/(class_wise_cnt[Y[i]]-1))

			alpha_all.append(alpha)

			
			#save the alpha to the file
			os.chdir(new_dataset_folder)
			with open(new_dataset_file, "r") as f:
				reader = csv.reader(f)
				data = [row for row in reader]
			data[0].insert(7+10*4*l+fold*4+cnt, "alpha")
			for i in range(len(line)):
				data[i+1].insert(7+10*4*l+fold*4+cnt, alpha[i])
			with open(new_dataset_file, 'w') as f: 
				writer = csv.writer(f)
				writer.writerows(data)
			os.chdir(dataset_folder)

		#calculate the average alpha over 10 folds
		ave_alpha = []
		for i in range(len(alpha_all[0])): 
			temp  = 0
			for j in range(len(alpha_all)): 
				temp += alpha_all[j][i]
			temp /= len(alpha_all)
			ave_alpha.append(temp)

		#plot the distribution of alpha 
		os.chdir(figure_folder)
		plt.clf()
		plt.hist(ave_alpha, bins=20) 
		figure_name = dataset[:len(dataset)-12] + '_' + str(l) + ".png"
		plt.savefig(figure_name, dpi=300)

		#save average alpha 
		os.chdir(new_dataset_folder)
		with open(new_dataset_file, "r") as f:
			reader = csv.reader(f)
			data = [row for row in reader]
		data[0].append("algorithm"+str(l))
		for i in range(len(line)): 
			data[i+1].append(ave_alpha[i])
		with open(new_dataset_file, "w") as f:
			writer = csv.writer(f)
			writer.writerows(data)
		os.chdir(dataset_folder)
	cnt += 1