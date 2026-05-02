import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DB_FILE = "movies.json"

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        
        # Данные
        self.movies = self.load_data()

        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(root, text="Жанр:").grid(row=1, column=0)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=1, column=1)

        tk.Label(root, text="Год выпуска:").grid(row=2, column=0)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=2, column=1)

        tk.Label(root, text="Рейтинг (0-10):").grid(row=3, column=0)
        self.rating_entry = tk.Entry(root)
        self.rating_entry.grid(row=3, column=1)

        # Кнопка добавления
        self.add_btn = tk.Button(root, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтрация
        tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0)
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=5, column=1)
        
        self.filter_btn = tk.Button(root, text="Применить фильтры", command=self.update_table)
        self.filter_btn.grid(row=6, column=0, columnspan=2)

        # Таблица (Treeview)
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=columns, show='headings')
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.update_table()

    def add_movie(self):
        # Валидация данных (Пункт 5)
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        if not (title and genre and year and rating):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        try:
            year = int(year) # Проверка: год должен быть числом
            rating = float(rating)
            if not (0 <= rating <= 10): # Проверка: рейтинг от 0 до 10
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный год или рейтинг (0-10)")
            return

        new_movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(new_movie)
        self.save_data()
        self.update_table()

    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        f_genre = self.filter_genre.get().lower()

        # Отображение с фильтрацией (Пункт 3)
        for m in self.movies:
            if f_genre in m['genre'].lower():
                self.tree.insert("", tk.END, values=(m['title'], m['genre'], m['year'], m['rating']))

    def save_data(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
