import time

def gotoxy(x,y):
    print ("%c[%d;%df" % (0x1B, y, x), end='')

class Cell:
    def __init__(self):
        self.num_of_neighbors_evengen = 0
        self.num_of_neighbors_oddgen = 0
        self.state_evengen = 0                  # active or not
        self.state_oddgen = 0

    def make_active(self):
        self.state_oddgen = 1



class Board:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.cells = [[0] * cols for i in range(rows)]
        for i in range(rows):
            for j in range(cols):
                self.cells[i][j] = Cell()


    def initialize_board(self, list_of_active_cells):
        for each_cell in list_of_active_cells:
            row, col = each_cell
            self.cells[row][col].make_active()
        self.update_all_neighbors(1)


    def update_its_neighbor_count(self, row, col, gen):
        num_neighbors = 0
        if gen % 2 == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < self.rows and 0 <= col + j < self.cols and not (i == 0 and j == 0):
                        if self.cells[row + i][col + j].state_evengen:
                            num_neighbors += 1
            self.cells[row][col].num_of_neighbors_oddgen = num_neighbors           

        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= row + i < self.rows and 0 <= col + j < self.cols and not (i == 0 and j == 0):
                        if self.cells[row + i][col + j].state_oddgen:
                            num_neighbors += 1
            self.cells[row][col].num_of_neighbors_evengen = num_neighbors


    def update_board(self, gen):
        if gen % 2 != 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    num_neighbors = self.cells[i][j].num_of_neighbors_oddgen
                    activity = self.cells[i][j].state_evengen                        # from previous generation
                    if activity:
                        if num_neighbors == 0 or num_neighbors == 1 or num_neighbors >= 4:
                            self.cells[i][j].state_oddgen = 0
                        else:
                            self.cells[i][j].state_oddgen = 1
                    else:
                        if num_neighbors == 3:
                            self.cells[i][j].state_oddgen = 1
                        else:
                            self.cells[i][j].state_oddgen = 0

        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    num_neighbors = self.cells[i][j].num_of_neighbors_evengen
                    activity = self.cells[i][j].state_oddgen
                    if activity:
                        if num_neighbors == 0 or num_neighbors == 1 or num_neighbors >= 4:
                            self.cells[i][j].state_evengen = 0
                        else:
                            self.cells[i][j].state_evengen = 1
                    else:
                        if num_neighbors == 3:
                            self.cells[i][j].state_evengen = 1
                        else:
                            self.cells[i][j].state_evengen = 0


    def next_move(self, gen):
        self.update_board(gen)
        self.update_all_neighbors(gen)


    def update_all_neighbors(self, gen):
        for i in range(self.rows):
            for j in range(self.cols):
                self.update_its_neighbor_count(i, j, gen)


    def print_board(self, gen):
        gotoxy(0,0)
        if gen % 2 == 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.cells[i][j].state_evengen:
                        print('O ', end='')
                    else:
                        print('. ', end='')
                print()
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.cells[i][j].state_oddgen:
                        print('O ', end='')
                    else:
                        print('. ', end='')
                print()

    
    def print_neighbor_matrix(self, gen):
        for i in range(self.rows):
            for j in range(self.cols):
                if gen % 2 != 0:
                    print(self.cells[i][j].num_of_neighbors_oddgen, end="")
                else:
                    print(self.cells[i][j].num_of_neighbors_evengen, end="")
            print()




board = Board(20,20)
activate_cells = [(8, 9), (9, 11), (10, 11), (11, 10), (10, 9), (10, 8), (8, 10), (8, 8), (7, 8), (4, 4), (4, 6), (5, 5), (6, 4), (6, 6)]
board.initialize_board(activate_cells)
board.print_board(1)
time.sleep(0.4)

for gen in range(2, 20):
    board.next_move(gen)
    print('\x1bc')                     # to clear screen
    board.print_board(gen)
    time.sleep(0.4)


