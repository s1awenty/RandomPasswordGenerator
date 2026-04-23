import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import string
import os

# Константы для файла истории
HISTORY_FILE = 'password_history.json'

# Создаем главное окно
root = tk.Tk()
root.title("Random Password Generator")

# Настройка интерфейса
length_var = tk.IntVar(value=12)
include_digits = tk.BooleanVar(value=True)
include_letters = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=False)

# Функции
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_password():
    length = length_var.get()
    if not (4 <= length <= 64):
        messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 64 символов")
        return
    
    chars = ''
    if include_digits.get():
        chars += string.digits
    if include_letters.get():
        chars += string.ascii_letters
    if include_symbols.get():
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return

    password = ''.join(random.choice(chars) for _ in range(length))
    password_var.set(password)

    # Добавление в историю
    history = load_history()
    entry = {"password": password}
    history.append(entry)
    save_history(history)
    update_history_table()

def update_history_table():
    for row in tree.get_children():
        tree.delete(row)
    history = load_history()
    for idx, entry in enumerate(history):
        tree.insert('', 'end', values=(entry['password'],))

# Элементы интерфейса
# Ползунок длины
ttk.Label(root, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
length_slider = ttk.Scale(root, from_=4, to=64, orient='horizontal', variable=length_var)
length_slider.grid(row=0, column=1, padx=5, pady=5, sticky='we')

# Чекбоксы
ttk.Checkbutton(root, text="Цифры", variable=include_digits).grid(row=1, column=0, sticky='w')
ttk.Checkbutton(root, text="Буквы", variable=include_letters).grid(row=1, column=1, sticky='w')
ttk.Checkbutton(root, text="Спецсимволы", variable=include_symbols).grid(row=1, column=2, sticky='w')

# Кнопка генерации
generate_button = ttk.Button(root, text="Генерировать", command=generate_password)
generate_button.grid(row=2, column=0, columnspan=3, pady=10)

# Поле для отображения пароля
password_var = tk.StringVar()
ttk.Label(root, text="Пароль:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
password_entry = ttk.Entry(root, textvariable=password_var, width=30)
password_entry.grid(row=3, column=1, padx=5, pady=5, sticky='we')

# Таблица истории
ttk.Label(root, text="История паролей:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
columns = ('Пароль',)
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
tree.heading('Пароль', text='Пароль')
tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

# Обновление таблицы при запуске
update_history_table()

# Расширение окна
root.columnconfigure(1, weight=1)
root.rowconfigure(5, weight=1)

# Запуск приложения
root.mainloop()
