#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <string>
#include <string.h>
#include <regex>
#include <cstdlib>

using namespace std;

struct Column
{
    int index;
    float cost;
    float costFunctionValue;
    vector<int> coveredRows;

    bool operator==(const Column &other) const
    {
        return index == other.index &&
               cost == other.cost &&
               coveredRows == other.coveredRows;
    }
};

bool compareColumns(const Column &a, const Column &b)
{
    return a.costFunctionValue < b.costFunctionValue;
}

// Cost functions proposed by Vasco and Wilson (1984)
float costFunction1(float cj, float kj)
{
    return cj;
}

float costFunction2(float cj, float kj)
{
    return cj / kj;
}

float costFunction3(float cj, float kj)
{
    return cj / log2(kj);
}

float costFunction4(float cj, float kj)
{
    return cj / (kj * log2(kj));
}

float costFunction5(float cj, float kj)
{
    return cj / (kj * log(kj));
}

float costFunction6(float cj, float kj)
{
    return cj / pow(kj, 2);
}

float costFunction7(float cj, float kj)
{
    return sqrt(cj) / pow(kj, 2);
}

int getFileData(string fileName, vector<pair<int, float>> *columnAndCost, vector<vector<int>> *linesThatCoverColumn, int *numRows, int *numColumns)
{
    // Open a file for reading
    ifstream inputFile(fileName);

    // Check if the file is open
    if (!inputFile.is_open())
    {
        cerr << "Erro na abertura de arquivo!" << endl;
        return 1;
    }

    regex numberRegex("\\b\\d+\\b");

    // Read data from the file
    string line;

    while (getline(inputFile, line))
    {
        smatch match;
        if (regex_search(line, match, numberRegex))
        {
            *numRows = stoi(match.str());
            break;
        }
    }

    while (getline(inputFile, line))
    {
        smatch match;
        if (regex_search(line, match, numberRegex))
        {
            *numColumns = stoi(match.str());
            break;
        }
    }

    getline(inputFile, line); // Data label

    while (getline(inputFile, line))
    {
        istringstream iss(line);
        // Read the first two values
        int value1;
        float value2;
        if (!(iss >> value1 >> value2))
        {
            cerr << "Error reading the first two values from a line." << endl;
            return 1; // Return an error code
        }

        columnAndCost->push_back(make_pair(value1, value2));

        // Read the remaining values
        vector<int> remaining;
        int value;
        while (iss >> value)
        {
            remaining.push_back(value);
        }

        linesThatCoverColumn->push_back(remaining);
    }

    // Close the file
    inputFile.close();

    return 0;
}

vector<int> updateGlobalCoveredRows(vector<int> &globalCoveredRows, vector<int> &coveredRows)
{
    vector<int> aux = globalCoveredRows;
    for (int i : coveredRows)
    {
        aux[i - 1] = 1;
    }

    return aux;
}

vector<Column> createColumns(vector<pair<int, float>> columnAndCost, vector<vector<int>> linesThatCoverColumn, int numRows, int numCols)
{
    vector<Column> columns(numCols);

    for (int j = 0; j < numCols; ++j)
    {
        columns[j].index = columnAndCost[j].first;
        columns[j].cost = columnAndCost[j].second;
        columns[j].coveredRows = linesThatCoverColumn[j];
    }

    return columns;
}

float getMaxCost(const vector<Column> &columns)
{
    float maxCost = 0;
    for (const Column &column : columns)
    {
        if (column.cost > maxCost)
        {
            maxCost = column.cost;
        }
    }
    return maxCost;
}

void displayResult(vector<Column> solution)
{
    float totalCost = 0;

    cout << "Primary Cover: ";
    for (Column selectedColumn : solution)
    {
        cout << selectedColumn.index << " ";
        totalCost += selectedColumn.cost;
    }
    cout << endl;
    cout << "Total Cost: " << totalCost << endl;
}

vector<Column> greedyAlgorithm(vector<pair<int, float>> columnAndCost, vector<vector<int>> linesThatCoverColumn, int numRows, int numCols)
{
    vector<int> newGlobalCoveredRows;
    vector<Column> solution;

    int kj = 0;

    vector<Column> columns = createColumns(columnAndCost, linesThatCoverColumn, numRows, numCols);
    vector<int> globalCoveredRows(numRows, 0);

    while (count(globalCoveredRows.begin(), globalCoveredRows.end(), 1) < numRows)
    {
        for (int j = 0; j < numCols; ++j)
        {
            // calculate kj (number of lines not yet covered that can be covered by the column j)

            int alreadyCoveredRows = count(globalCoveredRows.begin(), globalCoveredRows.end(), 1);

            vector<int> aux = updateGlobalCoveredRows(globalCoveredRows, columns[j].coveredRows);

            int newCoveredRows = count(aux.begin(), aux.end(), 1);

            kj = newCoveredRows - alreadyCoveredRows;

            // Randomly choose a cost function
            int costFunction = 2;

            if (kj == 0)
            {
                columns[j].costFunctionValue = INT64_MAX;
                continue;
            }

            switch (costFunction)
            {
            case 1:
                columns[j].costFunctionValue = costFunction1(columns[j].cost, kj);
                break;
            case 2:
                columns[j].costFunctionValue = costFunction2(columns[j].cost, kj);
                break;
            case 3:
                columns[j].costFunctionValue = costFunction3(columns[j].cost, kj);
                break;
            case 4:
                columns[j].costFunctionValue = costFunction4(columns[j].cost, kj);
                break;
            case 5:
                columns[j].costFunctionValue = costFunction5(columns[j].cost, kj);
                break;
            case 6:
                columns[j].costFunctionValue = costFunction6(columns[j].cost, kj);
                break;
            case 7:
                columns[j].costFunctionValue = costFunction7(columns[j].cost, kj);
                break;
            default:
                cerr << "Invalid cost function." << endl;
                exit(1);
            }
        }
        sort(columns.begin(), columns.end(), compareColumns);
        solution.push_back(columns[0]);
        globalCoveredRows = updateGlobalCoveredRows(globalCoveredRows, columns[0].coveredRows);
        for (int i : globalCoveredRows)
        {
            cout << i << " ";
        }
        cout << endl;
    }

    return solution;
}
vector<Column> localSearch(vector<Column> allColumns, vector<Column> initialSolution, int numRows, int numCols)
{
    vector<Column> solution = initialSolution;
    vector<Column> notInSolution;
    float N_S = solution.size();
    int d = 0;

    // get the greatest cost on solution
    float Q_S = 0;
    for (Column column : solution)
    {
        if (column.cost > Q_S)
        {
            Q_S = column.cost;
        }
    }

    float greatestCost = getMaxCost(allColumns);

    float p1 = N_S / numCols;
    float p2 = (Q_S == 0) ? 0 : Q_S / greatestCost;

    // generate random number between two limits

    float D = ceil(p1 * N_S);
    float E = ceil(p2 * Q_S);

    // insert in notInSolution all columns that are not in the initial solution
    for (Column column : allColumns)
    {
        if (find(initialSolution.begin(), initialSolution.end(), column) == initialSolution.end())
        {
            notInSolution.push_back(column);
        }
    }

    // Number of columns that cover each row
    vector<int> wi(numRows, 0);

    for (Column column : solution)
    {
        for (int row : column.coveredRows)
        {
            wi[row - 1]++;
        }
    }

    // Step 1:
    while (d < D)
    {
        int randomColumnIndex = rand() % solution.size();
        for (int row : solution[randomColumnIndex].coveredRows)
        {
            wi[row - 1]--;
        }

        solution.erase(solution.begin() + randomColumnIndex);

        notInSolution.push_back(solution[randomColumnIndex]);
        d++;
    }

    vector<int> U{};
    for (int i = 0; i < numRows; i++)
    {
        if (wi[i] == 0)
        {
            U.push_back(i);
        }
    }

    while (!U.empty())
    {
        vector<Column> Se;
        for (Column column : notInSolution)
        {
            if (column.cost < E)
            {
                Se.push_back(column);
            }
        }

        // Step 4:
        vector<vector<int>> aij(numRows, vector<int>(numCols, 0));
        for (int i = 0; i < numRows; i++)
        {
            for (int j = 0; j < numCols; j++)
            {
                if (wi[i] == 0 && find(Se.begin(), Se.end(), allColumns[j]) != Se.end())
                {
                    aij[i][j] = 1;
                }
                else
                {
                    aij[i][j] = 0;
                }
            }
        }

        // vj is the sum of all the elements in aij where j is in Se
        vector<int> vj(numCols, 0);
        for (int j = 0; j < numCols; j++)
        {
            if (find(Se.begin(), Se.end(), allColumns[j]) != Se.end())
            {
                for (int i = 0; i < numRows; i++)
                {
                    vj[j] += aij[i][j];
                }
            }
        }

        vector<float> Bj;
        for (Column column : Se)
        {
            if (vj[column.index] != 0)
            {
                Bj.push_back(column.cost / vj[column.index]);
            }
            else
            {
                // Handle division by zero if vj is zero
                Bj.push_back(0);
            }
        }

        float minBj = INT64_MAX;
        for (float i : Bj)
        {
            if (i < minBj)
            {
                minBj = i;
            }
        }

        // K has all the columns where Bj is equal to minBj in Se
        vector<Column> K;
        for (int i = 0; i < Bj.size(); i++)
        {
            if (Bj[i] == minBj)
            {
                K.push_back(Se[i]);
            }
        }

        // Select a random Column from K and add it to the solution and remove it from notInSolution
        int randomColumnIndex = rand() % K.size();
        solution.push_back(K[randomColumnIndex]);
        notInSolution.erase(find(notInSolution.begin(), notInSolution.end(), K[randomColumnIndex]));

        // update wi
        for (int row : K[randomColumnIndex].coveredRows)
        {
            wi[row - 1]++;
        }

        U.clear();
        for (int i = 0; i < numRows; i++)
        {
            if (wi[i] == 0)
            {
                U.push_back(i);
            }
        }

        // show all variables
        cout << "d: " << d << endl;
        cout << "D: " << D << endl;
        cout << "E: " << E << endl;
        cout << "N_S: " << N_S << endl;
        cout << "p1: " << p1 << endl;
        cout << "p2: " << p2 << endl;
        cout << "Q_S: " << Q_S << endl;
        cout << "Se: ";
        for (Column column : Se)
        {
            cout << column.index << " ";
        }
        cout << endl;
        cout << "vj: ";
        for (int i : vj)
        {
            cout << i << " ";
        }
        cout << endl;
        cout << "Bj: ";
        for (float i : Bj)
        {
            cout << i << " ";
        }
        cout << endl;
        cout << "minBj: " << minBj << endl;
        cout << "K: ";
        for (Column column : K)
        {
            cout << column.index << " ";
        }
        cout << endl;
        cout << "U: ";
        for (int i : U)
        {
            cout << i << " ";
        }
        cout << endl;
        cout << "wi: ";
        for (int i : wi)
        {
            cout << i << " ";
        }
        cout << endl;
        cout << "Solution: ";
        for (Column column : solution)
        {
            cout << column.index << " ";
        }
        cout << endl;
        cout << "Not in solution: ";
        for (Column column : notInSolution)
        {
            cout << column.index << " ";
        }
        cout << endl;
    }

    // Step 6:
    sort(solution.begin(), solution.end(), compareColumns);

    for (int i = solution.size() - 1; i >= 0; i--)
    {
        bool canBeRemoved = true;
        for (int row : solution[i].coveredRows)
        {
            if (wi[row - 1] - 1 < 0)
            {
                canBeRemoved = false;
                break;
            }
        }

        if (canBeRemoved)
        {
            for (int row : solution[i].coveredRows)
            {
                wi[row - 1]--;
            }
            solution.erase(solution.begin() + i);
        }
    }

    return solution;
}

int main()
{
    vector<pair<int, float>> columnAndCost;
    vector<vector<int>> linesThatCoverColumn;
    int numRows;
    int numCols;

    cout << "Input the file name to be read: ";
    string fileName;
    cin >> fileName;

    if (getFileData(fileName, &columnAndCost, &linesThatCoverColumn, &numRows, &numCols) != 0)
    {
        cerr << "Error reading data from the file." << endl;
        return 1;
    }

    vector<Column> columns = createColumns(columnAndCost, linesThatCoverColumn, numRows, numCols);
    vector<Column> greedySolution;
    vector<Column> localSearchSolution;

    greedySolution = greedyAlgorithm(columnAndCost, linesThatCoverColumn, numRows, numCols);

    displayResult(greedySolution);

    // localSearchSolution = localSearch(columns, greedySolution, numRows, numCols);

    // displayResult(localSearchSolution);

    return 0;
}