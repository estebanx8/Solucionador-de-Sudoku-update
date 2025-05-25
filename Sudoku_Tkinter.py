#estas son las librerías que utilizaremos

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading

#aquí definimos los objetos

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Sudoku")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.frames = [[None for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.create_grid()
        self.create_buttons()
        self.status_label = tk.Label(self.root, text="COLOCA TU SUDOKU A RESOLVER!!!!", font=("Arial"))
        self.status_label.grid(row=9, column=0, columnspan=9, pady=5)
        # Barra de progreso
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=10, column=0, columnspan=9, pady=5)
        self.progress["maximum"] = 100  # Porcentaje
        self.progress_value = 0

    #procedemos a crear las celdas

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                # márgenes azules más oscuros cada 3 celdas
                top =5 if row % 3 == 0 else 2
                left =5 if col % 3 == 0 else 2
                bottom = 4 if row == 8 else 0
                right = 4 if col == 8 else 0
                frame = tk.Frame(
                    self.root,
                    highlightbackground="#003366",  # azul marino oscuro
                    highlightcolor="#003366",
                    highlightthickness=0,
                    bd=0
                )
                frame.grid(
                    row=row,
                    column=col,
                    padx=(left, right),
                    pady=(top, bottom)
                )

                entry = tk.Entry(frame, width=2, font=('Arial', 29), justify='center', bd=0)
                entry.pack()
                self.entries[row][col] = entry
                self.frames[row][col] = frame
                
    #aquí colocamos los botónes

    def create_buttons(self):
        solve_button = tk.Button(self.root, text="Resolver", command=self.solve_sudoku_thread)
        solve_button.grid(row=11, column=0, columnspan=9, sticky="we", pady=5)
        
        clear_button = tk.Button(self.root, text="Nuevo Sudoku", command=self.clear_grid)
        clear_button.grid(row=13, column=0, columnspan=9, sticky="we", pady=5)
        
        ejemplo_button = tk.Button(self.root, text="Ejemplo para resolver", command=self.load_example)
        ejemplo_button.grid(row=14, column=0, columnspan=9, sticky="we", pady=5)
        
    #aquí colocamos especificaciónes con respecto a los números colocados, las celdas
    #sí se coloca una letra o sea un 0 salga una ventana de error y si es más de 1 dijito también
    #colo el color al solucionar etc

    def get_grid(self):
        grid = []
        for row in range(9):
            current_row = []
            for col in range(9):
                val = self.entries[row][col].get().strip()
                if val == "":
                    num = 0
                elif val.isdigit():
                    if len(val) > 1:
                        messagebox.showerror("Error", f"Número de más de un dígito en la celda ({row+1},{col+1}). Solo se permite 1-9.")
                        return None
                    num = int(val)
                    if not (1 <= num <= 9):
                        messagebox.showerror("Error", f"Número fuera de rango en la celda ({row+1},{col+1}). Solo se permite 1-9.")
                        return None
                else:
                    messagebox.showerror("Error", f"Letra o carácter inválido en la celda ({row+1},{col+1}). Solo se permiten números del 1 al 9.")
                    return None
                current_row.append(num)
                self.original_grid[row][col] = num
            grid.append(current_row)
        return grid


    def set_grid(self, grid):
        for row in range(9):
            for col in range(9):
                self.entries[row][col].delete(0, tk.END)
                if grid[row][col] != 0:
                    self.entries[row][col].insert(0, str(grid[row][col]))
                    color = 'red' if self.original_grid[row][col] != 0 else 'green'
                    self.entries[row][col].config(fg=color)
                    
    #aquí colocamos las divisiones de los 3x3 y si es valido el número

    def is_valid(self, grid, row, col, num):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if grid[box_row_start + i][box_col_start + j] == num:
                    return False
        return True
    
    #aquí tenemos el procedimietno de resolucion de los sudokus
    #utilizando el back-traking

    def solve(self, grid, update_progress=None):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if update_progress:
                                update_progress(row * 9 + col + 1)
                            if self.solve(grid, update_progress):
                                return True
                            grid[row][col] = 0
                    return False
        return True
    
    #funcion para el botón de "resolver"

    def solve_sudoku(self):
        grid = self.get_grid()
        if grid is None:
            return  # Si hay error en la entrada, no intenta resolver
        if self.solve(grid):
            self.set_grid(grid)
            self.status_label.config(text="¡Sudoku resuelto!", fg="green")
        else:
            messagebox.showerror("Error", "No se pudo resolver el Sudoku. Verifica los datos ingresados.")
            self.status_label.config(text="No se pudo resolver el Sudoku.", fg="red")
        self.progress["value"] = 81

    # Hilo para no bloquear la interfaz
    def solve_sudoku_thread(self):
        grid = self.get_grid()
        if grid is None:
            return
        self.status_label.config(text="Resolviendo...", fg="orange")
        self.progress["value"] = 0
        self.progress_value = 0
        # Calcula las posiciones vacías para progreso real
        self.empty_cells = [(r, c) for r in range(9) for c in range(9) if grid[r][c] == 0]
        self.total_empty = len(self.empty_cells)
        threading.Thread(target=self.solve_sudoku, args=(grid,), daemon=True).start()

    def solve_sudoku(self, grid):
        solved = self.solve_with_progress(grid, 0)
        if solved:
            self.root.after(0, lambda: self.set_grid(grid))
            self.root.after(0, lambda: self.status_label.config(text="¡Sudoku resuelto!", fg="green"))
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo resolver el Sudoku. Verifica los datos ingresados."))
            self.root.after(0, lambda: self.status_label.config(text="No se pudo resolver el Sudoku.", fg="red"))
        self.root.after(0, lambda: self.progress.config(value=100))

    def solve_with_progress(self, grid, idx):
        if idx == self.total_empty:
            return True
        row, col = self.empty_cells[idx]
        for num in range(1, 10):
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                percent = int((idx + 1) * 100 / self.total_empty)
                self.root.after(0, lambda v=percent: self.progress.config(value=v))
                if self.solve_with_progress(grid, idx + 1):
                    return True
                grid[row][col] = 0
        return False
    
    #función para el botón de "Nuevo Sudoku"
            
    def clear_grid(self):
        for row in range(9):
            for col in range(9):
               self.entries[row][col].delete(0, tk.END)
               self.entries[row][col].config(fg='black')
               self.original_grid[row][col] = 0
        self.status_label.config(text="")  # Borra el mensaje de estado
        self.progress["value"] = 0

    #función para el botón de "ejemplo a resolver"
        
    def load_example(self):
         example_grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                        [6, 0, 0, 1, 9, 5, 0, 0, 0],
                        [0, 9, 8, 0, 0, 0, 0, 6, 0],
                        [8, 0, 0, 0, 6, 0, 0, 0, 3],
                        [4, 0, 0, 8, 0, 3, 0, 0, 1],
                        [7, 0, 0, 0, 2, 0, 0, 0, 6],
                        [0, 6, 0, 0, 0, 0, 2, 8, 0],
                        [0, 0, 0, 4, 1, 9, 0, 0, 5],
                        [0, 0, 0, 0, 8, 0, 0, 7, 9]
         ]
         self.set_grid(example_grid)
         self.status_label.config(text="Ejemplo cargado", fg="blue")
         self.progress["value"] = 0
         
#iniciar aplicación

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverGUI(root)
    root.mainloop()
