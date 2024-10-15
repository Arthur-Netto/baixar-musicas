import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import yt_dlp as youtube_dl
import threading

# Lista para armazenar as músicas baixadas
musicas_baixadas = []

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes', 0)
        downloaded = d.get('downloaded_bytes', 0)
        if total > 0:
            percent = int(downloaded / total * 100)
            progress_var.set(percent)
            status_text.config(text=f"Baixando sua música... {percent}%")

def baixar_musica():
    link = link_entry.get()
    download_path = download_entry.get()
    if not download_path:
        messagebox.showwarning("Atenção", "Por favor, escolha um diretório de download.")
        return

    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'noplaylist': True,
        'progress_hooks': [progress_hook]
    }

    try:
        progress_var.set(0)
        status_text.config(text="Iniciando download...")
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([link])
            # Adiciona a música baixada à lista
            musicas_baixadas.append(link)  # Armazena o link
            atualizar_lista_musicas()
        status_text.config(text="Download concluído")
        progress_var.set(100)
    except Exception as e:
        status_text.config(text="Erro: " + str(e))
        progress_var.set(0)

def atualizar_lista_musicas():
    lista_musicas.delete(0, tk.END)  # Limpa a lista
    for musica in musicas_baixadas:
        lista_musicas.insert(tk.END, musica)  # Adiciona cada música à lista

def iniciar_download():
    baixar_button.config(state=tk.DISABLED)
    threading.Thread(target=baixar_musica).start()
    baixar_button.config(state=tk.NORMAL)

def escolher_diretorio():
    directory = filedialog.askdirectory()
    if directory:
        download_entry.delete(0, tk.END)
        download_entry.insert(0, directory)

# Cria a janela principal
root = tk.Tk()
root.title("Baixar Música")
root.geometry("600x400")  # Define um tamanho fixo para a janela
root.configure(bg="#f0f0f0")  # Cor de fundo clara

# Cria widgets principais
label = tk.Label(root, text="Digite o link da música:", bg="#f0f0f0", font=("Arial", 12))
label.pack(pady=(20, 0))

link_entry = tk.Entry(root, width=50)
link_entry.pack(pady=(0, 10))

download_label = tk.Label(root, text="Escolha o diretório de download:", bg="#f0f0f0", font=("Arial", 12))
download_label.pack()

download_entry = tk.Entry(root, width=50)
download_entry.pack(pady=(0, 10))

choose_button = tk.Button(root, text="Escolher Diretório", command=escolher_diretorio, bg="#4CAF50", fg="white", font=("Arial", 12))
choose_button.pack(pady=(0, 10))

baixar_button = tk.Button(root, text="Baixar Música", command=iniciar_download, bg="#4CAF50", fg="white", font=("Arial", 12))
baixar_button.pack(pady=(0, 10))

status_text = tk.Label(root, text="", bg="#f0f0f0", font=("Arial", 10))
status_text.pack(pady=(5, 0))

# Barra de progresso
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(fill=tk.X, padx=10, pady=10)

# Lista de músicas baixadas
titulo_lista = tk.Label(root, text="Músicas Baixadas:", bg="#f0f0f0", font=("Arial", 12))
titulo_lista.pack(pady=(10, 0))

lista_musicas = tk.Listbox(root, bg="white", fg="black", font=("Arial", 10))
lista_musicas.pack(fill=tk.BOTH, expand=True)

# Inicia o loop principal da interface
root.mainloop()
