def findEmpty(x):
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i][j] == 0:
                return (i, j)  # row, col
    return None

def valid(x, num, pos):
    # row check
    for i in range(len(x[0])):
        if x[pos[0]][i] == num and pos[1] != i:
            return False
    # col check
    for i in range(len(x)):
        if x[i][pos[1]] == num and pos[0] != i:
            return False
    # box check
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if x[i][j] == num and (i,j) != pos:
                return False
    return True


def solve(x):
    find = findEmpty(x)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1,10):
        if valid(x, i, (row, col)):
            x[row][col] = i
            if solve(x):
                return True
            x[row][col] = 0
    return False

def board(x):
    for i in range(len(x)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(len(x[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(x[i][j])
            else:
                print(str(x[i][j]) + " ", end="")
