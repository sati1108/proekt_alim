# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 13:40:47 2026

@author: student
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime

# --- Константы ---
DATA_FILE = "movie_library.json"
MAX_RATING = 10
MIN_RATING = 0
CURRENT_YEAR = datetime.now().year

# --- Основное окно ---
root = tk.Tk()
root.title("Movie Library")
root.geometry("800x600") # Устанавливаем начальный размер окна

# --- Переменные для хранения фильмов ---
movies = []

# --- Функции ---

def load_movies():
    """Загружает данные о фильмах из JSON файла."""
    global movies
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                movies = json.load(f)
            update_movie_table() # Обновляем таблицу после загрузки
        except (json.JSONDecodeError, FileNotFoundError):
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные из {DATA_FILE}. Файл может быть поврежден или пуст.")
            movies = [] # Сбрасываем данные, если файл некорректен
    else:
        movies = [] # Если файла нет, начинаем с пустого списка

def save_movies():
    """Сохраняет текущие данные о фильмах в JSON файл."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Успех", "Данные успешно сохранены.")
    except IOError:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные в {DATA_FILE}.")

def validate_input(title, genre, year_str, rating_str):
    """Проверяет корректность ввода данных."""
    if not title or not genre or not year_str or not rating_str:
        return "Все поля должны быть заполнены."

    try:
        year = int(year_str)
        if not (1888 <= year <= CURRENT_YEAR): # Примерный диапазон для года выпуска
            return f"Год выпуска должен быть между 1888 и {CURRENT_YEAR}."
    except ValueError:
        return "Год выпуска должен быть числом."

    try:
        rating = float(rating_str)
        if not (MIN_RATING <= rating <= MAX_RATING):
            return f"Рейтинг должен быть от {MIN_RATING} до {MAX_RATING}."
    except ValueError:
        return "Рейтинг должен быть числом (например, 7.5 или 9)."

    return None # Нет ошибок

def add_movie():
    """Добавляет новый фильм в список и обновляет таблицу."""
    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year_str = entry_year.get().strip()
    rating_str = entry_rating.get().strip()

    error_message = validate_input(title, genre, year_str, rating_str)
    if error_message:
        messagebox.showerror("Ошибка ввода", error_message)
        return

    year = int(year_str)
    rating = float(rating_str)

    new_movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating
    }
    movies.append(new_movie)
    update_movie_table()
    clear_input_fields()
    save_movies() # Автоматически сохраняем после добавления

def clear_input_fields():
    """Очищает поля ввода."""
    entry_title.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_year.delete(0, tk.END)
    entry_rating.delete(0, tk.END)

def update_movie_table(filter_genre=None, filter_year=None):
    """
    Обновляет таблицу с фильмами.
    Принимает опциональные параметры для фильтрации.
    """
    # Очищаем текущие записи в таблице
    for row in tree.get_children():
        tree.delete(row)

    filtered_movies = movies

    # Применяем фильтр по жанру
    if filter_genre:
        filtered_movies = [
            movie for movie in filtered_movies
            if movie["genre"].lower() == filter_genre.lower()
        ]

    # Применяем фильтр по году
    if filter_year:
        try:
            filter_year_int = int(filter_year)
            filtered_movies = [
                movie for movie in filtered_movies
                if movie["year"] == filter_year_int
            ]
        except ValueError:
            pass # Игнорируем некорректный ввод года для фильтра

    # Добавляем отфильтрованные фильмы в таблицу
    for movie in filtered_movies:
        tree.insert("", tk.END, values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            movie["rating"]
        ))

def apply_filters():
    """Применяет выбранные фильтры к таблице."""
    genre_filter = entry_filter_genre.get().strip()
    year_filter = entry_filter_year.get().strip()
    update_movie_table(filter_genre=genre_filter if genre_filter else None,
                       filter_year=year_filter if year_filter else None)

def reset_filters():
    """Сбрасывает поля фильтрации и обновляет таблицу."""
    entry_filter_genre.delete(0, tk.END)
    entry_filter_year.delete(0, tk.END)
    update_movie_table()

def delete_selected_movie():
    """Удаляет выбранный фильм из списка."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Внимание", "Пожалуйста, выберите фильм для удаления.")
        return

    # Получаем индекс выбранного элемента в таблице
    item_index = tree.index(selected_item)
    # Находим соответствующий фильм в основном списке `movies`
    # Это может быть не совсем тривиально, если есть дубликаты названий,
    # но для простоты предполагаем, что порядок соответствует.
    # Более надежный способ - добавить уникальный ID к каждому фильму.
    # Для данного примера, мы будем ориентироваться на первый найденный фильм
    # с такими же данными, что было не совсем точно.
    # Корректнее будет работать с индексом, если мы будем хранить его.
    # Давайте упростим: используем данные из строки для поиска.

    # Получаем значения из выбранной строки
    values = tree.item(selected_item, 'values')
    if not values:
        return # Нечего удалять

    title_to_delete = values[0]
    genre_to_delete = values[1]
    year_to_delete = int(values[2])
    rating_to_delete = float(values[3])

    # Ищем фильм в списке `movies` и удаляем его
    movie_to_remove = None
    for movie in movies:
        if (movie["title"] == title_to_delete and
            movie["genre"] == genre_to_delete and
            movie["year"] == year_to_delete and
            movie["rating"] == rating_to_delete):
            movie_to_remove = movie
            break

    if movie_to_remove:
        movies.remove(movie_to_remove)
        update_movie_table()
        save_movies()
    else:
        messagebox.showerror("Ошибка", "Не удалось найти выбранный фильм для удаления.")


# --- Настройка GUI ---

# Фрейм для ввода данных
input_frame = ttk.LabelFrame(root, text="Добавить новый фильм", padding=(10, 5))
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_title = ttk.Entry(input_frame, width=40)
entry_title.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

ttk.Label(input_frame, text="Жанр:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
entry_genre = ttk.Entry(input_frame, width=40)
entry_genre.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

ttk.Label(input_frame, text="Год выпуска:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
entry_year = ttk.Entry(input_frame, width=15)
entry_year.grid(row=2, column=1, padx=5, pady=2, sticky="w")

ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
entry_rating = ttk.Entry(input_frame, width=15)
entry_rating.grid(row=3, column=1, padx=5, pady=2, sticky="w")

button_add = ttk.Button(input_frame, text="Добавить фильм", command=add_movie)
button_add.grid(row=4, column=0, columnspan=2, pady=10)

input_frame.columnconfigure(1, weight=1) # Позволяет полю ввода расширяться

# Фрейм для фильтрации
filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding=(10, 5))
filter_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_filter_genre = ttk.Entry(filter_frame, width=30)
entry_filter_genre.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

ttk.Label(filter_frame, text="По году выпуска:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
entry_filter_year = ttk.Entry(filter_frame, width=15)
entry_filter_year.grid(row=1, column=1, padx=5, pady=2, sticky="w")

button_apply_filters = ttk.Button(filter_frame, text="Применить фильтры", command=apply_filters)
button_apply_filters.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

button_reset_filters = ttk.Button(filter_frame, text="Сбросить фильтры", command=reset_filters)
button_reset_filters.grid(row=0, column=3, rowspan=2, padx=5, pady=5)

filter_frame.columnconfigure(1, weight=1)

# Фрейм для таблицы фильмов
table_frame = ttk.Frame(root, padding=(10, 10))
table_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Создаем виджет Treeview для отображения таблицы
columns = ("Название", "Жанр", "Год выпуска", "Рейтинг")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

# Настраиваем заголовки столбцов
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor=tk.W) # Устанавливаем ширину и выравнивание
# Настраиваем ширину для рейтинга, чтобы он помещался
tree.column("Рейтинг", width=80, anchor=tk.CENTER)
tree.column("Год выпуска", width=100, anchor=tk.CENTER)
tree.column("Жанр", width=170, anchor=tk.W)

# Добавляем полосы прокрутки
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
vsb.grid(row=0, column=1, sticky="ns")
hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
hsb.grid(row=1, column=0, sticky="ew")

tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.grid(row=0, column=0, sticky='nsew')

# Добавляем кнопки для управления таблицей (например, удаление)
button_frame = ttk.Frame(root, padding=(10, 5))
button_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

btn_delete = ttk.Button(button_frame, text="Удалить выбранный", command=delete_selected_movie)
btn_delete.grid(row=0, column=0, padx=5)

# Настраиваем растяжение виджетов
root.grid_rowconfigure(2, weight=1) # Основная таблица должна занимать доступное пространство
root.grid_columnconfigure(0, weight=1)
table_frame.grid_rowconfigure(0, weight=1)
table_frame.grid_columnconfigure(0, weight=1)

# --- Инициализация ---
load_movies() # Загружаем данные при запуске

# --- Запуск приложения ---
root.mainloop()
