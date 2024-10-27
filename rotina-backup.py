import tkinter as tk
from tkinter import filedialog, ttk
import shutil
import os
import datetime
import threading
import time

def backup_files(source_folder, destination_folder, num_copies, interval, progress_label, window):
    log_file = os.path.join(os.path.dirname(__file__), 'log.txt')
    with open(log_file, 'a') as log:
        for i in range(num_copies):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log.write(f'Backup {i + 1} - {timestamp}\n')
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    source_path = os.path.join(root, file)
                    extension = os.path.splitext(file)[1]
                    destination_path = os.path.join(destination_folder, f'{file}_{i + 1}{extension}')
                    shutil.copy2(source_path, destination_path)
                    log.write(f'{timestamp} - Copied: {file} -> {destination_path}\n')
            progress_label.config(text=f'Progresso: {i + 1}/{num_copies}')
            time.sleep(interval)

    progress_label.config(text='Backup concluído.')
    enable_start_button(window)

def select_source_folder():
    source_folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(tk.END, source_folder)

def select_destination_folder():
    destination_folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(tk.END, destination_folder)

def start_backup(window):
    source_folder = source_entry.get()
    destination_folder = destination_entry.get()
    num_copies = int(num_copies_entry.get())
    interval_hours = interval_hours_var.get()
    interval_minutes = interval_minutes_var.get()
    interval_seconds = interval_seconds_var.get()
    interval = interval_hours * 3600 + interval_minutes * 60 + interval_seconds

    progress_label.config(text='Backup em andamento...')
    start_button.config(state=tk.DISABLED)

    thread = threading.Thread(target=backup_files, args=(source_folder, destination_folder, num_copies, interval, progress_label, window))
    thread.start()

def enable_start_button(window):
    start_button.config(state=tk.NORMAL)

# Cria a janela da interface gráfica
window = tk.Tk()
window.title('Backup Automático')
window.geometry('400x270')
window.configure(bg="#E6F0F3")  # Light blue background color

# Rótulos e campos de entrada
source_label = tk.Label(window, text='Pasta de Origem:', bg="#E6F0F3")  # Light blue background color
source_label.pack()
source_entry = tk.Entry(window)
source_entry.pack()

source_button = tk.Button(window, text='Selecionar', command=select_source_folder, bg="#3E8CC7", fg="white")  # Blue button color
source_button.pack()

destination_label = tk.Label(window, text='Pasta de Destino:', bg="#E6F0F3")  # Light blue background color
destination_label.pack()
destination_entry = tk.Entry(window)
destination_entry.pack()

destination_button = tk.Button(window, text='Selecionar', command=select_destination_folder, bg="#3E8CC7", fg="white")  # Blue button color
destination_button.pack()

num_copies_label = tk.Label(window, text='Quantidade de Cópias:', bg="#E6F0F3")  # Light blue background color
num_copies_label.pack()
num_copies_entry = tk.Entry(window)
num_copies_entry.pack()

# Rótulo de intervalo entre cópias
interval_label = ttk.Label(window, text='Intervalo entre cópias:', background="#E6F0F3")  # Light blue background color
interval_label.pack()

interval_frame = ttk.Frame(window)
interval_frame.pack()

interval_hours_var = tk.IntVar(value=0)
interval_minutes_var = tk.IntVar(value=0)
interval_seconds_var = tk.IntVar(value=0)

interval_hours_label = ttk.Label(interval_frame, text='Horas:', background="#E6F0F3")  # Light blue background color
interval_hours_label.pack(side=tk.LEFT)
interval_hours_spinbox = tk.Spinbox(interval_frame, from_=0, to=23, textvariable=interval_hours_var, width=3)
interval_hours_spinbox.pack(side=tk.LEFT)

interval_minutes_label = ttk.Label(interval_frame, text='Minutos:', background="#E6F0F3")  # Light blue background color
interval_minutes_label.pack(side=tk.LEFT)
interval_minutes_spinbox = tk.Spinbox(interval_frame, from_=0, to=59, textvariable=interval_minutes_var, width=3)
interval_minutes_spinbox.pack(side=tk.LEFT)

interval_seconds_label = ttk.Label(interval_frame, text='Segundos:', background="#E6F0F3")  # Light blue background color
interval_seconds_label.pack(side=tk.LEFT)
interval_seconds_spinbox = tk.Spinbox(interval_frame, from_=0, to=59, textvariable=interval_seconds_var, width=3)
interval_seconds_spinbox.pack(side=tk.LEFT)

# Botão de iniciar backup
start_button = ttk.Button(window, text='Iniciar Backup', command=lambda: start_backup(window), style="Blue.TButton")  # Blue button style
start_button.pack()

# Rótulo de progresso
progress_label = ttk.Label(window, text='', background="#E6F0F3")  # Light blue background color
progress_label.pack()

# Estilo dos botões
style = ttk.Style()
style.configure("Blue.TButton", background="#3E8CC7", foreground="white")  # Blue button style

# Executa a janela principal
window.mainloop()
