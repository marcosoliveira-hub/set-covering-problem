import random
import math
from timeit import default_timer as timer

class Column:
    """
    Represents a column in the input file
    """
    def __init__(self, index, cost, coveredRows):
        self.index: int = index
        self.cost: float = cost
        self.coveredRows: list[int] = coveredRows

def compareColumns(a, b):
    """
    Compares two columns by their cost function value
    """
    return a.costFunctionValue < b.costFunctionValue

def costFunction1(cj, kj):
    return cj

def costFunction2(cj, kj):
    return cj / kj

def costFunction3(cj, kj):
    return cj / math.log2(kj) if kj != 1 else float('inf')

def costFunction4(cj, kj):
    return cj / (kj * math.log2(kj)) if kj != 1 else float('inf')

def costFunction5(cj, kj):
    return cj / (kj * math.log(kj)) if kj != 1 else float('inf')

def costFunction6(cj, kj):
    return cj / (kj ** 2)

def costFunction7(cj, kj):
    return math.sqrt(cj) / (kj ** 2)

def getFileData(fileName):
    """
    Takes the file name as input and returns the data from the file, the
    file data must be in the following format:
    
    rowslabel <number of rows>
    columnslabel <number of columns>
    datalabel
    <column index> <column cost> <row index> <row index> ...
    """
    columnAndCost = []
    linesThatCoverColumn = []
    numRows = 0
    numColumns = 0

    with open(fileName, 'r') as file:
        data = file.readlines()

        numRows = int(data[0].split()[1])
        numColumns = int(data[1].split()[1])

        for line in data[3:]:
            values = line.split()
            values = [int(values[0]), float(values[1])] + [int(v) for v in values[2:]]
            columnAndCost.append((values[0], values[1]))
            linesThatCoverColumn.append(values[2:])

    return columnAndCost, linesThatCoverColumn, numRows, numColumns

def updateGlobalCoveredRows(globalCoveredRows, coveredRows) -> list[int]:
    """
    Auxiliar function to update the global covered rows list using the
    covered rows of the current column
    """
    aux = globalCoveredRows.copy()
    for i in coveredRows:
        aux[i - 1] = 1

    return aux

def createColumns(columnAndCost, linesThatCoverColumn) -> list[Column]:
    """
    Creates a list of columns, where each column has its index, cost and the lines that it covers
    """
    columns = []
    for j in range(len(columnAndCost)):
        columns.append(Column(columnAndCost[j][0], columnAndCost[j][1], linesThatCoverColumn[j]))

    return columns

def displayResult(solution) -> None:
    """
    Shows the result of the algorithm, which is the selected columns and the total cost of the solution
    """
    totalCost = calcTotalCost(solution)
    print("Selected Columns:", [selectedColumn.index for selectedColumn in solution])
    print("Total Cost:", totalCost)

def calcTotalCost(solution) -> float:
    totalCost = 0
    for column in solution:
        totalCost += column.cost

    return totalCost

def verifySolution(solution, numRows) -> bool:
    """
    Verifies if the solution is valid, i.e., if all rows are covered
    """
    coveredRows = [0] * numRows
    for column in solution:
        for row in column.coveredRows:
            coveredRows[row - 1] += 1

    for i in coveredRows:
        if i == 0:
            return False

    return True

def construction1(columns, numRows, numColumns) -> list[Column]:
    """
    Greedy Construction 1 -> Selects the column that has the best cost per covered row,
    where the cost per covered row is calculated by a cost function, which can be:
    1 - cj
    2 - cj / kj
    3 - cj / log2(kj)
    4 - cj / (kj * log2(kj))
    5 - cj / (kj * log(kj))
    6 - cj / (kj ** 2)
    7 - sqrt(cj) / (kj ** 2)
    Where cj is the cost of the column and kj is the number of uncovered rows covered by the column
    In this implementation, the cost function is randomly chosen for each column added to the solution
    """
    
    solution = []
    kj = 0

    globalCoveredRows = [0] * numRows

    while globalCoveredRows.count(1) < numRows:
        for j in range(numColumns):
            alreadyCoveredRows = globalCoveredRows.count(1)
            aux = updateGlobalCoveredRows(globalCoveredRows, columns[j].coveredRows)
            newCoveredRows = aux.count(1)
            kj = newCoveredRows - alreadyCoveredRows

            costFunction = 2

            if kj == 0:
                columns[j].costFunctionValue = float('inf')
                continue

            if costFunction == 1:
                columns[j].costFunctionValue = costFunction1(columns[j].cost, kj)
            elif costFunction == 2:
                columns[j].costFunctionValue = costFunction2(columns[j].cost, kj)
            elif costFunction == 3:
                columns[j].costFunctionValue = costFunction3(columns[j].cost, kj)
            elif costFunction == 4:
                columns[j].costFunctionValue = costFunction4(columns[j].cost, kj)
            elif costFunction == 5:
                columns[j].costFunctionValue = costFunction5(columns[j].cost, kj)
            elif costFunction == 6:
                columns[j].costFunctionValue = costFunction6(columns[j].cost, kj)
            elif costFunction == 7:
                columns[j].costFunctionValue = costFunction7(columns[j].cost, kj)
            else:
                print("Invalid cost function.")
                exit(1)

        columns.sort(key=lambda x: x.costFunctionValue)
        solution.append(columns[0])
        globalCoveredRows = updateGlobalCoveredRows(globalCoveredRows, columns[0].coveredRows)

    if(not verifySolution(solution, numRows)):
        print("Solution is invalid.")
        exit(1)
    
    return solution


def construction2(columns, numRows):
    """
    Selects the column that covers the most uncovered rows
    independent of the cost of the column
    """

    solution = []
    notInSolution = columns.copy()
    uncoveredRows = set(range(1, numRows + 1))
    
    while len(uncoveredRows) > 0:
        bestColumn = max(notInSolution, key=lambda x: len(uncoveredRows & set(x.coveredRows)))
        
        uncoveredRows -= set(bestColumn.coveredRows)
        
        solution.append(bestColumn)
        
        notInSolution.remove(bestColumn)
    
    if(not verifySolution(solution, numRows)):
        print("Solution is invalid.")
        exit(1)
    
    return solution
        

def getCoveredRows(columns, numRows) -> list[int]:
    coveredRows = [0] * numRows
    for column in columns:
        for row in column.coveredRows:
            coveredRows[row - 1] += 1

    return coveredRows


def localSearchAlgorithm(columns, initialSolution, numRows, isBestImprovement = True):
    """
    Local Search Algorithm -> Removes D random columns from the solution and adds columns
    from the line that covers the most uncovered rows, until there are no uncovered rows left.
    Then, removes columns that if removed would not leave any uncovered rows, until there are no
    such columns left.
    """

    S = initialSolution.copy()
    
    N_S = len(S)
    
    Q_S = max(column.cost for column in S)
    
    S_line = [column for column in columns if column not in initialSolution]
    
    p1 = random.uniform(0.2, 0.7)
    p2 = random.uniform(1.1, 3)
    
    D = math.ceil(N_S * p1)
    E = math.ceil(Q_S * p2)
    
    solutionCoveredRows = getCoveredRows(S, numRows)
    
    d = 0
    while d < D:
        randomColumn = S[random.randint(0, len(S) - 1)]
        S.remove(randomColumn)
        S_line.append(randomColumn)
        for line in randomColumn.coveredRows:
            solutionCoveredRows[line - 1] -= 1
        d += 1
    
    U = [i + 1 for i in range(numRows) if solutionCoveredRows[i] == 0]
    
    while len(U) > 0:
        S_line_E = [column for column in S_line if column.cost <= E]
        
        alpha = []
        for column in S_line_E:
            vj = 0
            for line in column.coveredRows:
                if line in U:
                    vj += 1
            alpha.append(vj)
        
        beta = [S_line_E[i].cost / aj if aj > 0 else float('inf') for i, aj in enumerate(alpha)]
        
        minBeta = min(beta)
        
        assert minBeta < float('inf')
        
        K = [S_line_E[i] for i, b in enumerate(beta) if b == minBeta]
        
        if(isBestImprovement):
            bestColumn = K[0]
            for column in K:
                if len(column.coveredRows) > len(bestColumn.coveredRows):
                    bestColumn = column
            newColumn = bestColumn
        else:
            newColumn = K[0]
        
        for row in newColumn.coveredRows:
            if solutionCoveredRows[row - 1] == 0:
                U.remove(row)
            solutionCoveredRows[row - 1] += 1
        
        S.append(newColumn)
        S_line.remove(newColumn)
    
    for column in reversed(S):
        if all(solutionCoveredRows[i - 1] > 1 for i in column.coveredRows):
            S.remove(column)
            S_line.append(column)
            for line in column.coveredRows:
                solutionCoveredRows[line - 1] -= 1
    
    return S


# Function to run multiple local search instances and change the number of iterations
def runLocalSearchAlgorithm(columns, numRows, numColumns, iterations, isBestImprovement = True):
    
    bestSolutionFound = construction1(columns, numRows, numColumns)
    
    numIterations = math.ceil(math.sqrt(int(iterations)))

    counter = 0
    
    start = timer()
    for _ in range(numIterations):
        solution = construction1(columns, numRows, numColumns)
        for _ in range(numIterations):
            aux = localSearchAlgorithm(columns, solution, numRows, isBestImprovement)
            if calcTotalCost(aux) < calcTotalCost(solution):
                solution = aux.copy()
        if calcTotalCost(solution) < calcTotalCost(bestSolutionFound):
            bestSolutionFound = solution.copy()
            counter += 1
            print(f"{counter} Melhoria(s) encontradas: {calcTotalCost(bestSolutionFound)}")
    end = timer()
    print(f"Execution time: {end - start} seconds")
    
    return bestSolutionFound

def main():

    option = input("Do you want to execute: \n \
        1 - Local search algorithm for all files (Best Improvement)\n \
        2 - Greedy algorithms for all files\n \
        3 - Local search algorithm for a specific file (Best Improvement)\n \
        4 - Greedy algorithms for a specific file\n \
        5 - local Search algorithm for all files (First improvement)\n \
            Option (index of the option): ")
    print("\n")
    
    if option == '1':
        numIterations = input("Insert the number of iterations to be made (10.000 is a recommended\n \
          value for a good execution time and final answer): ")
        print("Running tests...")
        for file in ["Teste_01.dat", "Teste_02.dat", "Teste_03.dat", "Teste_04.dat", "Wren_01.dat", "Wren_02.dat", "Wren_03.dat", "Wren_04.dat"]:
            print("File Analysed -> ", file)
            
            columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData(file)
            columns = createColumns(columnAndCost, linesThatCoverColumn)
            
            bestSolutionFound = runLocalSearchAlgorithm(columns, numRows, numColumns, numIterations, True)

            print("Best Solution Found on Local Search Algorithm on " + file + ": ")
            displayResult(bestSolutionFound)

            print("\n")
    
    elif option == '2':
        print("Running tests...")
        for file in ["Teste_01.dat", "Teste_02.dat", "Teste_03.dat", "Teste_04.dat", "Wren_01.dat", "Wren_02.dat", "Wren_03.dat", "Wren_04.dat"]:
            print("File Analysed -> ", file)
            
            columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData(file)
            columns = createColumns(columnAndCost, linesThatCoverColumn)
            
            greedySolution1 = construction1(columns, numRows, numColumns)
            
            greedySolution2 = construction2(columns, numRows)
            
            start = timer()
            print("Greedy Solution 1: ")
            displayResult(greedySolution1)
            end = timer()
            print(f"Execution Time: {end - start} seconds.")
            
            start = timer()
            print("Greedy Solution 2: ")
            displayResult(greedySolution2)
            end = timer()
            print(f"Execution Time: {end - start} seconds.")
            
            print("\n")
            
    elif option == '3':
        fileName = input("Input the file name to be read: ")
        columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData(fileName)
        columns = createColumns(columnAndCost, linesThatCoverColumn)
        
        greedySolution1 = construction1(columns, numRows, numColumns)
        
        greedySolution2 = construction2(columns, numRows)
        
        print("Greedy algorithm solutions")
        
        print("File Analysed ", fileName)
        print("Greedy Solution 1: ")
        displayResult(greedySolution1)
        
        print("Greedy Solution 2: ")
        displayResult(greedySolution2)

        numIterations = input("Insert the number of iterations to be made (10.000 is a recommended\n \
          value for a good execution time and final answer): ")

        bestSolutionFound = runLocalSearchAlgorithm(columns, numRows, numColumns, numIterations, True)

        print("Local Search Algorithm Solution: ")
        
        displayResult(bestSolutionFound)


    elif option == '4':
        fileName = input("Input the file name to be read: ")
        columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData(fileName)
        columns = createColumns(columnAndCost, linesThatCoverColumn)
        
        greedySolution1 = construction1(columns, numRows, numColumns)
        
        greedySolution2 = construction2(columns, numRows)
        
        print("Greedy algorithm solutions")
        
        print("File Analysed ", fileName)
        print("Greedy Solution 1: ")
        displayResult(greedySolution1)
        
        print("Greedy Solution 2: ")
        displayResult(greedySolution2)
    
    elif option == '5':
        numIterations = input("Insert the number of iterations to be made (10.000 is a recommended\n \
          value for a good execution time and final answer): ")
        print("Running tests...")
        for file in ["Teste_01.dat", "Teste_02.dat", "Teste_03.dat", "Teste_04.dat", "Wren_01.dat", "Wren_02.dat", "Wren_03.dat", "Wren_04.dat"]:
            print("File Analysed -> ", file)
            
            columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData(file)
            columns = createColumns(columnAndCost, linesThatCoverColumn)
            
            greedySolution1 = construction1(columns, numRows, numColumns)

            print("Local Search Algorithm Solution: ")
            
            solution = runLocalSearchAlgorithm(columns, numRows, numColumns, numIterations, False)
            
            displayResult(solution)
            
            print("\n")
    
    else:
        print("Invalid option.")
        exit(1)

if __name__ == "__main__":
    main()
