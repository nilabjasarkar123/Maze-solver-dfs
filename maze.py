from cell import Cell
import  time, random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if(seed):
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visted()
      
    def _create_cells(self):
        for i in range(self._num_cols):
            col_cell = []
            for j in range(self._num_rows):
                col_cell.append(Cell(self._win))
            self._cells.append(col_cell)
        
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    '''
    def _create_cells(self):
        for i in range(self._num_rows):
            row_cell = []
            for j in range(self._num_cols):
                row_cell.append(Cell(self._win))
            self._cells.append(row_cell)
        
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)

    '''
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i*self._cell_size_x
        y1 = self._y1 + j*self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return 
        
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)
    
    # BFS
    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            new_list = []
            possible_direction = 0

            # visit left
            if i > 0 and not self._cells[i-1][j].visited:
                new_list.append((i-1, j))
                possible_direction += 1

            # visit right 
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                new_list.append((i+1, j))
                possible_direction += 1

            #visit up
            if j > 0 and not self._cells[i][j-1].visited:
                new_list.append((i, j-1))
                possible_direction += 1
            
            #visit down 
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                new_list.append((i, j+1))
                possible_direction += 1
            
            if possible_direction == 0:
                self._draw_cell(i, j)
                return
            
            # pick a random direction
            direction = random.randrange(possible_direction)
            new_index = new_list[direction]

            # delete right wall
            if new_index[0] == i+1:
                self._cells[i][j].has_right_wall = False
                self._cells[i+1][j].has_left_wall = False

            # delete left wall
            if new_index[0] == i-1:
                self._cells[i][j].has_left_wall = False
                self._cells[i-1][j].has_right_wall = False
            
            # delete bottom wall
            if new_index[1] == j+1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j+1].has_top_wall = False

            # delete up wall
            if new_index[1] == j-1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j-1].has_bottom_wall = False
            
            

            #recursivly visit next
            self._break_walls_r(new_index[0], new_index[1])
        
    def _reset_cells_visted(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
    

    # solve the maze
    def _solve_maze(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        if(i == self._num_cols-1 and j == self._num_rows-1):
            return True

        # move left if no wall and never been visited
        if(i > 0 and not self._cells[i][j].has_left_wall and not self._cells[i-1][j].visited):
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if(self._solve_maze(i-1, j)):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i-1][j], True)
        
        # move right
        if(i < self._num_cols-1 and not self._cells[i][j].has_right_wall and not self._cells[i+1][j].visited):
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if(self._solve_maze(i+1, j)):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i+1][j], True)

        # move up
        if(j > 0 and not self._cells[i][j].has_top_wall and not self._cells[i][j-1].visited):
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if(self._solve_maze(i, j-1)):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j-1], True)
        
        # move down
        if j < self._num_cols-1 and not self._cells[i][j].has_bottom_wall and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if(self._solve_maze(i, j+1)):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j+1], True)
        
        return False


    def solve(self):
        return self._solve_maze(0,0)
