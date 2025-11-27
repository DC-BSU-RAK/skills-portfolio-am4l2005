import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# ------------------ Student ------------------
class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = int(code)
        self.name = name
        self.c1 = int(c1); self.c2 = int(c2); self.c3 = int(c3)
        self.exam = int(exam)

    def cw(self): return self.c1 + self.c2 + self.c3
    def total(self): return self.cw() + self.exam
    def pct(self): return round((self.total() / 160) * 100, 2)

    def grade(self):
        p = self.pct()
        if p >= 70: return "A"
        if p >= 60: return "B"
        if p >= 50: return "C"
        if p >= 40: return "D"
        return "F"

    def format(self):
        return (f"Name: {self.name}\n"
                f"Code: {self.code}\n"
                f"Coursework: {self.cw()}/60\n"
                f"Exam: {self.exam}/100\n"
                f"Total: {self.total()}/160\n"
                f"Percentage: {self.pct()}%\n"
                f"Grade: {self.grade()}\n")

# ------------------ Manager ------------------
class StudentManager:
    def __init__(self, path):
        self.path = path
        self.students = []
        self.load()

    def load(self):
        if not os.path.exists(self.path):
            messagebox.showerror("Error", f"File not found: {self.path}")
            return

        with open(self.path, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]

        if not lines: return

        # Skip first line (number of students)
        data = lines[1:] if lines[0].isdigit() else lines
        for ln in data:
            parts = ln.split(",")
            if len(parts) == 6:
                self.students.append(Student(*parts))

    def by_code(self, code):
        for s in self.students:
            if s.code == code: return s
        return None

# ------------------ App ------------------
class App:
    def __init__(self, root, manager):
        self.root = root
        self.m = manager

        root.title("Student Manager")
        root.geometry("850x500")
        root.config(bg="#f2f2f2")

        tk.Label(root, text="Student Manager", bg="#4c57ff", fg="white",
                 font=("Segoe UI", 18, "bold"), pady=10).pack(fill="x")

        # Main container
        main = tk.Frame(root, bg="#f2f2f2")
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT: Listbox of students
        left = tk.Frame(main, bg="#f2f2f2")
        left.pack(side="left", fill="y")
        tk.Label(left, text="Students", font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
        self.listbox = tk.Listbox(left, width=32, height=23, font=("Segoe UI", 10))
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.select_student)
        self.refresh_listbox()

        # RIGHT: Output
        right = tk.Frame(main, bg="#f2f2f2")
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="Output", font=("Segoe UI", 12, "bold"), bg="#f2f2f2").pack(anchor="w")
        self.output = tk.Text(right, wrap="word", height=20, font=("Segoe UI", 10))
        self.output.pack(fill="both", expand=True)

        # Menu buttons
        menu = tk.Frame(root, bg="#f2f2f2")
        menu.pack(fill="x", pady=6)
        btn = dict(bg="#4c57ff", fg="white", font=("Segoe UI", 10, "bold"), width=20)

        tk.Button(menu, text="View All", command=self.view_all, **btn).pack(side="left", padx=4)
        tk.Button(menu, text="View Individual", command=self.view_single, **btn).pack(side="left", padx=4)
        tk.Button(menu, text="Highest Score", command=self.view_highest, **btn).pack(side="left", padx=4)
        tk.Button(menu, text="Lowest Score", command=self.view_lowest, **btn).pack(side="left", padx=4)

    # ---------------- Utils ----------------
    def write(self, txt):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", txt)
        self.output.config(state="disabled")

    def refresh_listbox(self):
        self.listbox.delete(0, "end")
        for s in self.m.students:
            self.listbox.insert("end", f"{s.code} - {s.name}")

    # ---------------- Features ----------------
    def select_student(self, e=None):
        try: idx = self.listbox.curselection()[0]
        except: return
        s = self.m.students[idx]
        self.write(s.format())

    def view_all(self):
        if not self.m.students:
            self.write("No student records available.")
            return
        out = ""
        total_pct = 0
        for s in self.m.students:
            out += s.format() + "-"*40 + "\n"
            total_pct += s.pct()
        avg = round(total_pct / len(self.m.students), 2)
        out += f"\nTotal Students: {len(self.m.students)}\nAverage Percentage: {avg}%"
        self.write(out)

    def view_single(self):
        code = simpledialog.askinteger("Find Student", "Enter student code:")
        if code is None: return
        s = self.m.by_code(code)
        if not s:
            messagebox.showinfo("Not Found", "No student with that code.")
            return
        self.write(s.format())

    def view_highest(self):
        if not self.m.students: return
        s = max(self.m.students, key=lambda x: x.total())
        self.write("Highest Scoring Student:\n\n" + s.format())

    def view_lowest(self):
        if not self.m.students: return
        s = min(self.m.students, key=lambda x: x.total())
        self.write("Lowest Scoring Student:\n\n" + s.format())

# ---------------- Main ----------------
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks.txt")
    mgr = StudentManager(path)
    root = tk.Tk()
    App(root, mgr)
    root.mainloop()

if __name__ == "__main__":
    main()
