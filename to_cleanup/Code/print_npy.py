import numpy as np
import csv
import os

home = os.getcwd()
path = os.path.join(os.getcwd(), "Classical-Decision_Tree")
main_file = "Classical-Decision_Tree.txt"
os.chdir(path)

for dataset in os.listdir(path):
	os.chdir(path)
	file_name = dataset[:(len(dataset)-8)]
	file_path = os.path.join(path, dataset)
	print(file_name)
	file = np.load(file_path)
	file = list(file)
	file.insert(0,str(file_name))
	#print(file)
	os.chdir(home)
	with open(main_file,"a") as f:
		writer = csv.writer(f)
		writer.writerow(file)


