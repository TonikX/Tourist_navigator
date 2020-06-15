import copy

import requests
from tsp_solver.greedy import solve_tsp


class FindRoute:
    def __init__(self, arrayCoord):
        self.arrayCoord = arrayCoord
        self.lenOfMatrix = len(arrayCoord)

    def create_edgeList(self):
        i = 0
        j = 0
        summ = 0
        status = 0
        edgeList = list()
        while i < (self.lenOfMatrix - 1):
            j = i + 1
            while j < (self.lenOfMatrix):
                body = {"coordinates": [self.arrayCoord[i], self.arrayCoord[j]]}
                headers = {
                    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                    'Authorization': '5b3ce3597851110001cf6248f6955b0cf5054da0885068280284b6a9',
                    'Content-Type': 'application/json; charset=utf-8'
                }

                call = requests.post('https://api.openrouteservice.org/v2/directions/foot-walking/json', json=body,
                                     headers=headers)

                if call.status_code == 200:
                    edgeList.append(dict({"from": self.arrayCoord[i], "to": self.arrayCoord[j],
                                          "distance": call.json()["routes"][0]["summary"]["distance"]}))
                else:
                    print("Сan't reach this point")
                    status = 1
                    j = self.lenOfMatrix
                    i = self.lenOfMatrix
                j += 1
            i += 1
        for count in range(len(edgeList)):
            summ += edgeList[count]['distance']
        summ = summ * summ
        return edgeList, summ, status

    def create_edgeMatrix(self, edgeList):
        startP = 0
        edgeMatrix = [[0] * (self.lenOfMatrix) for z in range(self.lenOfMatrix)]
        edgeListMatrix = copy.deepcopy(edgeMatrix)
        for i in range(self.lenOfMatrix):
            for j in range(self.lenOfMatrix):
                if (j == i):
                    edgeMatrix[i][j] = 0
                    edgeListMatrix[i][j] = 0
                elif (j > i):
                    edgeMatrix[i][j] = edgeList[startP]['distance']
                    edgeMatrix[j][i] = edgeList[startP]['distance']
                    edgeListMatrix[i][j] = edgeList[startP]
                    edgeListMatrix[j][i] = edgeList[startP]
                    startP += 1
        return edgeMatrix, edgeListMatrix

    def addPointsToMatrix(self, edgeMatrix, summ):
        additionalArr = [[0] * (self.lenOfMatrix + 2) for z in range(2)]
        for iter in range(2):
            for jiter in range(self.lenOfMatrix + 2):
                if (iter == 0):
                    if (jiter == self.lenOfMatrix):
                        additionalArr[iter][jiter] = 0
                    else:
                        additionalArr[iter][jiter] = int(summ)
                else:
                    if (jiter == 0) or (jiter == self.lenOfMatrix):
                        additionalArr[iter][jiter] = 0
                    elif (jiter == self.lenOfMatrix + 1):
                        additionalArr[iter][jiter] = 0

                    else:
                        additionalArr[iter][jiter] = int(summ)
        for i in range(self.lenOfMatrix):
            edgeMatrix[i].append(additionalArr[0][i])
            edgeMatrix[i].append(additionalArr[1][i])
        edgeMatrix.append(additionalArr[0])
        edgeMatrix.append(additionalArr[1])
        return edgeMatrix

    def solveTSP(self):
        edgeList, summ, status = self.create_edgeList()
        if (status == 0):
            edgeMatrix, edgeListMatrix = self.create_edgeMatrix(edgeList)
            edgeMatrix = self.addPointsToMatrix(edgeMatrix, summ)
            solve = solve_tsp(edgeMatrix)
            solve_len = len(solve)
            print(solve)
            solve.pop(solve_len - 1)
            solve.pop(solve_len - 2)
            solve_len = len(solve)
            solve.reverse()
            print(solve)
            routeList = []
            suma = 0
            for i in range(solve_len - 1):
                suma += edgeMatrix[solve[i]][solve[i + 1]]
                routeList.append(edgeListMatrix[solve[i]][solve[i + 1]])
            return routeList
        else:
            return status
