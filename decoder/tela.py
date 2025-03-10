import threading
import socket
import binascii
import datetime
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

def start_server():
    global server, running
    if running:
        return
    
    running = True
    log_dir = "logs/"
    os.makedirs(log_dir, exist_ok=True)
    
    port = int(port_entry.get())
    log_name = log_name_entry.get()
    
    if log_var.get():
        payload_file_name = os.path.join(log_dir, log_name + "_raw.csv")
        decoded_file_name = os.path.join(log_dir, log_name + "_decoded.csv")
    else:
        payload_file_name = decoded_file_name = ""
    
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(("0.0.0.0", port))
        log("Servidor iniciado na porta {}".format(port))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar servidor: {e}")
        running = False
        return
    
    threading.Thread(target=receive_messages, args=(payload_file_name,), daemon=True).start()

def receive_messages(payload_file_name):
    while running:
        try:
            message, address = server.recvfrom(1024)
            data = binascii.hexlify(message).decode()
            curr_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log(f"[{curr_time}] Recebido de {address}: {data}")
            
            if log_var.get():
                with open(payload_file_name, "a") as f:
                    f.write(f"{curr_time},{address},{data}\n")
        except:
            break

def send_command():
    cmd = command_entry.get()
    if not cmd or not server:
        return
    server.sendto(cmd.encode("utf-8"), ("127.0.0.1", int(port_entry.get())))
    log(f"Comando enviado: {cmd}")
    command_entry.delete(0, tk.END)

def log(message):
    text_area.insert(tk.END, message + "\n")
    text_area.yview(tk.END)

def stop_server():
    global running
    running = False
    if server:
        server.close()
    log("Servidor parado.")

def save_log():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(text_area.get("1.0", tk.END))
        messagebox.showinfo("Sucesso", "Log salvo com sucesso!")

# GUI Setup
root = tk.Tk()
root.title("Servidor UDP")

frame = tk.Frame(root)
frame.pack(pady=10)

# Porta
tk.Label(frame, text="Porta:").grid(row=0, column=0)
port_entry = tk.Entry(frame)
port_entry.grid(row=0, column=1)
port_entry.insert(0, "9116")

# Log
log_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Habilitar Log", variable=log_var).grid(row=1, column=0)
log_name_entry = tk.Entry(frame)
log_name_entry.grid(row=1, column=1)
log_name_entry.insert(0, "log")

# Botões
tk.Button(frame, text="Iniciar Servidor", command=start_server).grid(row=2, column=0)
tk.Button(frame, text="Parar Servidor", command=stop_server).grid(row=2, column=1)
tk.Button(frame, text="Salvar Log", command=save_log).grid(row=2, column=2)

# Área de log
text_area = scrolledtext.ScrolledText(root, width=60, height=20)
text_area.pack()

# Entrada de comando
command_frame = tk.Frame(root)
command_frame.pack(pady=5)
command_entry = tk.Entry(command_frame, width=50)
command_entry.pack(side=tk.LEFT)
tk.Button(command_frame, text="Enviar", command=send_command).pack(side=tk.RIGHT)

root.mainloop()
