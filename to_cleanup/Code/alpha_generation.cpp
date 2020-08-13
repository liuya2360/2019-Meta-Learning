#include<iostream> 
#include<fstream> 
#include<vector>
using namespace std;

std::vector read_csv(string file_name)
{
	fstream fio;
	fio.open(file_name);
	vector<vector<string>> data;
	vector<string> row;
	while(fio){
		row.clear();
		string line, word;
		getline(fio, line);//read one row and store it in a string variable 'line' 
		stringstream s(line); // used for breaking words 
		//read every column data of a row and store it in a string variable, 'word' 
		while (getline(s, word, ',')) { 
			row.push_back(word); //add all the column data of a row to a vector 
		} 
		data.push_back(row);
	}
	return data;
}

int main()
{
	fstream fio; // Creation of fstream class object 
	fio.open("sample.txt"); // by default openmode = ios::in|ios::out mode 

	fio.seekg(0, ios::beg); // point read pointer at beginning of file 
	/*
	string line;
	while (fio) { 
		// Read a Line from File 
		getline(fio, line); 
		// Print line in Console 
		cout << line << endl; 
	} 
	// Close the file 
	fio.close(); 
	*/

	vector<vector<string>> data;
	data.clear();
	data.push_back(read_csv("sample.txt"))
	for(int i = 0; i < data.size(); i++){
		for(int j = 0; j < data[i].size(); j++)
			cout << data[i][j] << ',';
		cout << endl;
	}


	return 0;
}