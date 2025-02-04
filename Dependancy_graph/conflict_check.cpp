#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
using namespace std;

vector<vector<string>> table;
vector<vector<int>> graph(100, vector<int>(100, 0));
int numRows;
int numCols;

void readInput(){
    ifstream inputFile("test3.txt");
    if (!inputFile) {
        cerr << "Error opening file." << endl;
        return;
    }

    string line;
    while (getline(inputFile, line)) {
        stringstream ss(line);
        string value;
        vector<string> row;

        while (getline(ss, value, ',')) {
            value.erase(0, value.find_first_not_of(" \t"));
            value.erase(value.find_last_not_of(" \t") + 1);
            row.push_back(value);
        }
        table.push_back(row);
    }

    inputFile.close();
    numRows = table.size();
    numCols = numRows > 0 ? table[0].size() : 0;
}

void printInput(){
    cout << "Number of Rows: " << numRows << endl;
    cout << "Number of Columns: " << numCols << endl;
    for (const auto& row : table) {
        for (size_t j = 0; j < row.size(); ++j) {
            cout << row[j] << (j == row.size() - 1 ? "\n" : ", ");
        }
    }
}

void makeGraph(){
    string operation;
    string target;
    int row;
    int startCol;
    for(int i=1; i<numCols; i++){
        for(int j=0; j<numRows; j++){
            if(table[j][i][0] == 'R' || table[j][i][0] == 'W'){
                operation = table[j][i];
                row = j;
                startCol = i;
                // cout << "Operation: " << operation << endl;
                // cout << "Row: " << row << endl;
            }
        }
        for(int j=startCol; j<numCols; j++){
            for (int k=0; k<numRows; k++){
                if(k==row){
                    // cout << "Skipping row: " << row << endl;
                    continue;
                }
                else if(operation[0] == 'R' && table[k][j] == "W" + operation.substr(1)){
                    graph[row][k] = 1;
                    // cout << "Conflict at: " << k << " " << j << endl;
                    // cout<<"graph["<<row<<"]["<<k<<"] = 1"<<endl;
                }
                else if(operation[0] == 'W' && (table[k][j] == "W" + operation.substr(1) || table[k][j] == "R" + operation.substr(1))){
                    graph[row][k] = 1;
                    // cout << "Conflict at: " << k << " " << j << endl;
                    // cout<<"graph["<<row<<"]["<<k<<"] = 1"<<endl;
                }
            }
        }
    }
}

void printGraph(){
    for(int i=0; i<numRows; i++){
        for(int j=0; j<numRows; j++){
            cout << graph[i][j] << " ";
        }
        cout << endl;
    }
}

vector<int> visited;
vector<int> recStack;

bool cycleFoundUtil(int vertex) {
    if (!visited[vertex]) {
        visited[vertex] = 1;
        recStack[vertex] = 1;

        for (int i = 0; i < numRows; ++i) {
            if (graph[vertex][i] == 1) {
                if (!visited[i] && cycleFoundUtil(i)) {
                    return true;
                } else if (recStack[i]) {
                    return true;
                }
            }
        }
    }
    recStack[vertex] = 0;
    return false;
}

bool cycleFound() {
    visited.assign(numRows, 0);
    recStack.assign(numRows, 0);

    for (int i = 0; i < numRows; ++i) {
        if (cycleFoundUtil(i)) {
            return true;
        }
    }
    return false;
}

int main() {

    readInput();
    printInput();

    makeGraph();
    printGraph();
    if(cycleFound()){
        cout<<"Not conflict serializable"<<endl;
    }
    else{
        cout<<"Conflict serializable"<<endl;
    }
    return 0;
}
