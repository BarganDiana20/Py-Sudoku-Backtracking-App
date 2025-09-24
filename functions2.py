def find_empty_cell(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 0:
                return (row, col)
    return None
def is_consistent2(puzzle,num,pos):
     for i in range(len(puzzle[0])):
        if puzzle[pos[0]][i] == num and pos[1] != i:
               return False
     for i in range(len(puzzle)):
        if puzzle[i][pos[1]] == num and pos[0] != i:
                return False
     box_x = pos[1] // 2
     box_y = pos[0] // 2
     for i in range(box_y * 2, box_y * 2 + 2):
        for j in range(box_x * 2, box_x * 2 + 2):
            if puzzle[i][j] == num and (i, j) != pos:
                return False
     return True
def is_puzzle_valid2(puzzle):
    for row in puzzle:
        if not is_valid_unit(row):
            return False
    for col in zip(*puzzle):
        if not is_valid_unit(col):
            return False
    for i in (0, 2):
        for j in (0, 2):
            unit = [puzzle[x][y] for x in range(i,i+2) for y in range(j,j+2)]
            if not is_valid_unit(unit):
                    return False
        return True
    return True
def is_valid_unit( unit):
    unit = [i for i in unit if i != 0]
    return len(unit) == len(set(unit))

