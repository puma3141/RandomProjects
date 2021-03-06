#include "pch.h"
#include <iostream>
#include <fstream>
#include <vector>
#include <stack>
#include <stdlib.h>
#include <string>
#include <unordered_map>

void interprate(std::vector<std::vector<std::string>> parsedInput);

std::string line;
std::ifstream myfile("p1.myl");
std::vector<std::vector<std::string>> parsedInput;
std::stack<int> s;
std::unordered_map<std::string, int> umap;

int main() {
	if (myfile.is_open())
	{
		while (getline(myfile, line))
		{
			std::vector<std::string> input;
			int subStrStart = 0;
			for (int i = 0; i < line.length(); i++) {
				
				if (line[i] == ' '){				
					input.push_back(line.substr(subStrStart, i - subStrStart));
					subStrStart = i;
				}
			}
			input.push_back(line.substr(subStrStart, line.length() - subStrStart));
			parsedInput.push_back(input);
		}
		myfile.close();
	}
	else std::cout << "Unable to open file";
	interprate(parsedInput);
	return 0;
}

void interprate(std::vector<std::vector<std::string>> parsedInput) {
	int i = 0;
	int k;
	while(i<parsedInput.capacity()){
		// fixing spaces so that " INT" is shorted to "INT" (this is def not a place for it, move it to parser)
		for (int j = 0; j < parsedInput[i].capacity(); j++) {
			if (parsedInput[i][j][0] == ' ')
				parsedInput[i][j] = parsedInput[i][j].substr(1, parsedInput[i][j].length() - 1);
			if (parsedInput[i][j][parsedInput[i][j].length() - 1] == ' ')
				parsedInput[i][j] = parsedInput[i][j].substr(0, parsedInput[i][j].length() - 1);
		}
		if (parsedInput[i][0][parsedInput[i][0].length() - 1] == ':') {
			k = 1;
			umap.insert({ parsedInput[i][0], i });
		}
		else
			k = 0;

		if (parsedInput[i][k].compare("PRINT") == 0) {
			std::cout << s.top() << "\n";
		}
		else if (parsedInput[i][k].compare("INT") == 0) {
			s.push(stoi(parsedInput[i][k + 1]));
		}
		else if (parsedInput[i][k].compare("ADD") == 0) {
			int first = s.top();
			s.pop();
			int second = s.top();
			s.pop();
			s.push(first + second);
		}
		else if (parsedInput[i][k].compare("SUB") == 0) {
			int first = s.top();
			s.pop();
			int second = s.top();
			s.pop();
			s.push(second - first);
		}
		else if (parsedInput[i][k].compare("JGE") == 0) {
			if (s.top() >= 0)
				i = umap[parsedInput[i][k + 1]] ;

		}
		else if (parsedInput[i][k].compare("SWAP") == 0) {
			int first = s.top();
			s.pop();
			int second = s.top();
			s.pop();
			s.push(first);
			s.push(second);
		}
		else if (parsedInput[i][k].compare("CALL") == 0) {
			s.push(i + 1);
			umap[parsedInput[i][k + 1]] ;
		}
		else if (parsedInput[i][k].compare("RET") == 0) {
			i = s.top() - 1;
			s.pop();
		}
		else if (parsedInput[i][k].compare("EXIT") == 0) {
			break;
		}
	
		i++;
	}
}
