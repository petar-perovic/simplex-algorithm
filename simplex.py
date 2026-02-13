import tkinter as tk
from tkinter import messagebox
import numpy as np
from fractions import Fraction


class SimplexGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simplex Algoritam")

        self.font_label = ("Arial", 14)
        self.font_table = ("Arial", 14)

        self.window_width = 900
        self.window_height = 600
        self.center_window(self.window_width, self.window_height)

        self.n_var = tk.IntVar()
        self.n_con = tk.IntVar()

        self.entries_A = []
        self.entries_b = []
        self.entries_c = []

        self.iterations = []
        self.current_iter = 0

        self.build_start()
        self.root.mainloop()

    # =================================
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    # =================================
    def build_start(self):
        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor="center") 

        tk.Label(frame, text="Broj promjenljivih (x)", font=self.font_label).grid(row=0, column=0, pady=5)
        tk.Entry(frame, textvariable=self.n_var, width=5, font=self.font_label).grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Broj ogranicenja", font=self.font_label).grid(row=1, column=0, pady=5)
        tk.Entry(frame, textvariable=self.n_con, width=5, font=self.font_label).grid(row=1, column=1, pady=5)

        tk.Button(frame, text="OK", command=self.build_input, font=self.font_label, padx=10, pady=5)\
            .grid(row=2, columnspan=2, pady=10)

    # ==================================
    def build_input(self):
        n = self.n_var.get()
        m = self.n_con.get()

        if n <= 0 or m <= 0:
            messagebox.showerror("Error", "Neispravan unos")
            return

        for w in self.root.winfo_children():
            w.destroy()

        frame = tk.Frame(self.root)
        frame.place(relx=0.5, rely=0.5, anchor="center") 

        tk.Label(frame, text="Max Z =", font=self.font_label).grid(row=0, column=0, pady=5)

        self.entries_c = []
        for j in range(n):
            e = tk.Entry(frame, width=5, font=self.font_label)
            e.grid(row=0, column=j+1, pady=5)
            self.entries_c.append(e)
            tk.Label(frame, text=f"x{j+1}", font=self.font_label).grid(row=1, column=j+1, pady=5)

        tk.Label(frame, text="Ogranicenja", font=self.font_label).grid(row=2, column=0, pady=5)

        self.entries_A = []
        self.entries_b = []

        for i in range(m):
            row = []
            for j in range(n):
                e = tk.Entry(frame, width=5, font=self.font_label)
                e.grid(row=3+i, column=j+1, pady=3)
                row.append(e)
            self.entries_A.append(row)

            eb = tk.Entry(frame, width=5, font=self.font_label)
            eb.grid(row=3+i, column=n+2, pady=3)
            self.entries_b.append(eb)

            tk.Label(frame, text="<=", font=self.font_label).grid(row=3+i, column=n+1, pady=3)

        tk.Button(frame, text="Pocni", command=self.start_simplex, font=self.font_label, padx=10, pady=5)\
            .grid(row=3+m, columnspan=n+3, pady=10)

    # ==================================
    def start_simplex(self):
        try:
            self.c = np.array([float(e.get()) for e in self.entries_c])
            self.A = np.array([[float(e.get()) for e in row] for row in self.entries_A])
            self.b = np.array([float(e.get()) for e in self.entries_b])
        except:
            messagebox.showerror("Error", "Neispravan unos")
            return

        self.n = self.n_var.get()
        self.m = self.n_con.get()
        self.var_names = [f"x{i+1}" for i in range(self.n)] + [f"s{i+1}" for i in range(self.m)]

        self.solve_simplex()
        self.build_visualizer()

    def snapshot(self, table, pivot_row=None, pivot_col=None):
        self.iterations.append({
            "table": table.copy(),
            "pivot_row": pivot_row,
            "pivot_col": pivot_col
        })

    def solve_simplex(self):
        m, n = self.A.shape
        I = np.eye(m)
        A_full = np.hstack((self.A, I))
        c_full = np.hstack((self.c, np.zeros(m)))

        B = np.array([n+i for i in range(m)])
        CB = np.zeros(m)
        xb = self.b.copy()
        table = np.hstack((B.reshape(-1,1), CB.reshape(-1,1), xb.reshape(-1,1), A_full))
        table = table.astype(float)

        self.iterations.clear()
        self.snapshot(table)

        while True:
            CB_vector = table[:,1]
            zj = np.sum((CB_vector.reshape(-1,1) * table[:,3:]), axis=0)
            cj_zj = c_full - zj

            if max(cj_zj) <= 0:
                self.snapshot(table)
                break

            k = np.argmax(cj_zj)
            ratios = [table[i,2]/table[i,3+k] if table[i,3+k]>0 else np.inf for i in range(m)]
            r = np.argmin(ratios)

            pivot_col = 3+k
            self.snapshot(table, r, pivot_col)

            table[r,2:] /= table[r,pivot_col]
            for i in range(m):
                if i != r:
                    table[i,2:] -= table[i,pivot_col] * table[r,2:]

            table[r,0] = k
            table[r,1] = c_full[k]

    # ================= vizualizacija =================
    def build_visualizer(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  

        self.info = tk.Label(self.root, text="", font=("Arial", 16))
        self.info.pack(pady=5)

        tk.Button(self.root, text="Sledeca iteracija", command=self.next_iteration,
                  font=("Arial", 14), padx=10, pady=5).pack(pady=5)

        self.draw_iteration()


    def draw_iteration(self):
        for w in self.frame.winfo_children():
            w.destroy()

        data = self.iterations[self.current_iter]
        table = data["table"]
        pr = data["pivot_row"]
        pc = data["pivot_col"]

        m, total_cols = table.shape
        n_cols = total_cols - 3

        headers = ["B", "CB"] + self.var_names + ["b", "odnos"]
        for j, h in enumerate(headers):
            tk.Label(self.frame, text=h, relief="solid", width=8, bg="#ddd", font=("Arial", 14, "bold"))\
                .grid(row=0, column=j)

        for i, row in enumerate(table):
            basic = self.var_names[int(row[0])]
            row_bg = "#f9f9f9" if i % 2 == 0 else "#e6f2ff"  
            tk.Label(self.frame, text=basic, relief="solid", width=8, font=("Arial", 14), bg=row_bg)\
                .grid(row=i+1, column=0)
            tk.Label(self.frame, text=int(row[1]), relief="solid", width=8, font=("Arial", 14), bg=row_bg)\
                .grid(row=i+1, column=1)

            for j in range(n_cols):
                bg = row_bg
                if pr == i and pc == j+3:
                    bg = "#ff6666"  
                elif pr == i:
                    bg = "#80c1ff"  
                elif pc == j+3:
                    bg = "#99ff99"  

                tk.Label(self.frame, text=Fraction(row[3+j]).limit_denominator(100),
                         relief="solid", width=8, font=("Arial", 14), bg=bg)\
                    .grid(row=i+1, column=2+j)

            tk.Label(self.frame, text=Fraction(row[2]).limit_denominator(100),
                     relief="solid", width=8, font=("Arial", 14), bg=row_bg)\
                .grid(row=i+1, column=2+n_cols)

            if pc is not None and row[pc] > 0:
                ratio_txt = Fraction(row[2]/row[pc]).limit_denominator(100)
            else:
                ratio_txt = "-"
            tk.Label(self.frame, text=ratio_txt, relief="solid", width=8, font=("Arial", 14), bg=row_bg)\
                .grid(row=i+1, column=3+n_cols)

        CB_vector = table[:,1]
        zj_row = [np.sum(CB_vector * table[:,3+i]) for i in range(n_cols)]
        cj_zj_row = [self.c[i]-zj_row[i] if i<len(self.c) else 0-zj_row[i] for i in range(n_cols)]

        base_row = m + 1
        tk.Label(self.frame, text="Zj", width=8, relief="solid", bg="#ffc", font=("Arial", 14, "bold"))\
            .grid(row=base_row, column=1)
        for j, val in enumerate(zj_row):
            tk.Label(self.frame, text=Fraction(val).limit_denominator(100), width=8,
                     relief="solid", bg="#ffc", font=("Arial", 14, "bold"))\
                .grid(row=base_row, column=2+j)

        tk.Label(self.frame, text="Cj-Zj", width=8, relief="solid", bg="#ffc", font=("Arial", 14, "bold"))\
            .grid(row=base_row+1, column=1)
        for j, val in enumerate(cj_zj_row):
            tk.Label(self.frame, text=Fraction(val).limit_denominator(100), width=8,
                     relief="solid", bg="#ffc", font=("Arial", 14, "bold"))\
                .grid(row=base_row+1, column=2+j)

        self.info.config(text=f"{self.current_iter}")

    
    def next_iteration(self):
        if self.current_iter < len(self.iterations) - 1:
            self.current_iter += 1
            self.draw_iteration()
        else:
            messagebox.showinfo("Kraj", "Dosli ste do optimalnog resenja")


if __name__ == "__main__":
    SimplexGUI()
