import math, random

class Cell:
    def __init__(self,y,x,Tx,Ty):
        if Tx == x and Ty == y:
            self.distance = 0 
        else:
            self.distance = int(round(math.hypot(x-Tx,y-Ty)))

def printMatrix(m):
    for i in range(len(m)):
        tmp = ""
        for j in range(len(m[0])):
            tmp += f'{m[i][j].distance} '
        print(tmp)

def main():
    Tx = random.choice(range(10))
    Ty = random.choice(range(10))
    #print(f'Posizione tesoro: {Tx} {Ty}')
    ocean = [[Cell(i,j,Tx,Ty) for i in range(10)] for j in range(10)]

    attempts = 0
    while True:
        print("Scegli una cella")
        x = int(input("x: "))
        y = int(input("y: "))
        attempts += 1
        if ocean[x][y].distance == 0:
            print(f"Hai vinto! Numero di tentativi: {attempts}")
            printMatrix(ocean)
            break
        else:
            print(f"Distanza dal tesoro: {ocean[x][y].distance}")


if __name__ == '__main__':
    main()