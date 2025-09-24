import copy, time
from random import randint
import tkinter as tk
from tkinter import messagebox, ttk
from sudoku_functions import is_puzzle_valid, is_consistent
from functions2 import is_puzzle_valid2, is_consistent2, find_empty_cell
from time_puzzle import Watch
from generator import _gen, _gen2
from tkinter.font import Font
gBtn = [tk.Button]

def selectValue(val, self):
    global inputVal, gBtn
    inputVal = val

class Board_config(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self,bg="white")
        container.pack(side="top",fill = "both",expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container,self)
            self.frames[F] = frame
            frame.grid_configure(row=0, column=0, sticky="nsew")
        self.switch_frame(StartPage)
    def switch_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg="white")
        self.python_image = tk.PhotoImage(file='C:/Users/Diana/PycharmProjects/Proiect Sudoku2/background3.gif')
        ttk.Label(self,image=self.python_image).pack()
        tk.Button(self,text='About sudoku',bg="#fdddfe",fg="black",font=("Helvetica 14 bold"),command=self._about).place(x=170, y=200)
        tk.Button(self,text='Play 4x4 sudoku',bg="#fdddfe",fg="black",font=("Helvetica 14 bold"),command=lambda:controller.switch_frame(PageOne)).place(x=60, y=300)
        tk.Button(self,text='Play 9x9 sudoku',bg="#fdddfe",fg="black",font=("Helvetica 14 bold"),command=lambda:controller.switch_frame(PageTwo)).place(x=280, y=300)
    def _about(self):
     messagebox.showinfo("About Sudoku",
        "Sudoku is one of the most popular puzzle games of all time. Sudoku is a game based on the logical placement of numbers."
        "It doesn't require any calculation or special math skills; all it takes is brains and concentration!! \n""\n"
        "How to play?  \n" "\n"
        "Sudoku is played on a 9x9 grid, divided into 3x3 squares separated by thicker lines."
        "The purpose of the game is to fill each cell with a number from 1 to 9, making sure that there are no repeated digits in any column or row in the grid, nor in the square itself.\n" "\n"
        "The game starts with the grid partially filled and the player has to find the remaining numbers according to the position of the already given ones. The difficulty of the puzzle ( EASY, MEDIUM, HARD ) varies according to the number of cells filled at the beginning of each game.\n""\n"
        "The rules of 4x4 Sudoku puzzles for kids are the same as for traditional Sudoku (9x9) grids. Only the number of cells and digits that must be placed are different.\n",)

class PageOne(tk.Frame):
    visual_running= False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self, bg="white")
        self.controller=controller
        self.display(), self._bindings()
        tk.Button(self,text="Back to Start Page",highlightthickness=0,height=1,bg="#fdddfe",font=("Helvetica 12 bold"),command=lambda:controller.switch_frame(StartPage)).place(x=30, y=30)
        tk.Button(self,text="Instructions",highlightthickness=0,height=1,bg="#fdddfe",font=("Helvetica 12 bold"),command=self.instructions).place(x=200, y=30)
        tk.Label(self,text="Time:",font=("Arial Bold",17),bg="white").place(x=555, y=40)
        self.grid_clicked_color = "#cbd6e2"
        self.grid_affected_color = "#fdddfe"
        self.grid_unaffected_color = "#e2ebf3"
        self.generated_color = "#EBB8DD"
        self.grid_clicked = None
        self.buttons_can_be_clicked = True
        self.generated_list = []
        self.difficulty = "KIDS"
        self.puzzle = [[0 for i in range(4)] for j in range(4)]
        self.grid = [[None for _ in range(4)] for _ in range(4)]
        Buttons_frame = tk.Frame(self,bg="pink",height=275,width=275)
        Buttons_frame.place(x=555, y=150)
        global gBtn
        btn = [tk.Button] * 5
        for i in range(1, 5):
            btn[i] = tk.Button(Buttons_frame,text=i,bg="#fdddfe",fg="black",font=("Helvetica 14 bold"),highlightthickness=0,bd=2,pady=25,padx=30)
            button_number = i
            if 0 < button_number <= 2:
                btn[i].grid(row=0, column=i - 1)
            elif 2 < button_number <= 4:
                btn[i].grid(row=1, column=i - 3)
        btn[1].configure(command=lambda: resetColor(btn[1], 1))
        btn[1].bind("<Button-1>", self.btn_click1)
        btn[2].configure(command=lambda: resetColor(btn[2], 2))
        btn[2].bind("<Button-1>", self.btn_click2)
        btn[3].configure(command=lambda: resetColor(btn[3], 3))
        btn[3].bind("<Button-1>", self.btn_click3)
        btn[4].configure(command=lambda: resetColor(btn[4], 4))
        btn[4].bind("<Button-1>", self.btn_click4)
        def changeBg(self, val):
            self.configure(bg="#e2ebf3",fg="black")
            selectValue(val, self)
        def resetColor(self, val):
            for i in range(1, 5):
                btn[i].configure(bg="#fdddfe",fg="black")
            changeBg(self, val)
        Board_frame = tk.Canvas(self,bg="#eeeeee")
        self.hv15 = Font(family="Helvetica",size=51)
        self.grid = []
        for i in range(4):
            row = []
            for j in range(4):
                color = "#EBB8DD"
                e = tk.Entry(Board_frame,width=2,justify='center',bd=1,font=self.hv15,bg=color)
                Board_frame.create_line(0,163,330,163,fill="black",width=3)
                Board_frame.create_line(0,328,330,328,fill="black",width=3)
                Board_frame.create_line(163,0,163,331,fill="black",width=3)
                Board_frame.create_line(328,0,328,330,fill="black",width=3)
                Board_frame.place(x=70,y=90,width=332,height=331)
                e.grid(row=i, column=j,padx=1, pady=1)
                e.bind("<Button-1>", self._grid_clicked)
                row.append(e)
            self.grid.append(row)
        self.margin = 40
        self.box_w = 50
        self.box_space = 2
        self.box_w_plus_space = self.box_w + self.box_space
        self.extra_space = 4
        self.btn_top_margin = 25
        self.btn_height = 50
        self.btn_width = 100
        self.btn_space = 40
        common_right_margin = 20
        common_top_margin = 50
        rBtns_left_margin = self.margin+9*(self.box_w_plus_space)+common_right_margin
        clearBtn = tk.Button(self,text='CLEAR ALL',font=("Arial Bold", 12),command=self.clear_button_action)
        clearBtn.place(x=rBtns_left_margin + 27,y=common_top_margin + 42,width=self.btn_width, height=self.btn_height)
        checkBtn = tk.Button(self, text='CHECK', font=("Arial Bold", 12), command=self.checkBtn_action)
        checkBtn.place(x=rBtns_left_margin + 137,y=common_top_margin + 42,width=self.btn_width, height=self.btn_height)
        self.demoBtn = tk.Button(self, text='VISUALIZE', font=("Arial Bold", 12),command=self.visualize_backtracking_soln)
        self.demoBtn.config(state=tk.DISABLED)
        self.demoBtn.place(x=rBtns_left_margin + 245,y=common_top_margin + 40,width=self.btn_width, height=self.btn_height)
        self.new_gameBtn = tk.Button(self, text='NEW GAME',font=("Arial Bold",14),bg="#fdddfe",command=lambda: self.generate(self.difficulty))
        self.new_gameBtn.place(x=rBtns_left_margin + 200,y=common_top_margin + 380,width=self.btn_width + 50, height=self.btn_height + 30)
        l2 = tk.Label(self,text="Select mode game:",font=("Arial Bold", 12),bg="white")
        l2.place(x=rBtns_left_margin + 20,y=common_top_margin + 380,width=self.btn_width + 50, height=self.btn_height + 2)
        self.difficulty_button = tk.Menubutton(self,text="Difficulty",relief=tk.RAISED,bg="#fdddfe",fg="black",font=("Arial Bold",13))
        self.difficulty_button.place(x=rBtns_left_margin + 20, y=common_top_margin + 420)
        self.difficulty_menu = tk.Menu(self.difficulty_button, tearoff=0)
        self.difficulty_menu.add_command(label="KIDS", command=lambda:self._toggle_difficulty("KIDS"))
        self.difficulty_button["menu"] = self.difficulty_menu

    def instructions(self):
        win = tk.Toplevel(app)
        win.title("Instructiuni")
        win.geometry('470x320')
        win.configure(bg="white")
        win.geometry("+%d+%d" % (x + 550, y + 150))
        win.wm_transient(app)
        tk.Label(win,text="Instructions",fg="black",bg="white",font=("Helvetica",24)).pack(side="top")
        text = "1. Choose the game difficulty from the menu and click on\n the NEW GAME button to start the game."
        tk.Label(win,text=text,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=60)
        text1 = "2.Select an empty square."
        tk.Label(win,text=text1, fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=130)
        self.img1 = tk.PhotoImage(file="C:/Users/Diana/PycharmProjects/Proiect Sudoku2/img1.gif")
        tk.Label(win, image=self.img1).place(x=200, y=110)
        text2 = "3.Select a number to fill the square."
        tk.Label(win,text=text2,fg="black",bg="white", font=("Helvetica",12)).place(x=10, y=170)
        self.img2 = tk.PhotoImage(file="C:/Users/Diana/PycharmProjects/Proiect Sudoku2/img2.gif")
        tk.Label(win, image=self.img2).place(x=290,y=140)
        text4 = "4.The CLEAR ALL completely clears the Sudoku board."
        tk.Label(win,text=text4,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=200)
        text5 = "5.The VISUALIZE button displays the sudoku puzzle using\nthe Backtracking algorithm. "
        tk.Label(win,text=text5,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=230)

    def display(self):
        display_watch = Watch(self)
        display_watch.place(x=630, y=40)
        display_watch.Stop()

    def _grid_clicked(self, event):
        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]
        self.grid_clicked = event.widget
        self._unhighlight(row, col)
        for i in range(4):
            self.grid[row][i].config(bg=self.grid_affected_color)
            self.grid[i][col].config(bg=self.grid_affected_color)
        for i in range(2):
            for j in range(2):
                self.grid[(row // 2) * 2 + i][(col // 2) * 2 + j].config(bg=self.grid_affected_color)
        event.widget.bind("<FocusOut>",lambda event: self._unhighlight(row, col)
            if event.widget.get() == ""
            else event.widget.config(bg=self.grid_unaffected_color))
        event.widget.config(bg=self.grid_clicked_color)

    def _unhighlight(self, row, col):
        for i in range(4):
            for j in range(4):
                self.grid[i][j].config(bg=self.grid_unaffected_color)
        self.grid_clicked.config(bg=self.grid_unaffected_color)
        for i in range(4):
            self.grid[row][i].config(bg=self.grid_unaffected_color)
            self.grid[i][col].config(bg=self.grid_unaffected_color)
        for i in range(2):
            for j in range(2):
                self.grid[(row // 2) * 2 + i][(col // 2) * 2 + j].config(bg=self.grid_unaffected_color)

    def clear_button_action(self):
        for i in range(4):
            for j in range(4):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].config(bg="#EBB8DD")

    def checkBtn_action(self):
        matrix = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                try:
                    matrix[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        find = find_empty_cell(matrix)
        if not find:
            if is_puzzle_valid2(matrix):
                messagebox.showinfo("Information","You have completed the game.")
            else:
                messagebox.showinfo("Information","Game is not over yet. There is at least one mistake!")
        else:
            messagebox.showinfo("Information","Game is not over yet. You should complete all the square.")

    def btn_click1(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 1)
    def btn_click2(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 2)
    def btn_click3(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 3)
    def btn_click4(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 4)
    def _clickable_buttons(self):
        self.buttons_can_be_clicked = True
        self.new_gameBtn.config(state=tk.NORMAL)
    def _unclickable_buttons(self):
        self.buttons_can_be_clicked = False
        self.new_gameBtn.config(state=tk.DISABLED)
        self.demoBtn.config(state=tk.NORMAL)
    def _bindings(self):
        self.controller.bind("k",lambda event:self._toggle_difficulty("KIDS")
            if self.buttons_can_be_clicked else None,)
    def _toggle_buttons(self):
        if self.buttons_can_be_clicked:
            self._unclickable_buttons()
        else:
            self._clickable_buttons()
    def _toggle_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_button.config(text="Difficulty: " + difficulty)

    def generate(self, difficulty):
        self._toggle_buttons()
        board = _gen2()
        self.solution = copy.deepcopy(board)
        for i in range(4):
            for j in range(4):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(0, board[i][j])
        if difficulty == "KIDS":
            for i in range(4):
                for j in range(4):
                    if randint(0, 2) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(fg="#32a1fd")
                        self.generated_list.append((i, j))
        display_watch = Watch(self)
        display_watch.place(x=630, y=40)
        display_watch.Start()
        self._toggle_buttons()

    def messageGood(self):
        win2 = tk.Toplevel(app)
        win2.title("Congratulations!")
        win2.geometry('300x200')
        win2.configure(bg="white")
        win2.geometry("+%d+%d" % (x + 900, y + 180))
        textgood="Sudoku puzzle is solved!\nThis is the first solution.\n \nQuestion!"
        txtquestion="Do you want to display more\n solutions to this puzzle if they exist?\n"
        tk.Label(win2,text=textgood,fg="black",bg="white",font=("Helvetica",11)).place(x=20,y=20)
        tk.Label(win2,text=txtquestion,fg="black",bg="white",font=("Helvetica",11)).place(x=20,y=100)
        tk.Button(win2,text="YES",fg="black",bg="#fdddfe",font=("Helvetica", 11),command=lambda:[win2.destroy(),self.choice('yes')]).place(x=60, y=150)
        tk.Button(win2,text="NO",fg="black",bg="#fdddfe",font=("Helvetica", 11),command=lambda:win2.destroy()).place(x=120, y=150)
        win2.wm_transient(app)

    def choice(self, option):
        if option == 'yes':
          win3 = tk.Toplevel(app)
          win3.geometry('300x150')
          win3.configure(bg="white")
          win3.geometry("+%d+%d" % (x + 900, y + 180))
          tk.Label(win3, text="This is the second solution.\n Do you want another solution?",fg="black",bg="white",font=("Helvetica",11)).place(x=20, y=20)
          tk.Button(win3,text="YES",fg="black",bg="#fdddfe",font=("Helvetica",11),command=lambda:[win3.destroy(),self.mesNosol()]).place(x=60, y=100)
          tk.Button(win3,text="NO",fg="black",bg="#fdddfe",font=("Helvetica",11),command=lambda:win3.destroy()).place(x=120, y=100)
          if is_puzzle_valid2(self.solution):
            if self.backtrack(self.solution):
                for i in range(4):
                    for j in range(4):
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].insert(0, self.solution[i][j])
          display_watch = Watch(self)
          display_watch.place(x=630, y=40)
          display_watch.Stop()
          win3.wm_transient(app)

    def mesNosol(self):
        win4 = tk.Toplevel(app)
        win4.geometry('250x100')
        win4.configure(bg="white")
        win4.geometry("+%d+%d" % (x + 900, y + 180))
        tk.Label(win4,text="There is no other solution.",fg="black",bg="white",font=("Helvetica",11)).place(x=20,y=20)
        win4.wm_transient(app)

    def backtrack(self, puzzle):
        find = find_empty_cell(puzzle)
        if not find:
            return True
        else:
            row,col = find
        for i in range(1, 5):
            if is_consistent2(puzzle,i,(row, col)):
                puzzle[row][col] = i
                if self.backtrack(puzzle):
                    return True
                puzzle[row][col] = 0
        return False

    def visualize_backtracking_soln(self):
        puzzle = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                try:
                    puzzle[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        if is_puzzle_valid2(puzzle):
            if self.backtrack(puzzle):
                for i in range(4):
                    for j in range(4):
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].insert(0, puzzle[i][j])
            self.messageGood()
        display_watch = Watch(self)
        display_watch.place(x=630, y=40)
        display_watch.Stop()

class PageTwo(tk.Frame):
    visual_running= False
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.configure(self,bg="white")
        self.controller = controller
        self._bindings(), self.display()
        tk.Button(self, text="Back to Start Page",highlightthickness=0,height=1,bg="#fdddfe", font=("Helvetica 12 bold"),command=lambda: controller.switch_frame(StartPage)).place(x=30, y=30)
        tk.Button(self,text="Instructions",highlightthickness=0,height=1,bg="#fdddfe",font=("Helvetica 12 bold"), command=self.instructions).place(x=200, y=30)
        tk.Label(self,text="Time:",font=("Arial Bold",17),bg="white").place(x=555, y=40)
        self.grid_clicked_color = "#cbd6e2"
        self.grid_affected_color = "#fdddfe"
        self.grid_unaffected_color = "#e2ebf3"
        self.generated_color = "#EBB8DD"
        self.grid_clicked = None
        self.buttons_can_be_clicked = True
        self.generated_list = []
        self.difficulty = "EASY"
        self.puzzle = [[0 for i in range(9)] for j in range(9)]
        self.grid = [[None for _ in range(9)] for _ in range(9)]
        Buttons_frame = tk.Frame(self, bg="pink", height=275, width=275)
        Buttons_frame.place(x=555, y=150)
        global gBtn
        btn = [tk.Button] * 10
        for i in range(1, 10):
            btn[i] = tk.Button(Buttons_frame,text=i,bg="#fdddfe",fg="black",font=("Helvetica 14 bold"),
                               highlightthickness=0,bd=2,pady=25,padx=30)
            button_number = i
            if 0 < button_number <= 3:
                btn[i].grid(row=0, column=i - 1)
            elif 3 < button_number <= 6:
                btn[i].grid(row=1, column=i - 4)
            elif 6 < button_number <= 9:
                btn[i].grid(row=2, column=i - 7)
        btn[1].configure(command=lambda: resetColor(btn[1], 1))
        btn[1].bind("<Button-1>", self.btn_click1)
        btn[2].configure(command=lambda: resetColor(btn[2], 2))
        btn[2].bind("<Button-1>", self.btn_click2)
        btn[3].configure(command=lambda: resetColor(btn[3], 3))
        btn[3].bind("<Button-1>", self.btn_click3)
        btn[4].configure(command=lambda: resetColor(btn[4], 4))
        btn[4].bind("<Button-1>", self.btn_click4)
        btn[5].configure(command=lambda: resetColor(btn[5], 5))
        btn[5].bind("<Button-1>", self.btn_click5)
        btn[6].configure(command=lambda: resetColor(btn[6], 6))
        btn[6].bind("<Button-1>", self.btn_click6)
        btn[7].configure(command=lambda: resetColor(btn[7], 7))
        btn[7].bind("<Button-1>", self.btn_click7)
        btn[8].configure(command=lambda: resetColor(btn[8], 8))
        btn[8].bind("<Button-1>", self.btn_click8)
        btn[9].configure(command=lambda: resetColor(btn[9], 9))
        btn[9].bind("<Button-1>", self.btn_click9)
        def changeBg(self, val):
            self.configure(bg="#e2ebf3",fg="black")
            selectValue(val, self)
        def resetColor(self, val):
            for i in range(1, 10):
                btn[i].configure(bg="#fdddfe",fg="black")
            changeBg(self, val)
        Board_frame = tk.Canvas(self,bg="#eeeeee")
        self.hv15 = Font(family="Helvetica",size=31)
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                if ((i // 3) + (j // 3)) % 2 == 0:
                    color = "#EBB8DD"
                else:
                    color = "#CBD6E2"
                Board_frame.create_line(0,159,470,159,fill="black",width=3)
                Board_frame.create_line(0,318,470,318,fill="black",width=3)
                Board_frame.create_line(156,0,156,475,fill="black",width=3)
                Board_frame.create_line(312,0,312,475,fill="black",width=3)
                Board_frame.pack()
                e = tk.Entry(Board_frame,width=2,justify='center',bd=1,font=self.hv15,bg=color)
                Board_frame.place(x=30,y=70,width=470,height=480)
                e.grid(row=i, column=j,padx=1,pady=1)
                e.bind("<Button-1>",self._grid_clicked)
                row.append(e)
            self.grid.append(row)
        self.margin = 40
        self.box_w = 50
        self.box_space = 2
        self.box_w_plus_space = self.box_w+self.box_space
        self.extra_space = 4
        self.btn_top_margin = 25
        self.btn_height = 50
        self.btn_width = 100
        self.btn_space = 40
        common_right_margin = 20
        common_top_margin = 50
        rBtns_left_margin = self.margin+9*(self.box_w_plus_space)+common_right_margin
        clearBtn = tk.Button(self,text='CLEAR ALL',font=("Arial Bold",12),command=self.clear_button_action)
        clearBtn.place(x=rBtns_left_margin + 27,y=common_top_margin + 42,width=self.btn_width,height=self.btn_height)
        checkBtn = tk.Button(self,text='CHECK',font=("Arial Bold",12),command=self.checkBtn_action)
        checkBtn.place(x=rBtns_left_margin + 137,y=common_top_margin + 42,width=self.btn_width, height=self.btn_height)
        self.demoBtn = tk.Button(self,text='VISUALIZE',font=("Arial Bold",12),command=self.visualize_backtracking_soln)
        self.demoBtn.config(state=tk.DISABLED)
        self.demoBtn.place(x=rBtns_left_margin + 245,y=common_top_margin + 40,width=self.btn_width,height=self.btn_height)
        self.new_gameBtn = tk.Button(self,text='NEW GAME',font=("Arial Bold",14),bg="#fdddfe",command=lambda: self.generate(self.difficulty))
        self.new_gameBtn.place(x=rBtns_left_margin+200,y=common_top_margin+380,width=self.btn_width + 50,height=self.btn_height + 30)
        l2 = tk.Label(self,text="Select mode game:",font=("Arial Bold",12),bg="white")
        l2.place(x=rBtns_left_margin + 20,y=common_top_margin + 380,width=self.btn_width + 50,height=self.btn_height + 2)
        self.difficulty_button = tk.Menubutton(self,text="Difficulty",relief=tk.RAISED,bg="#fdddfe",fg="black",font=("Arial Bold",13))
        self.difficulty_button.place(x=rBtns_left_margin + 20, y=common_top_margin + 420)
        self.difficulty_menu = tk.Menu(self.difficulty_button,tearoff=0)
        self.difficulty_menu.add_command(label="EASY",command=lambda:self._toggle_difficulty("EASY"))
        self.difficulty_menu.add_command(label="MEDIUM",command=lambda:self._toggle_difficulty("MEDIUM"))
        self.difficulty_menu.add_command(label="HARD",command=lambda:self._toggle_difficulty("HARD"))
        self.difficulty_button["menu"] = self.difficulty_menu

    def instructions(self):
        win = tk.Toplevel(app)
        win.title("Instructions")
        win.geometry('470x320')
        win.configure(bg="white")
        win.geometry("+%d+%d" % (x+550,y+150))
        win.wm_transient(app)
        tk.Label(win,text="Instructions",fg="black",bg="white",font=("Helvetica",24)).pack(side="top")
        text = "1.Choose the game difficulty from the menu and click on\n the NEW GAME button to start the game."
        tk.Label(win,text=text,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=60)
        text1 = "2.Select an empty square."
        tk.Label(win,text=text1,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=130)
        self.img1 = tk.PhotoImage(file="C:/Users/Diana/PycharmProjects/Proiect Sudoku2/img1.gif")
        tk.Label(win,image=self.img1).place(x=200, y=110)
        text2 = "3.Select a number to fill the square."
        tk.Label(win, text=text2,fg="black",bg="white",font=("Helvetica", 12)).place(x=10, y=170)
        self.img2 = tk.PhotoImage(file="C:/Users/Diana/PycharmProjects/Proiect Sudoku2/img2.gif")
        tk.Label(win, image=self.img2).place(x=290, y=140)
        text4 = "4.The CLEAR ALL completely clears the Sudoku board."
        tk.Label(win, text=text4,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=200)
        text5 = "5.The VISUALIZE button displays the sudoku puzzle using\nthe Backtracking algorithm. "
        tk.Label(win, text=text5,fg="black",bg="white",font=("Helvetica",12)).place(x=10, y=230)

    def display(self):
        display_watch = Watch(self)
        display_watch.place(x=630,y=40)
        display_watch.Stop()

    def _grid_clicked(self, event):
        row = event.widget.grid_info()["row"]
        col = event.widget.grid_info()["column"]
        self.grid_clicked = event.widget
        self._unhighlight(row, col)
        for i in range(9):
            self.grid[row][i].config(bg=self.grid_affected_color)
            self.grid[i][col].config(bg=self.grid_affected_color)
        for i in range(3):
            for j in range(3):
                self.grid[(row // 3) * 3 + i][(col // 3) * 3 + j].config(bg=self.grid_affected_color)
        event.widget.bind("<FocusOut>",lambda event: self._unhighlight(row, col)
            if event.widget.get() == ""
            else event.widget.config(bg=self.grid_unaffected_color),)
        event.widget.config(bg=self.grid_clicked_color)

    def _unhighlight(self, row, col):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].config(bg=self.grid_unaffected_color)
        self.grid_clicked.config(bg=self.grid_unaffected_color)
        for i in range(9):
            self.grid[row][i].config(bg=self.grid_unaffected_color)
            self.grid[i][col].config(bg=self.grid_unaffected_color)
        for i in range(3):
            for j in range(3):
                self.grid[(row // 3) * 3 + i][(col // 3) * 3 + j].config(bg=self.grid_unaffected_color)

    def clear_button_action(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)

    def checkBtn_action(self):
        matrix = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                try:
                    matrix[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        find = find_empty_cell(matrix)
        if not find:
            if is_puzzle_valid(matrix):
                messagebox.showinfo("Information","You have completed the game.")
            else:
                messagebox.showinfo("Information","Game is not over yet. There is at least one mistake!")
        else:
            messagebox.showinfo("Information","Game is not over yet. You should complete all the square.")

    def btn_click1(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 1)

    def btn_click2(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 2)
    def btn_click3(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 3)
    def btn_click4(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 4)
    def btn_click5(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 5)
    def btn_click6(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 6)
    def btn_click7(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 7)
    def btn_click8(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 8)
    def btn_click9(self, event):
        event.widget["text"]
        self.grid_clicked == event.widget
        self.grid_clicked.insert(0, 9)
    def _clickable_buttons(self):
        self.buttons_can_be_clicked = True
        self.new_gameBtn.config(state=tk.NORMAL)
    def _unclickable_buttons(self):
        self.buttons_can_be_clicked = False
        self.new_gameBtn.config(state=tk.DISABLED)
        self.demoBtn.config(state=tk.NORMAL)
    def _bindings(self):
        self.controller.bind("e",lambda event:self._toggle_difficulty("EASY")
            if self.buttons_can_be_clicked
            else None,)
        self.controller.bind("m",lambda event:self._toggle_difficulty("MEDIUM")
            if self.buttons_can_be_clicked
            else None,)
        self.controller.bind("h",lambda event:self._toggle_difficulty("HARD")
            if self.buttons_can_be_clicked
            else None,)
    def _toggle_buttons(self):
        if self.buttons_can_be_clicked:
            self._unclickable_buttons()
        else:self._clickable_buttons()
    def _toggle_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_button.config(text="Difficulty: " + difficulty)
    def generate(self, difficulty):
        self._toggle_buttons()
        board = _gen()
        self.solution=copy.deepcopy(board)
        for i in range(9):
            for j in range(9):
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(0, board[i][j])
        if difficulty == "EASY":
            for i in range(9):
                for j in range(9):
                    if randint(0, 1) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(fg="#32a1fd")
                        self.generated_list.append((i, j))
        elif difficulty == "MEDIUM":
            for i in range(9):
                for j in range(9):
                    if randint(0, 3) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(fg="#32a1fd")
                        self.generated_list.append((i, j))
        elif difficulty == "HARD":
            for i in range(9):
                for j in range(9):
                    if randint(0, 5) != 1:
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].config(fg="#32a1fd")
                        self.generated_list.append((i, j))
        display_watch = Watch(self)
        display_watch.place(x=630, y=40)
        display_watch.Start()
        self._toggle_buttons()
    def messageGood(self):
        win2 = tk.Toplevel(app)
        win2.title("Congratulations!")
        win2.geometry('300x200')
        win2.configure(bg="white")
        win2.geometry("+%d+%d" % (x+900,y+180))
        textgood="Sudoku puzzle is solved!\nThis is the first solution.\n \nQuestion!"
        txtquestion="Do you want to display more\n solutions to this puzzle if they exist?\n"
        tk.Label(win2,text=textgood,fg="black",bg="white",font=("Helvetica",11)).place(x=20, y=20)
        tk.Label(win2,text=txtquestion,fg="black",bg="white",font=("Helvetica",11)).place(x=20, y=100)
        tk.Button(win2,text="YES",fg="black",bg="#fdddfe",font=("Helvetica",11),command=lambda:[win2.destroy(), self.choice('yes')]).place(x=60,y=150)
        tk.Button(win2,text="NO",fg="black",bg="#fdddfe",font=("Helvetica",11),command=lambda:win2.destroy()).place(x=120,y=150)
        win2.wm_transient(app)
    def choice(self, option):
        if option == 'yes':
            win3 = tk.Toplevel(app)
            win3.geometry('300x150')
            win3.configure(bg="white")
            win3.geometry("+%d+%d" % (x+900,y+180))
            tk.Label(win3,text="This is the second solution.\n Do you want another solution?",fg="black",bg="white",font=("Helvetica",11)).place(x=20,y=20)
            tk.Button(win3,text="YES",fg="black",bg="#fdddfe",font=("Helvetica",11),command=lambda:[win3.destroy(),self.mesNosol()]).place(x=60,y=100)
            tk.Button(win3,text="NO",fg="black",bg="#fdddfe",font=("Helvetica",11),command=lambda:win3.destroy()).place(x=120,y=100)
            if is_puzzle_valid(self.solution):
                if self.backtrack(self.solution):
                    for i in range(9):
                        for j in range(9):
                            self.grid[i][j].delete(0, tk.END)
                            self.grid[i][j].insert(0, self.solution[i][j])
            win3.wm_transient(app)
    def mesNosol(self):
        win4 = tk.Toplevel(app)
        win4.geometry('250x100')
        win4.configure(bg="white")
        win4.geometry("+%d+%d" % (x+900,y+180))
        tk.Label(win4,text="There is no other solution.",fg="black",bg="white",font=("Helvetica",11)).place(x=20,y=20)
        win4.wm_transient(app)
    def backtrack(self, puzzle):
        find = find_empty_cell(puzzle)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if is_consistent(puzzle,i,(row,col)):
                puzzle[row][col] = i
                if self.backtrack(puzzle):
                    return True
                puzzle[row][col] = 0
        return False
    def visualize_backtracking_soln(self):
        puzzle = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                try:
                    puzzle[i][j] = int(self.grid[i][j].get())
                except ValueError:
                    pass
        if is_puzzle_valid(puzzle):
            if self.backtrack(puzzle):
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j].delete(0, tk.END)
                        self.grid[i][j].insert(0, puzzle[i][j])
            self.messageGood()
        display_watch = Watch(self)
        display_watch.place(x=630, y=40)
        display_watch.Stop()

if __name__== "__main__":
    app= Board_config()
    app.title('Game Sudoku')
    app.geometry('900x600+350+50')
    app.configure(bg="white")
    x = app.winfo_x()
    y = app.winfo_y()
    try:
        app.iconbitmap("sudoku.ico")
    except:
        pass
    app.mainloop()