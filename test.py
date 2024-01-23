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
    return cj / math.log2(kj)

def costFunction4(cj, kj):
    return cj / (kj * math.log2(kj))

def costFunction5(cj, kj):
    return cj / (kj * math.log(kj))

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
    totalCost = sum(column.cost for column in solution)
    print("Primary Cover:", [selectedColumn.index for selectedColumn in solution])
    print("Total Cost:", totalCost)

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

            costFunction = 4

            if kj == 0:
                columns[j].costFunctionValue = float('inf')
                continue
            else:
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

def localSearchAlgorithm(columns, initialSolution, numRows):
    # Parameters
    S = initialSolution.copy()
    S_line = [column for column in columns if column not in initialSolution]
    N_S = len(S)  # N(S)= o número de colunas no conjunto S
    Q_S = max(column.cost for column in S)
    p1 = random.uniform(0.3, 0.7)
    p2 = random.uniform(1.1, 2)
    D = math.ceil(N_S * p1)
    E = int(math.ceil(Q_S * p2))

    # number of columns that cover each row in S
    wi = [0] * numRows
    for column in S:
        for row in column.coveredRows:
            wi[row - 1] += 1

    # Step 2
    d = 0
    while d < D and S:  # Check if S is not empty
        randomColumn = S[random.randint(0, len(S) - 1)]
        S.remove(randomColumn)
        S_line.append(randomColumn)

        for line in randomColumn.coveredRows:
            wi[line - 1] -= 1

        d += 1
        
    print("S before step 3:", [column.index for column in S])

    # Step 3
    while True:
        U = [index + 1 for index, value in enumerate(wi) if value == 0]  # U= Conjunto das linhas descobertas
        if not U:
            break

        # Step 4
        # Correct calculation of S_line_E
        S_line_E = [column for column in S_line if column.cost <= E]
        
        if not S_line_E:
            continue

        # Correct calculation of vij and bj
        vij = [(column, sum([1 for line in column.coveredRows if line in U])) for column in S_line_E if any(line in U for line in column.coveredRows)]
        bj = [(column, column.cost / vi) for column, vi in vij if vi != 0]
        
        if not bj:
            continue

        bmin = min(bj, key=lambda x: x[1])
        K = [column for column, vi in vij if vi != 0 and abs(column.cost / vi - bmin[1]) < 1e-9]

        # Step 5
        if K:
            randomK = random.choice(K)
            S.append(randomK)
            S_line.remove(randomK)
            for line in randomK.coveredRows:
                wi[line - 1] += 1

    print("S before step 6:", [column.index for column in S])
    
    # Step 6
    for column in reversed(S):
        if all(wi[row - 1] > 1 for row in column.coveredRows):
            for row in column.coveredRows:
                wi[row - 1] -= 1
            S.remove(column)
            S_line.append(column)


    return S


def main():
    # fileName = input("Input the file name to be read: ")
    columnAndCost, linesThatCoverColumn, numRows, numColumns = getFileData("test1.txt")

    columns = createColumns(columnAndCost, linesThatCoverColumn)
    
    greedySolution = greedyAlgorithm(columns, numRows, numColumns)

    displayResult(greedySolution)
    
    #localSearchSolution = localSearchAlgorithm(columns, greedySolution, numRows)
    
    #displayResult(localSearchSolution)

if __name__ == "__main__":
    main()
