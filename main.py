########################################################################
#
# Pathfinding Algorithm Visualizer
# Using tkinter
# Muhammad Ishmamul Hoque
# Date
#
########################################################################
# References used:
#
# @Tech With Tim: Python A* Path Finding Tutorial
# https://www.youtube.com/watch?v=JtiK0DOeI4A&ab_channel=TechWithTim
#
# @Daria Vasileva: Pathfinding_Algorithm_Visualizer
# https://github.com/DariaSVasileva/Pathfinding_Algorithm_Visualizer_tkinter
#
# resource path : https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
#########################################################################
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from queue import PriorityQueue
from collections import deque
import random
import time
import sys
import os
from PIL import ImageTk, Image

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


s = 2
# initial window setting
H = 700
W = 1180
gd_h = 680
gd_w = 680
init_x = 100
init_y = 20
state = -1
ROW = int
COL = int
start_point = None
end_point = None
start = False
end = False
grid_exist = False
algos = ["BFS", "DFS", "Dijkstra's Algorithm", "A* Search Algorithm"]
blocks = ["Random Blocks", "Square maze", "Carved maze"]


class Spot:

    def __init__(self, app, row, col, width):
        self.width = width
        self.row = row
        self.col = col
        self.button = Button(app, command=self.click, bg='white', relief=RAISED)
        self.button.place(x=col * width, y=row * width, height=width, width=width, anchor='center')

        self.neighbors = []
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None
        self.barrier = False
        self.clicked = False
        self.visited = False
        self.to_visit = False

    def make_start(self):
        self.button.config(bg="#ffdf29")
        global start
        start = True
        self.clicked = True
        global start_point
        start_point = (self.row, self.col)

    def make_end(self):
        self.button.config(bg="#1ac439")
        global end
        end = True
        self.clicked = True
        global end_point
        end_point = (self.row, self.col)

    def make_barrier(self):
        self.button.config(bg="black")
        self.barrier = True
        self.clicked = True

    def make_border(self):
        self.button.config(bg='grey', activebackground='grey', relief=FLAT)
        self.barrier = True
        self.clicked = True

    def reset(self):
        self.button.config(bg="white")
        self.clicked = False
        self.barrier = False
        self.to_visit = False
        self.visited = False

    def make_path(self):
        self.button.config(bg="#7b27db")

    def make_open(self):
        self.button.config(bg="#f51111")

    def make_closed(self):
        self.button.config(bg="#38e8eb")

    def disable(self):
        self.button.config(state=DISABLED)

    def enable(self):
        self.button.config(state=NORMAL)

    def make_to_visit(self):
        self.button.config(bg="red")
        self.to_visit = True

    def click(self):
        global state
        global start
        global end
        global start_point
        global end_point
        if state == 0:
            if not self.clicked:
                if not start_point:
                    self.make_start()
                else:
                    messagebox.showwarning("WARNING", "Can not have multiple start points")
            else:
                if start_point == (self.row, self.col):
                    self.reset()
                    start = False
                    start_point = None
                else:
                    messagebox.showwarning("WARNING", "Node already occupied")

        elif state == 1:
            if not self.clicked:
                if not end_point:
                    self.make_end()
                else:
                    messagebox.showwarning("WARNING", "Can not have multiple end points")
            else:
                if end_point == (self.row, self.col):
                    self.reset()
                    end = False
                    end_point = None
                else:
                    messagebox.showwarning("WARNING", "Node already occupied")
        elif state == 2:
            if not self.clicked:
                self.make_barrier()
            else:
                if self.barrier:
                    self.reset()
                else:
                    messagebox.showwarning("WARNING", "Node already occupied")

    def update_neighbors(self):
        if self.row < ROW:
            if not li[self.row + 1][self.col].barrier:
                self.neighbors.append(li[self.row + 1][self.col])
            # if self.col>0 and not li[self.row + 1][self.col-1].barrier:
            #     self.neighbors.append(li[self.row + 1][self.col-1])
            # if self.col<29 and not li[self.row + 1][self.col+1].barrier:
            #      self.neighbors.append(li[self.row + 1][self.col+1])

        if self.row > 1:
            if not li[self.row - 1][self.col].barrier:
                self.neighbors.append(li[self.row - 1][self.col])
            # if self.col > 0 and not li[self.row - 1][self.col - 1].barrier:
            #     self.neighbors.append(li[self.row - 1][self.col - 1])
            # if self.col < 29 and not li[self.row - 1][self.col + 1].barrier:
            #     self.neighbors.append(li[self.row - 1][self.col+1])

        if self.col < ROW and not li[self.row][self.col + 1].barrier:
            self.neighbors.append(li[self.row][self.col + 1])

        if self.col > 1 and not li[self.row][self.col - 1].barrier:
            self.neighbors.append(li[self.row][self.col - 1])


def hst(x, y):
    return abs(x.row - y.row) + abs(x.col - y.col)


# A* search algorithm
def a_star_search():
    global steps
    count = 0
    start_node = li[start_point[0]][start_point[1]]
    finish = li[end_point[0]][end_point[1]]

    open_node = PriorityQueue()

    # add start_node in open_node with f_score = 0 and count as one item
    open_node.put((0, count, start_node))

    # put g_score for start to 0
    start_node.g = 0
    start_node.f = hst(start_node, finish)

    # create a dict to keep track of spots in open_set, can't check PriorityQueue
    start_node.visited = True

    # if open_node is empty - all possible nodes are considered, path doesn't exist
    while not open_node.empty():

        # popping the spot with lowest f_score from open_set
        # if score the same, then whatever was inserted first - PriorityQueue
        # popping [2] - spot itself
        current = open_node.get()[2]
        current.visited = False

        if current == finish:
            build_path(current)

            # draw end and start again
            finish.make_end()
            start_node.make_start()
            enable_board()
            return

        # if not end - consider all neighbors of current spot to choose next step
        for neighbor in current.neighbors:

            # calculate g_score for every neighbor
            temp_g_score = current.g + 1

            # if new path through this neighbor better
            if temp_g_score < neighbor.g:

                # update g_score for this spot and keep track of new best path
                neighbor.parent = current
                neighbor.g = temp_g_score
                neighbor.f = temp_g_score + hst(neighbor, finish)

                if not neighbor.visited:
                    # count the step
                    count += 1

                    # add neighbor in open_set for consideration
                    open_node.put((neighbor.f, count, neighbor))
                    neighbor.visited = True
                    neighbor.make_open()
                app.update_idletasks()
                time.sleep((0.25 - delay.get() / 200))

        if current != start_node:
            current.make_closed()
            steps += 1
    # didn't find path
    messagebox.showinfo("No Solution", "There was no solution")
    reset_result()
    enable_board()


# dijkstra's algorithm
def dijkstra():
    global steps
    global ROW
    z = (ROW + 2) ** 2
    for i in range(1, ROW + 1):
        for j in range(1, ROW + 1):
            li[i][j].g = z
    start_node = li[start_point[0]][start_point[1]]
    finish = li[end_point[0]][end_point[1]]

    open_node = deque()
    open_node.append(start_node)
    start_node.visited = True
    start_node.g = 0
    while len(open_node) > 0:
        curr = open_node.popleft()
        if curr == finish:
            build_path(curr)
            start_node.make_start()
            finish.make_end()
            return
        for neighbor in curr.neighbors:
            if curr.g + 1 < neighbor.g:
                neighbor.parent = curr
                open_node.append(neighbor)
                neighbor.g = curr.g + 1
                neighbor.make_open()
        if curr != start_node:
            curr.make_closed()
            steps += 1
        app.update_idletasks()
        time.sleep((0.25 - delay.get() / 200))
    # no path avialable
    messagebox.showinfo("", "No solution found")
    reset_result()
    enable_board()


# DFS Algorithm
def dfs():
    global steps
    start_node = li[start_point[0]][start_point[1]]
    finish = li[end_point[0]][end_point[1]]
    curr = start_node
    curr.visited = True
    while (1):
        if curr == finish:
            steps -= 1
            build_path(curr)
            start_node.make_start()
            finish.make_end()
            return
        if len(curr.neighbors) != 0:
            z = []
            for i in range(0, len(curr.neighbors)):
                if curr.neighbors[i] == finish:
                    r = curr.neighbors[0]
                    curr.neighbors[0] = curr.neighbors[i]
                    curr.neighbors[i] = r
                    break
                if curr.neighbors[i].visited == True:
                    z.append(curr.neighbors[i])
            for child in z:
                curr.neighbors.remove(child)
        if len(curr.neighbors) != 0:
            next_node = curr.neighbors[0]
            next_node.parent = curr
            if curr != start_node:
                curr.make_closed()
            next_node.make_open()
            app.update_idletasks()
            time.sleep((0.25 - delay.get() / 200))
            curr.neighbors.pop(0)

            curr.visited = True
            curr = next_node

            steps += 1
        else:
            if curr != start_node:
                curr.make_closed()
            curr = curr.parent
            curr.make_open()
            app.update_idletasks()
            time.sleep((0.25 - delay.get() / 200))
            steps += 1
            if curr == start_node:
                messagebox.showinfo("", "No solution found")
                reset_result()
                enable_board()
                return
        app.update_idletasks()
        time.sleep((0.25 - delay.get() / 200))


# BFS Algorithm
def bfs():
    global steps
    start_node = li[start_point[0]][start_point[1]]
    finish = li[end_point[0]][end_point[1]]
    open_node = deque()
    open_node.append(start_node)
    start_node.visited = True
    while len(open_node) > 0:
        curr = open_node.popleft()
        if curr == finish:
            build_path(curr)
            start_node.make_start()
            finish.make_end()
            return
        for neighbor in curr.neighbors:
            if not neighbor.visited:
                neighbor.parent = curr
                neighbor.visited = True
                open_node.append(neighbor)
                neighbor.make_open()
        if curr != start_node:
            curr.make_closed()
            steps += 1
        app.update_idletasks()
        time.sleep((0.25 - delay.get() / 200))
    # no path avialable
    messagebox.showinfo("", "No solution found")
    reset_result()
    enable_board()


def reset_result():
    global path
    global step
    global steps
    global s_dis
    s_dis = 0
    steps = 0
    step.configure(text='0')
    path.configure(text='0')


def update_result():
    global path
    global step
    global steps
    global s_dis
    # destination node
    steps += 1
    step.configure(text=str(steps))
    path.configure(text=str(s_dis))


def build_path(node):
    global s_dis
    start_node = li[start_point[0]][start_point[1]]
    curr = node
    while curr != start_node:
        # curr.update_neighbors()
        # if start_node in curr.neighbors:
        #     parent=start_node
        # else:
        #     parent = curr.parent
        parent = curr.parent
        parent.make_path()
        curr = parent
        s_dis += 1
        app.update_idletasks()
        time.sleep((0.25 - delay.get() / 200))
    update_result()
    enable_board()


def delet(li):
    for i in sub.winfo_children():
        i.destroy()
    for i in li:
        del i


def make_grid():
    show(1)
    global ROW
    ROW = row_value.get()
    global li
    li = []
    delet(li)
    for i in range(0, ROW + 2):
        s = []
        for j in range(0, ROW + 2):
            node = Spot(sub, i, j, gd_h // (ROW + 2))
            if i == ROW + 1 or i == 0 or j == 0 or j == ROW + 1:
                node.make_border()
            s.append(node)
        li.append(s)
    global grid_exist
    grid_exist = True


def set_geometry(app):
    app.geometry(f"{W}x{H}+{init_x}+{init_y}")


def srt():
    global state
    global button_start
    global button_barrier
    global button_end
    global button_search
    global button_maze
    global button_reset
    global grid_exist
    if not grid_exist:
        messagebox.showerror('', "Create a grid first")
        return
    if state == 0:
        button_start.configure(bg='black')
        state = -1
    else:
        state = 0
        button_start.configure(bg='white')
        button_barrier.configure(bg='black')
        button_end.configure(bg='black')
        button_search.configure(bg='black')


def end_():
    global state
    global button_start
    global button_barrier
    global button_end
    global button_search
    global grid_exist
    if not grid_exist:
        messagebox.showerror('', "Create a grid first")
        return
    if state == 1:
        button_end.configure(bg='black')
        state = -1
    else:
        state = 1
        button_start.configure(bg='black')
        button_barrier.configure(bg='black')
        button_end.configure(bg='white')
        button_search.configure(bg='black')


def barrier():
    global state
    global button_start
    global button_barrier
    global button_end
    global button_search
    global grid_exist
    if not grid_exist:
        messagebox.showerror('', "Create a grid first")
        return

    if state == 2:
        button_barrier.configure(bg='black')
        state = -1
    else:
        state = 2
        button_start.configure(bg='black')
        button_barrier.configure(bg='white')
        button_end.configure(bg='black')
        button_search.configure(bg='black')


def search():
    global state
    global button_start
    global button_barrier
    global button_end
    global button_search
    global button_maze
    global button_reset
    global start
    global end
    global li
    global s_dis
    global steps
    global row_scale
    global button_grid
    global option_block
    global grid_exist
    if not grid_exist:
        messagebox.showerror('', "Create a grid first")
        return
    if not start and not end:
        messagebox.showwarning("Missing", "START NODE and END NODE are missing")
    elif not start:
        messagebox.showwarning("Missing", "START NODE is missing")
    elif not end:
        messagebox.showwarning("Missing", "END NODE is missing")
    else:
        if state == 3:
            button_search.configure(bg='black')
            state = -1
        else:
            state = 3
            button_start.configure(bg='black', state=DISABLED)
            button_barrier.configure(bg='black', state=DISABLED)
            button_end.configure(bg='black', state=DISABLED)
            button_search.configure(bg='white', state=DISABLED)
            button_maze.configure(bg='black', state=DISABLED)
            button_reset.configure(bg='black', state=DISABLED)
            option.configure(state=DISABLED)
            slide_block.configure(state=DISABLED)
            slide_speed.configure(state=DISABLED)
            row_scale.configure(state=DISABLED)
            button_grid.configure(state=DISABLED)
            option_block.configure(state=DISABLED)
            steps = 0
            s_dis = 0
            for i in range(1, ROW + 1):
                for j in range(1, ROW + 1):
                    li[i][j].neighbors = []
                    li[i][j].g = float('inf')
                    li[i][j].h = 0
                    li[i][j].f = float('inf')
                    li[i][j].parent = None
                    li[i][j].visited = False
                    li[i][j].update_neighbors()
                    if not li[i][j].clicked:
                        li[i][j].reset()
                    li[i][j].disable()
            if algo.get() == algos[0]:
                bfs()
            elif algo.get() == algos[1]:
                dfs()
            elif algo.get() == algos[2]:
                dijkstra()
            elif algo.get() == algos[3]:
                a_star_search()


def enable_board():
    global state
    state = -1
    button_start.configure(bg='black', state=NORMAL)
    button_barrier.configure(bg='black', state=NORMAL)
    button_end.configure(bg='black', state=NORMAL)
    button_search.configure(bg='black', state=NORMAL)
    button_maze.configure(bg='black', state=NORMAL)
    button_reset.configure(bg='black', state=NORMAL)
    option.configure(state=NORMAL)
    slide_block.configure(state=NORMAL)
    slide_speed.configure(state=NORMAL)
    row_scale.configure(state=NORMAL)
    button_grid.configure(state=NORMAL)
    option_block.configure(state=NORMAL)
    for i in range(1, ROW + 1):
        for j in range(1, ROW + 1):
            li[i][j].enable()


def show(x):
    global state
    state = -1
    button_start.configure(bg='black')
    button_barrier.configure(bg='black')
    button_end.configure(bg='black')
    button_search.configure(bg='black')


def random_block(z):
    global ROW
    x = random.randint(1, ROW)
    y = random.randint(1, ROW)
    li[x][y].make_start()
    while (1):
        if not li[x][y].clicked:
            li[x][y].make_end()
            break
        else:
            x = random.randint(1, ROW)
            y = random.randint(1, ROW)

    for i in range(0, z - 2):
        x = random.randint(1, ROW)
        y = random.randint(1, ROW)
        while (1):
            if not li[x][y].clicked:
                li[x][y].make_barrier()
                break
            else:
                x = random.randint(1, ROW)
                y = random.randint(1, ROW)


def square():
    global ROW
    x = ROW
    if x % 2 == 0:
        for i in range(1, ROW + 1):
            for j in range(1, ROW + 1):
                if i == ROW or j == ROW:
                    li[i][j].make_barrier()
    else:
        x += 1
    li[1][1].make_end()
    for z in range(2, x // 2, 2):
        ring = []
        for i in range(z, x - z + 1):
            for j in range(z, x - z + 1):
                if i == j or i + j == (x):
                    continue
                if i == z or i == x - z or j == z or j == x - z:
                    li[i][j].make_barrier()
                    ring.append(li[i][j])
        for i in range(0, 2):
            a = random.choice(ring)
            a.reset()
    li[x // 2][x // 2].make_start()
    for i in range(0, ROW // 5):
        x = random.randint(1, ROW - 1)
        y = random.randint(1, ROW - 1)
        while (1):
            if not li[x][y].clicked:
                li[x][y].make_barrier()
                break
            else:
                x = random.randint(1, ROW - 1)
                y = random.randint(1, ROW - 1)


def make_carved_maze(x):
    first = li[1][1]
    curr = li[1][1]
    z = None
    while (1):
        curr.button.configure(bg='gold')
        app.update_idletasks()
        time.sleep((0.25 - delay.get() / 200))
        curr.reset()
        choice_li = []
        if curr.col < x - 1:
            if li[curr.row][curr.col + 2].to_visit:
                choice_li.append(li[curr.row][curr.col + 2])
        if curr.col > 2:
            if li[curr.row][curr.col - 2].to_visit:
                choice_li.append(li[curr.row][curr.col - 2])
        if curr.row > 2:
            if li[curr.row - 2][curr.col].to_visit:
                choice_li.append(li[curr.row - 2][curr.col])
        if curr.row < x - 1:
            if li[curr.row + 2][curr.col].to_visit:
                choice_li.append(li[curr.row + 2][curr.col])
        if len(choice_li) == 0:
            curr = curr.parent
            if curr == first:
                break
            else:
                continue
        else:
            z = random.choice(choice_li)
            z.parent = curr
            if z.row == curr.row + 2:
                li[curr.row + 1][curr.col].button.configure(bg='gold')
                app.update_idletasks()
                time.sleep((0.25 - delay.get() / 200))
                li[curr.row + 1][curr.col].reset()
            if z.row == curr.row - 2:
                li[curr.row - 1][curr.col].button.configure(bg='gold')
                app.update_idletasks()
                time.sleep((0.25 - delay.get() / 200))
                li[curr.row - 1][curr.col].reset()
            if z.col == curr.col + 2:
                li[curr.row][curr.col + 1].button.configure(bg='gold')
                app.update_idletasks()
                time.sleep((0.25 - delay.get() / 200))
                li[curr.row][curr.col + 1].reset()
            if z.col == curr.col - 2:
                li[curr.row][curr.col - 1].button.configure(bg='gold')
                app.update_idletasks()
                time.sleep((0.25 - delay.get() / 200))
                li[curr.row][curr.col - 1].reset()
            curr = z


def carved():
    global ROW
    x = ROW
    if x % 2 == 0:
        for i in range(1, ROW + 1):
            for j in range(1, ROW + 1):
                if i == ROW or j == ROW:
                    li[i][j].make_barrier()
    else:
        x += 1
    for i in range(1, x):
        for j in range(1, x):
            if i % 2 != 0 and j % 2 != 0:
                li[i][j].make_to_visit()
            else:
                li[i][j].make_barrier()
    make_carved_maze(x)
    li[1][1].make_start()
    li[x - 1][x - 1].make_end()
    app.update_idletasks()
    time.sleep((0.25 - delay.get() / 200))


def maze():
    global state
    global button_start
    global button_barrier
    global button_end
    global button_search
    global button_maze
    global button_reset
    global block
    global grid_exist
    if not grid_exist:
        messagebox.showerror('', "Create a grid first")
        return
    state = 4
    z = int((ROW * ROW) * (value.get() / 100))
    maze_type = block.get()
    reset_board()
    if maze_type == blocks[0]:
        random_block(z)
    elif maze_type == blocks[1]:
        square()
    elif maze_type == blocks[2]:
        carved()


def reset_board():
    global state
    global button_start
    global button_barrier
    global button_end
    global button_search
    global button_maze
    global button_reset
    global start
    global start_point
    global end
    global row_scale
    global button_grid
    global option_block
    global end_point
    global path
    global step
    global s_dis
    global steps
    global grid_exist
    if not grid_exist:
        messagebox.showerror('', "Create a grid first")
        return
    row_value.set(ROW)
    if state != 4:
        value.set(50)
        block.set(blocks[0])
        delay.set(50)
    reset_result()
    algo.set(algos[0])
    button_start.configure(bg='black')
    button_barrier.configure(bg='black')
    button_end.configure(bg='black')
    button_search.configure(bg='black')
    enable_board()
    for i in range(1, ROW + 1):
        for j in range(1, ROW + 1):
            li[i][j].reset()
            li[i][j].neighbors = []
            li[i][j].g = float('inf')
            li[i][j].h = 0
            li[i][j].f = float('inf')
            li[i][j].parent = None
            li[i][j].visited = False
            li[i][j].enable()
            li[i][j].barrier = False
    start = False
    end = False
    start_point = None
    end_point = None
    state = -1


def instructions():
    messagebox.showinfo("Instructions",
                        "Welcome everyone. Follow the instructions properly to get your desired path:\n\n"
                        "1. First select total rows.\n\n"
                        "2. To select your start node tap on the start node button and then press on any spot on the grid to make it the start node.\n\n"
                        "3. Follow similar process for end node and barrier nodes.\n\n"
                        "4. Or you could select a maze type and generate random mazes.\n\n"
                        "5. To reset a node you can press it again on the grid to reset it.\n\n"
                        "6. After deciding the start, end and barrier nodes you can select search algorithm. Dafault is Bfs methode.\n\n"
                        "7. Then select the search button to start the searching process\n\n"
                        "8. Using reset button you can reset the whole board\n\n"
                        "9. Hope you have a pleasant time with the app :)")


# main algorithm
if s == 2:
    app = Tk()
    app.geometry(f"{W}x{H}+{init_x}+{init_y}")
    app.resizable(False, False)
    app.title("PATH FINDING VISUALIZER")
    logo = PhotoImage(file=resource_path("logo.png"))
    app.iconphoto(True, logo)
    app.configure(background="black")
    sub = Frame(app, relief="flat", bg="black", padx=10, pady=10)
    sub.place(x=475, y=10, height=H, width=H)

    # User frame
    user = Frame(app, width=300, height=680, borderwidth=10, relief="sunken", bg="black", padx=5, pady=5)
    user.pack_propagate(True)
    user.pack(side='left')
    label_u = Label(user, text="USER TAB", font=('Arial', 25, 'bold'), bg="black", fg="#00FF00",
                    activebackground='black', activeforeground='#00FF00', padx=25, pady=8)
    label_u.grid(row=0, column=0, columnspan=3)

    button_ins = Button(user, text="?", font=('Arial', 12, 'bold'), bg="black", fg="#00FF00",
                         command=instructions, activebackground='black', activeforeground='#00FF00', relief=GROOVE, borderwidth=5)
    button_ins.place(x=400,y=5)

    # Grid & Maze genarate
    grid_frame = Frame(user, pady=10, padx=5, bg='black', relief="groove", borderwidth=5)
    grid_frame.grid(row=1, column=0)
    label_g = Label(grid_frame, text="Create Grid", font=('Arial', 16, 'bold'), bg="black", fg="#00FF00",
                    activebackground='black', activeforeground='#00FF00', padx=25, pady=0)
    label_g.grid(row=0, column=0, columnspan=2)
    trlabelg1 = Label(grid_frame, height=1, bg='black', state=DISABLED)
    trlabelg1.grid(row=1, column=0, columnspan=2)
    row_value = IntVar()
    row_value.set(50)
    row_scale = Scale(grid_frame, command=show, from_=10, to=80, length=100, variable=row_value,
                      bg="black",
                      fg="#00FF00", activebackground='black', orient="horizontal", )
    row_scale.grid(row=2, column=1)
    scale_name = Label(grid_frame, text="Rows : ", font=("Arial", 10, "bold"), bg='black', fg="#00FF00", pady=10)
    scale_name.grid(row=2, column=0)
    trlabelg2 = Label(grid_frame, height=1, bg='black', state=DISABLED)
    trlabelg2.grid(row=3, column=0, columnspan=2)
    button_grid = Button(grid_frame, text="Generate", font=('Arial', 10, 'bold'), bg="black", fg="#00FF00",
                         command=make_grid, activebackground='black', activeforeground='#00FF00', relief=GROOVE,
                         padx=10,
                         pady=5, borderwidth=5, height=1, width=20)
    button_grid.grid(row=4, column=0, columnspan=2)
    trlabelg3 = Label(grid_frame, height=1, bg='black', state=DISABLED)
    trlabelg3.grid(row=5, column=0, columnspan=2)

    label_m = Label(grid_frame, text="Create Blocks", font=('Arial', 16, 'bold'), bg="black", fg="#00FF00",
                    activebackground='black', activeforeground='#00FF00', padx=25, pady=4)
    label_m.grid(row=6, column=0, columnspan=2)

    # block type
    label_select_maze = Label(grid_frame, text="Select block type :", font=('Arial', 12, 'bold'), bg="black",
                              fg="#00FF00",
                              activebackground='black', activeforeground='#00FF00', pady=20)
    label_select_maze.grid(row=7, column=0, columnspan=2)
    block = StringVar()
    block.set(blocks[0])
    option_block = OptionMenu(grid_frame, block, *blocks)
    option_block.configure(font=('Arial', 10, 'bold'), bg="black", fg="#00FF00",
                           activebackground='black', activeforeground='#00FF00', borderwidth=5, relief="ridge",
                           width=20,
                           padx=5, pady=5, textvariable=block)
    option_block.grid(row=8, column=0, columnspan=2)
    trlabelb1 = Label(grid_frame, height=1, bg='black', state=DISABLED)
    trlabelb1.grid(row=9, column=0, columnspan=2)

    value = IntVar()
    value.set(50)
    slide_block = Scale(grid_frame, command=show, from_=20, to=60, length=100, variable=value,
                        bg="black",
                        fg="#00FF00", activebackground='black', orient="horizontal")
    slide_block.grid(row=10, column=1)
    slide_name = Label(grid_frame, text="Blocks (%) : ", font=("Arial", 10, "bold"), bg='black', fg="#00FF00")
    slide_name.grid(row=10, column=0)

    trlabelb2 = Label(grid_frame, height=1, bg='black', state=DISABLED)
    trlabelb2.grid(row=11, column=0, columnspan=2)

    button_maze = Button(grid_frame, text="Genarate MAZE", font=('Arial', 10, 'bold'), bg="black",
                         fg="#00FF00",
                         command=maze, activebackground='black', activeforeground='#00FF00', relief=GROOVE, padx=10,
                         pady=5, borderwidth=5, height=1, width=20)
    button_maze.grid(row=12, column=0, columnspan=2)

    # blank
    label_bl = Label(user, bg="black", state=DISABLED)
    label_bl.grid(row=1, column=1)
    # Visualization keys

    visual = Frame(user, pady=10, padx=5, bg='black', relief="groove", borderwidth=5)
    visual.grid(row=1, column=2)

    label_v = Label(visual, text="Visualization", font=('Arial', 16, 'bold'), bg="black", fg="#00FF00",
                    activebackground='black', activeforeground='#00FF00', padx=25, pady=0)
    label_v.grid(row=0, column=0, columnspan=2)
    trlabelv1 = Label(visual, height=1, bg='black', state=DISABLED)
    trlabelv1.grid(row=1, column=0, columnspan=2)

    # start button
    button_start = Button(visual, text="START NODE", font=('Arial', 10, 'bold'), bg="black", fg="#00FF00", command=srt,
                          activebackground='black', activeforeground='#00FF00', relief=GROOVE, padx=10, pady=5,
                          borderwidth=5, height=1, width=20)
    button_start.grid(row=2, column=0, columnspan=2)
    trlabelv2 = Label(visual, height=1, bg='black', state=DISABLED)
    trlabelv2.grid(row=3, column=0, columnspan=2)

    # end Button
    button_end = Button(visual, text="END NODE", font=('Arial', 10, 'bold'), bg="black", fg="#00FF00", command=end_,
                        activebackground='black', activeforeground='#00FF00', relief=GROOVE, padx=10, pady=5,
                        borderwidth=5, height=1, width=20)
    button_end.grid(row=4, column=0, columnspan=2)
    trlabelv3 = Label(visual, height=1, bg='black', state=DISABLED)
    trlabelv3.grid(row=5, column=0, columnspan=2)

    # Barrier
    button_barrier = Button(visual, text="ROAD BLOCK", font=('Arial', 10, 'bold'), bg="black", fg="#00FF00",
                            command=barrier,
                            activebackground='black', activeforeground='#00FF00', relief=GROOVE, padx=10, pady=5,
                            borderwidth=5, height=1, width=20)
    button_barrier.grid(row=6, column=0, columnspan=2)

    # Algorithm selection

    label_search = Label(visual, text="Select search algorithm :", font=('Arial', 12, 'bold'), bg="black", fg="#00FF00",
                         activebackground='black', activeforeground='#00FF00', pady=16)
    label_search.grid(row=7, column=0, columnspan=2)
    algo = StringVar()
    algo.set(algos[0])
    option = OptionMenu(visual, algo, *algos)
    option.configure(font=('Arial', 10, 'bold'), bg="black", fg="#00FF00",
                     activebackground='black', activeforeground='#00FF00', borderwidth=5, relief="ridge", width=20,
                     padx=5, pady=5, textvariable=algo)
    option.grid(row=8, column=0, columnspan=2)
    trlabelv4 = Label(visual, height=1, bg='black', state=DISABLED)
    trlabelv4.grid(row=9, column=0, columnspan=2)

    # speed management
    delay = IntVar()
    delay.set(50)
    slide_speed = Scale(visual, command=show, from_=1, to=50, length=100, variable=delay,
                        bg="black",
                        fg="#00FF00", activebackground='black', orient="horizontal")
    slide_speed.grid(row=10, column=1)
    slide_name1 = Label(visual, text="Speed :  ", font=("Arial", 10, "bold"), bg='black', fg="#00FF00")
    slide_name1.grid(row=10, column=0)
    trlabelv5 = Label(visual, height=1, bg='black', state=DISABLED)
    trlabelv5.grid(row=11, column=0, columnspan=2)

    # search button

    pic = Image.open("logo.png")
    resized = pic.resize((20, 20))
    rpic = ImageTk.PhotoImage(resized)
    button_search = Button(visual, text="Search", font=('Arial', 12, 'bold'), bg="black", fg="#00FF00", command=search,
                           activebackground='black', activeforeground='#00FF00', relief=GROOVE, padx=10, pady=5,
                           borderwidth=5, image=rpic, compound='left', width=160)
    button_search.grid(row=12, column=0, columnspan=2)

    # experiment results

    result = Frame(user, pady=10, padx=5, bg='black', relief=FLAT)
    result.grid(row=3, column=0, columnspan=3)

    label_r = Label(result, text="Experiment Results", font=('Arial', 16, 'bold'), bg="black", fg="#00FF00",
                    activebackground='black', activeforeground='#00FF00', padx=25, pady=5)
    label_r.grid(row=0, column=0, columnspan=2)

    # steps
    global steps
    steps = 0
    name_l = Label(result, text="Total steps : ", font=("Arial", 12, "bold"), bg='black', fg="#00FF00")
    name_l.grid(row=1, column=0, sticky='e')
    step = Label(result, text=str(steps), font=("Arial", 12, "bold"), bg='black', fg="#00FF00")
    step.grid(row=1, column=1, sticky='w')

    # run time
    global s_dis
    s_dis = 0
    name_t = Label(result, text="Path length : ", font=("Arial", 12, "bold"), bg='black', fg="#00FF00")
    name_t.grid(row=2, column=0, sticky='e')
    path = Label(result, text='0', font=("Arial", 12, "bold"), bg='black', fg="#00FF00")
    path.grid(row=2, column=1, sticky='w')

    button_reset = Button(result, text="RESET", font=('Arial', 10, 'bold'), bg="black", fg="#00FF00",
                          command=reset_board,
                          activebackground='black', activeforeground='#00FF00', relief=GROOVE, padx=10, pady=5,
                          borderwidth=5, height=1, width=20)
    button_reset.grid(row=5, column=0, columnspan=2)
    instructions()
    app.mainloop()
