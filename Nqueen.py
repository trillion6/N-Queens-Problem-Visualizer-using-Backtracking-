import customtkinter as ctk
from tkinter import Canvas, messagebox

# ---------------- Technical N-Queens Visualizer with Step Counter ---------------- #

class NQueensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Problem Visualizer - Tech Edition")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Modern Tech Theme Setup
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Variables
        self.N = ctk.IntVar(value=8)
        self.delay_ms = ctk.IntVar(value=100)
        self.running = False
        self.solved = False
        self.positions = []
        self.row = 0
        self.next_col = 0
        self.step_count = 0

        # Build GUI
        self._build_ui()
        self._make_board()
        self.canvas.bind("<Configure>", self._resize_board)

    # ---------- UI Setup ---------- #
    def _build_ui(self):
        # Title
        title = ctk.CTkLabel(
            self.root,
            text="♛  N-Queens Problem Visualizer",
            font=("Consolas", 22, "bold"),
            text_color="#5ce1e6"
        )
        title.pack(pady=10)

        # Top Controls
        top = ctk.CTkFrame(self.root, fg_color="#0a0f1f", corner_radius=10)
        top.pack(side="top", fill="x", padx=20, pady=5)

        # Board Size Input
        ctk.CTkLabel(top, text="Board Size (N ≥ 4):", font=("Consolas", 12), text_color="#d8e2dc").grid(row=0, column=0, padx=10, pady=10)
        self.entry_n = ctk.CTkEntry(top, textvariable=self.N, width=60, justify="center", font=("Consolas", 12))
        self.entry_n.grid(row=0, column=1, padx=5)

        # Speed Control
        ctk.CTkLabel(top, text="Speed (ms):", font=("Consolas", 12), text_color="#d8e2dc").grid(row=0, column=2, padx=10)
        self.speed = ctk.CTkSlider(top, from_=0, to=600, variable=self.delay_ms, number_of_steps=60, progress_color="#5ce1e6")
        self.speed.grid(row=0, column=3, padx=5, pady=10)

        # Buttons
        self.btn_start = ctk.CTkButton(top, text="▶ Start", command=self.start, width=90,
                                       fg_color="#219ebc", hover_color="#1f7a8c",
                                       text_color="#ffffff", font=("Consolas", 12, "bold"))
        self.btn_start.grid(row=0, column=4, padx=8)

        self.btn_stop = ctk.CTkButton(top, text="⏸ Stop", command=self.stop, width=90,
                                      fg_color="#f77f00", hover_color="#f48c06",
                                      text_color="#ffffff", font=("Consolas", 12, "bold"),
                                      state="disabled")
        self.btn_stop.grid(row=0, column=5, padx=8)

        self.btn_reset = ctk.CTkButton(top, text="🔄 Reset", command=self.reset_board, width=90,
                                       fg_color="#495057", hover_color="#6c757d",
                                       text_color="#ffffff", font=("Consolas", 12, "bold"))
        self.btn_reset.grid(row=0, column=6, padx=8)

        # Canvas Area
        self.canvas_frame = ctk.CTkFrame(self.root, fg_color="#101f0a", corner_radius=10)
        self.canvas_frame.pack(expand=True, fill="both", padx=30, pady=(10, 0))
        self.canvas = Canvas(self.canvas_frame, bg="#0a0f1f", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")

        # Status + Step Counter
        self.status = ctk.CTkLabel(self.root, text="Ready to Start", font=("Consolas", 13), text_color="#5ce1e6")
        self.status.pack(pady=(8, 2))

        self.step_label = ctk.CTkLabel(self.root, text="Steps: 0", font=("Consolas", 12), text_color="#9be7ff")
        self.step_label.pack(pady=(0, 8))

    # ---------- Draw Board ---------- #
    def _resize_board(self, event=None):
        if not hasattr(self, "cell"):
            return
        self.canvas.delete("all")
        self._draw_grid()
        self._draw_queens()

    def _make_board(self):
        self.canvas.delete("all")
        self.running = False
        self.solved = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.step_count = 0
        self.step_label.configure(text=f"Steps: {self.step_count}")

        try:
            n = int(self.entry_n.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer ≥ 4.")
            self.status.configure(text="❌ Invalid input! Enter integer ≥ 4", text_color="#ef233c")
            return

        if n < 4:
            messagebox.showwarning("No Solution", "No valid configuration exists for N < 4.")
            self.status.configure(text="⚠️ No solution for N < 4", text_color="#fcbf49")
            return

        self.N.set(n)
        self.positions = [-1] * n
        self.row = 0
        self.next_col = 0
        self._draw_grid()
        self.status.configure(text=f"Board ready for N = {n}", text_color="#5ce1e6")

    def _draw_grid(self):
        n = self.N.get()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        size = min(width, height) - 20
        self.cell = size / n

        for r in range(n):
            for c in range(n):
                x0 = c * self.cell + 10
                y0 = r * self.cell + 10
                x1 = x0 + self.cell
                y1 = y0 + self.cell
                fill = "#0f2027" if (r + c) % 2 == 0 else "#0077b6"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#1e1e1e")

    def _draw_queens(self, highlight=None, color="#f72585"):
        self.canvas.delete("queen")
        n = self.N.get()
        pad = self.cell * 0.15
        for r in range(n):
            c = self.positions[r]
            if c != -1:
                x0 = c * self.cell + 10 + pad
                y0 = r * self.cell + 10 + pad
                x1 = (c + 1) * self.cell + 10 - pad
                y1 = (r + 1) * self.cell + 10 - pad
                self.canvas.create_oval(x0, y0, x1, y1, fill="#001219", outline="#80ffdb", width=2, tags="queen")
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="♛", fill="#5ce1e6",
                                        font=("Consolas", int(self.cell * 0.55)), tags="queen")

        if highlight:
            r, c = highlight
            x0 = c * self.cell + 10
            y0 = r * self.cell + 10
            x1 = (c + 1) * self.cell + 10
            y1 = (r + 1) * self.cell + 10
            self.canvas.create_rectangle(x0, y0, x1, y1, outline=color, width=3, tags="queen")

        self.canvas.update_idletasks()

    # ---------- Backtracking Logic ---------- #
    def is_safe(self, row, col):
        for r in range(row):
            c = self.positions[r]
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def start(self):
        if self.running:
            return
        self._make_board()
        if self.N.get() < 4:
            return
        self.running = True
        self.solved = False
        self.step_count = 0
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.status.configure(text="🧮 Solving...", text_color="#90e0ef")
        self.step_label.configure(text=f"Steps: {self.step_count}")
        self._step()

    def stop(self):
        self.running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        if not self.solved:
            self.status.configure(text="⏸ Stopped", text_color="#fcbf49")

    def reset_board(self):
        self.stop()
        self._make_board()

    def _step(self):
        if not self.running:
            return

        self.step_count += 1
        self.step_label.configure(text=f"Steps: {self.step_count}")
        n = self.N.get()

        if self.row >= n:
            self.solved = True
            self.running = False
            self.btn_stop.configure(state="disabled")
            self.status.configure(text=f"✅ Solved for N = {n} in {self.step_count} steps", text_color="#80ffdb")
            self._draw_queens()
            return

        placed = False
        for c in range(self.next_col, n):
            self._draw_queens(highlight=(self.row, c), color="#ffb703")
            self.step_count += 1
            self.step_label.configure(text=f"Steps: {self.step_count}")

            if self.is_safe(self.row, c):
                self.positions[self.row] = c
                self.row += 1
                self.next_col = 0
                placed = True
                break

        if not placed:
            if self.row == 0:
                self.running = False
                self.btn_stop.configure(state="disabled")
                self.status.configure(text=f"❌ No Solution Found (checked {self.step_count} steps)", text_color="#ef233c")
                return
            self.row -= 1
            prev_col = self.positions[self.row]
            self.positions[self.row] = -1
            self.next_col = prev_col + 1
            self._draw_queens(highlight=(self.row, prev_col), color="#e63946")

        self._draw_queens()
        self.root.after(max(0, self.delay_ms.get()), self._step)


# ---------- MAIN ---------- #
if __name__ == "__main__":
    root = ctk.CTk()
    app = NQueensApp(root)

    # Footer Label (Developer Credit)
    footer = ctk.CTkLabel(
        root,
        text="Developed by Anil Kumar Bal | MCA (AI/ML)",
        font=("Consolas", 11, "bold"),
        text_color="#5ce1e6"
    )
    footer.pack(side="bottom", pady=6)

    root.mainloop()
