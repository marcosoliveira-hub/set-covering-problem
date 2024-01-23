from copy import deepcopy
import random
import math

class Column:
    def __init__(self, index, cost, coveredRows):
        self.index: int = index
        self.cost: float = cost
        self.coveredRows: list[int] = coveredRows

def compareColumns(a, b):
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
    aux = globalCoveredRows.copy()
    for i in coveredRows:
        aux[i - 1] = 1

    return aux

def createColumns(columnAndCost, linesThatCoverColumn) -> list[Column]:
    columns = []
    for j in range(len(columnAndCost)):
        columns.append(Column(columnAndCost[j][0], columnAndCost[j][1], linesThatCoverColumn[j]))

    return columns

def getMaxCost(columns) -> float:
    maxCost = 0
    for column in columns:
        if column.cost > maxCost:
            maxCost = column.cost

    return maxCost

def displayResult(solution) -> None:
    totalCost = calcTotalCost(solution)
    print("Primary Cover:", [selectedColumn.index for selectedColumn in solution])
    print("Total Cost:", totalCost)

def calcTotalCost(solution) -> float:
    totalCost = 0
    for column in solution:
        totalCost += column.cost

    return totalCost

def greedyAlgorithm(columns, numRows, numColumns) -> list[Column]:
    solution = []
    kj = 0

    globalCoveredRows = [0] * numRows

    while globalCoveredRows.count(1) < numRows:
        for j in range(numColumns):
            alreadyCoveredRows = globalCoveredRows.count(1)
            aux = updateGlobalCoveredRows(globalCoveredRows, columns[j].coveredRows)
            newCoveredRows = aux.count(1)
            kj = newCoveredRows - alreadyCoveredRows

            costFunction = random.randint(1, 7)

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

    return solution

def getCoveredRows(columns, numRows) -> list[int]:
    coveredRows = [0] * numRows
    for column in columns:
        for row in column.coveredRows:
            coveredRows[row - 1] += 1

    return coveredRows

def localSearchAlgorithm(columns, initialSolution, numRows):
    S = initialSolution.copy()
    
    N_S = len(S)
    
    Q_S = max(column.cost for column in S)
    
    S_line = [column for column in columns if column not in initialSolution]
    
    p1 = random.uniform(0.05, 0.9)
    p2 = random.uniform(1.1, 2)
    
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
        
        alpha = [sum([1 for i in column.coveredRows if i in solutionCoveredRows]) for column in S_line_E]
        
        beta = [S_line_E[i].cost / aj if aj > 0 else float('inf') for i, aj in enumerate(alpha)]
        
        if len(beta) == 0:
            print("beta is empty")
            break
        
        minBeta = min(beta)
        
        assert minBeta < float('inf')
        
        K = [S_line_E[i] for i, b in enumerate(beta) if b == minBeta]
        
        newColumn = K[random.randint(0, len(K) - 1)]
        
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

def main():
    # fileName = input("Input the file name to be read: ")
    columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData("test1.txt")
    columns = createColumns(columnAndCost, linesThatCoverColumn)
    
    greedySolution = greedyAlgorithm(columns, numRows, numColumns)
    
    displayResult(greedySolution)
    
    solution = greedySolution.copy()
    
    for _ in range(20000):
        aux = localSearchAlgorithm(columns, solution, numRows)
        random.shuffle(aux)
        if calcTotalCost(aux) < calcTotalCost(solution):
            solution = deepcopy(aux)
            print(calcTotalCost(solution))
    
    displayResult(solution)

if __name__ == "__main__":
    main()


