import tkinter as tk
from pytube import YouTube

def baixar_musica():
    link = link_entry.get()
    try:
        yt = YouTube(link)
        status_text.config(text="Baixando sua música: " + yt.title)
        audio = yt.streams.filter(only_audio=True).first()
        audio.download()
        audio.download('c:\\Users\\Admin\\Downloads')  # Salva no diretório específico
        status_text.config(text="Download concluído")
    except Exception as e:
        status_text.config(text="Erro: " + str(e))

# Cria a janela principal
root = tk.Tk()
root.title("Baixar Música")

# Cria widgets
label = tk.Label(root, text="Digite o link da música:")
label.pack()

link_entry = tk.Entry(root, width=50)
link_entry.pack()

baixar_button = tk.Button(root, text="Baixar Música", command=baixar_musica)
baixar_button.pack()

status_text = tk.Label(root, text="")
status_text.pack()

# Inicia o loop principal da interface
root.mainloop()
