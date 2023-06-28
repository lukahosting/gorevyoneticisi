import psutil
import tkinter as tk
from tkinter import ttk
import signal

def get_process_list():
    process_list.delete(*process_list.get_children())
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        pid = proc.info['pid']
        name = proc.info['name']
        memory = proc.info['memory_info'].rss / 1024 / 1024 / 1024  # Convert to GB
        process_list.insert("", "end", values=(pid, name, f"{memory:.2f} GB"))

def end_task():
    selected_item = process_list.focus()
    if selected_item:
        pid = int(process_list.item(selected_item)['values'][0])
        try:
            process = psutil.Process(pid)
            process.terminate()
            get_process_list()  # Refresh the process list after termination
        except psutil.NoSuchProcess:
            # Process may have already terminated
            pass

root = tk.Tk()
root.title("Görev Yöneticisi")

process_list = ttk.Treeview(root, columns=("pid", "name", "memory"), show="headings")
process_list.heading("pid", text="PID")
process_list.heading("name", text="İsim")
process_list.heading("memory", text="Bellek (GB)")

process_list.pack(pady=10)

refresh_button = ttk.Button(root, text="Yenile", command=get_process_list)
refresh_button.pack()

end_task_button = ttk.Button(root, text="Görevi Sonlandır", command=end_task)
end_task_button.pack()

get_process_list()  # İlk açılışta işlem listesini doldurmak için

root.mainloop()
