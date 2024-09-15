import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

class WikipediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wikipedia Search")

        # Frame para a tela inicial
        self.home_frame = tk.Frame(root)
        self.home_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.query_label = ttk.Label(self.home_frame, text="Digite o termo de busca:")
        self.query_label.pack(pady=10)

        self.query_entry = ttk.Entry(self.home_frame, width=50)
        self.query_entry.pack(pady=5)

        self.search_button = ttk.Button(self.home_frame, text="Buscar", command=self.search)
        self.search_button.pack(pady=10)

        # Frame para a tela de resultados
        self.result_frame = tk.Frame(root)

        self.title_label = ttk.Label(self.result_frame, text="", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.image_label = tk.Label(self.result_frame)
        self.image_label.pack(pady=10)

        self.summary_text = tk.Text(self.result_frame, wrap=tk.WORD, height=10, width=80, font=("Arial", 12))
        self.summary_text.pack(pady=10)
        self.summary_text.config(state=tk.DISABLED)

        self.back_button = ttk.Button(self.result_frame, text="Voltar", command=self.show_home)
        self.back_button.pack(pady=10)

    def search(self):
        query = self.query_entry.get()
        if query:
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            try:
                response = requests.get(url)
                response.raise_for_status()  # Verifica se houve erro na requisição
                data = response.json()
                title = data.get('title', 'Não encontrado')
                summary = data.get('extract', 'Nenhuma descrição disponível.')
                image_url = data.get('thumbnail', {}).get('source', None)  # Usar a URL da imagem em miniatura
                self.show_results(title, summary, image_url)
            except Exception as e:
                self.show_results("Erro", f"Ocorreu um erro: {e}", None)

    def show_results(self, title, summary, image_url):
        self.home_frame.pack_forget()
        self.title_label.config(text=title)
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)

        # Atualizar a imagem
        if image_url:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(image_url, headers=headers)
                response.raise_for_status()  # Verifica se houve erro na requisição
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                image = image.resize((200, 150), Image.LANCZOS)  # Ajustar o tamanho da imagem
                self.image = ImageTk.PhotoImage(image)  # Manter uma referência da imagem
                self.image_label.config(image=self.image)
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")
                self.image_label.config(image='')
        else:
            self.image_label.config(image='')

        self.result_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def show_home(self):
        self.result_frame.pack_forget()
        self.home_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Configuração da interface gráfica
root = tk.Tk()
app = WikipediaApp(root)

# Iniciar a aplicação
root.mainloop()
