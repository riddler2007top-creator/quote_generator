import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

FILENAME = "quotes.json"

def load_data():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"quotes": [], "history": []}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generate_quote():
    if not data["quotes"]:
        messagebox.showinfo("Информация", "База цитат пуста. Добавьте свои цитаты!")
        return

    quote = random.choice(data["quotes"])
    data["history"].append(quote)
    save_data(data)
    update_history()

    text_quote.config(state="normal")
    text_quote.delete(1.0, tk.END)
    text_quote.insert(tk.END, f'"{quote["text"]}"\n\n— {quote["author"]} ({quote["topic"]})')
    text_quote.config(state="disabled")

def update_history():
    for i in treeview.get_children():
        treeview.delete(i)
    for q in data["history"]:
        treeview.insert("", "end", values=(q["text"], q["author"], q["topic"]))

def filter_history():
    author = entry_author.get()
    topic = entry_topic.get()
    for i in treeview.get_children():
        treeview.delete(i)
    for q in data["history"]:
        if (not author or author.lower() in q["author"].lower()) and (not topic or topic.lower() in q["topic"].lower()):
            treeview.insert("", "end", values=(q["text"], q["author"], q["topic"]))

# Загрузка данных
data = load_data()

# Окно приложения
root = tk.Tk()
root.title("Генератор случайных цитат")
root.geometry("750x500")

# Вкладки: Генерация и История/Фильтр
tab_control = ttk.Notebook(root)
tab_gen = ttk.Frame(tab_control)
tab_hist = ttk.Frame(tab_control)
tab_control.add(tab_gen, text="Сгенерировать цитату")
tab_control.add(tab_hist, text="История и фильтр")
tab_control.pack(expand=1, fill="both")

# Вкладка "Сгенерировать цитату"
btn_generate = tk.Button(tab_gen, text="Сгенерировать цитату", command=generate_quote, font=("Arial", 14))
btn_generate.pack(pady=20)

text_quote = tk.Text(tab_gen, height=6, width=60, font=("Arial", 12), state="disabled", wrap="word")
text_quote.pack(pady=10)

# Вкладка "История и фильтр"
tk.Label(tab_hist, text="Фильтр по автору:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_author = tk.Entry(tab_hist, width=20)
entry_author.grid(row=0, column=1, padx=10, pady=5)

tk.Label(tab_hist, text="Фильтр по теме:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_topic = tk.Entry(tab_hist, width=20)
entry_topic.grid(row=0, column=3, padx=10, pady=5)

btn_filter = tk.Button(tab_hist, text="Применить фильтр", command=filter_history)
btn_filter.grid(row=0, column=4, padx=10)

treeview = ttk.Treeview(tab_hist, columns=("Цитата", "Автор", "Тема"), show="headings")
treeview.heading("Цитата", text="Цитата")
treeview.heading("Автор", text="Автор")
treeview.heading("Тема", text="Тема")
treeview.column("Цитата", width=350)
treeview.column("Автор", width=120)
treeview.column("Тема", width=120)
treeview.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

# Заполнение истории при запуске
update_history()

root.mainloop()
