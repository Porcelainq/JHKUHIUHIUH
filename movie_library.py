import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data.json"

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("750x550")

        self.movies = []       # список фильмов в оперативной памяти
        self.load_data()       # загружаем из JSON при старте

        # ---------- фрейм ввода ----------
        input_frame = ttk.LabelFrame(root, text="Добавить фильм", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="e")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="e")
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(input_frame, textvariable=self.genre_var,
                                        values=["Боевик", "Комедия", "Драма", "Ужасы", "Фантастика",
                                                "Триллер", "Мелодрама", "Документальный", "Аниме"])
        self.genre_combo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky="e")
        self.year_entry = ttk.Entry(input_frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="e")
        self.rating_entry = ttk.Entry(input_frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        add_btn = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        add_btn.grid(row=1, column=4, padx=10)

        # ---------- фрейм фильтрации ----------
        filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky="e")
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var,
                                               values=["Все"] + sorted(set(self.genre_combo['values'])))
        self.filter_genre_combo.current(0)
        self.filter_genre_combo.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(filter_frame, text="По году (YYYY):").grid(row=0, column=2, sticky="e")
        self.filter_year_entry = ttk.Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5, pady=2)

        filter_btn = ttk.Button(filter_frame, text="Применить", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5)

        reset_btn = ttk.Button(filter_frame, text="Сбросить", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5)

        # ---------- таблица ----------
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("№", "Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("№", text="№")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("№", width=40, anchor="center")
        self.tree.column("Название", width=250)
        self.tree.column("Жанр", width=130)
        self.tree.column("Год", width=80, anchor="center")
        self.tree.column("Рейтинг", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.refresh_table()   # первоначальное заполнение

    # ======== работа с JSON ========
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.movies = []
        else:
            self.movies = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)

    # ======== валидация и добавление ========
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_var.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        if not title or not genre or not year_str or not rating_str:
            messagebox.showwarning("Проверка ввода", "Все поля обязательны для заполнения.")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть целым числом.")
            return

        try:
            rating = float(rating_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
            return

        if rating < 0 or rating > 10:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
            return

        # Добавляем фильм в список и сохраняем
        self.movies.append({
            "название": title,
            "жанр": genre,
            "год": year,
            "рейтинг": rating
        })
        self.save_data()
        self.refresh_table()

        # Очищаем поля ввода
        self.title_entry.delete(0, tk.END)
        self.genre_var.set("")
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Фильм добавлен!")

    # ======== фильтрация ========
    def apply_filter(self):
        genre_filter = self.filter_genre_var.get().strip()
        year_filter = self.filter_year_entry.get().strip()

        filtered = self.movies
        if genre_filter and genre_filter != "Все":
            filtered = [m for m in filtered if m["жанр"].lower() == genre_filter.lower()]

        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["год"] == year_int]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтрации должен быть числом.")
                return

        self.update_table(filtered)

    def reset_filter(self):
        self.filter_genre_combo.current(0)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()

    # ======== обновление таблицы ========
    def refresh_table(self):
        self.update_table(self.movies)

    def update_table(self, movie_list):
        # Удаляем все строки
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Заполняем заново
        for idx, movie in enumerate(movie_list, start=1):
            self.tree.insert("", "end", values=(
                idx,
                movie["название"],
                movie["жанр"],
                movie["год"],
                movie["рейтинг"]
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
