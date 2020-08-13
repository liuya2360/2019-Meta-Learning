from matplotlib import pyplot as plt 
import csv 
import os 

home = os.getcwd()
dataset_folder = os.path.join(home, "main_folder")
figure_folder = os.path.join(home, "dataset_visualisation")
if not os.path.exists(figure_folder):
	os.mkdir(figure_folder)

cnt = 0

for dataset in os.listdir(dataset_folder): 
	dataset_n = dataset[:len(dataset)-4]
	print("cnt:", cnt)

	os.chdir(dataset_folder)
	with open(dataset, 'r') as f: 
		reader = csv.reader(f)
		raw_data = [row for row in reader]

	label_wise = [[] for i in range(2)]
	for i in range(len(raw_data)): 
		label_wise[int(float(raw_data[i][2]))].append(i)

	label_color = ["#005BBB", "#FFD500"]
	plt.clf()
	for label in range(2): 
		x_axis = [] 
		y_axis = [] 
		for i in label_wise[label]:
			x_axis.append(float(raw_data[i][0]))
			y_axis.append(float(raw_data[i][1]))
		plt.plot(x_axis, y_axis, "ro", color=label_color[label])

	os.chdir(figure_folder)
	figure_name = dataset_n + ".png"
	plt.savefig(figure_name, dpi=300)
	cnt += 1