from matplotlib import pyplot as plt 
import csv 
import os 
import time 
import seaborn as sns
import numpy as np 

home = os.getcwd()
dataset_folder = os.path.join(home, "artificial-results-n")
figure_folder = os.path.join(home, "distribution")
if not os.path.exists(figure_folder):
	os.mkdir(figure_folder)

cnt = 0
#bin_list = []
#for i in range(41): 
	#bin_list.append(0.025*i)
#print(bin_list)
bin_list = 20

for dataset in os.listdir(dataset_folder):
	#new_start = time.time()
	print("count", cnt)
	#if cnt == 3:
		#break 
	os.chdir(dataset_folder)
	with open(dataset, "r") as f:
		reader = csv.reader(f)
		line = [row for row in reader]

	'''
	#print(line[0][3], line[0][46], line[0][89], line[0][132])
	alpha_shift_pos = [47,91,135]
	for i in range(3): 
		print(line[0][alpha_shift_pos[i]])
	'''
	line.pop(0)

	#plot the distribution of alpha of original dataset 
	alpha = []
	for i in range(len(line)): 
		alpha.append(float(line[i][3]))
	alpha = np.array(alpha).astype(np.float)
	os.chdir(figure_folder)
	plt.clf()
	#plt.hist(alpha, bins=10, range=(0.0,1.0))
	sns.distplot(alpha, bins=bin_list, kde=False)
	figure_name = dataset[:len(dataset)-14] + ".png"
	plt.savefig(figure_name, dpi=300)
	os.chdir(dataset_folder)

	algo_name = ["knn","nb","dt"]
	alpha_pos = [46,90,134]
	alpha_shift_pos = [47,91,135]

	for algo in range(3): 
		temp_alpha = []
		for i in range(len(line)): 
			temp_alpha.append(line[i][alpha_pos[algo]])
		#print(temp_alpha)
		#print(min(temp_alpha))
		#print(max(temp_alpha))

		figure_name = dataset[:len(dataset)-14] + "_" + algo_name[algo] + ".png"
		os.chdir(figure_folder)
		plt.clf()
		#plt.hist(temp_alpha, bins=10, range=(0.0,1.0))
		temp_alpha = np.array(temp_alpha).astype(np.float)
		sns.distplot(temp_alpha, bins=bin_list, kde=False)
		plt.savefig(figure_name, dpi = 300)

		temp_alpha_shift = []
		for i in range(len(line)): 
			temp_alpha_shift.append(line[i][alpha_shift_pos[algo]])
		figure_name = dataset[:len(dataset)-14] + "_" + algo_name[algo] + "_shift.png"
		plt.clf()
		temp_alpha_shift = np.array(temp_alpha_shift).astype(np.float)
		sns.distplot(temp_alpha_shift, bins=bin_list, kde=False)
		plt.savefig(figure_name, dpi=300)
		os.chdir(dataset_folder)

	cnt += 1

