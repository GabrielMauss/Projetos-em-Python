import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import random
import threading

class JogoForcaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variáveis do jogo
        self.palavra = ""
        self.letras_palavra = set()
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.max_erros = 6
        
        self.criar_interface()
        self.iniciar_novo_jogo()
    
    def criar_interface(self):
        """Cria a interface gráfica do jogo"""
        # Título
        titulo = tk.Label(self.root, text="JOGO DA FORCA", 
                         font=("Arial", 24, "bold"), 
                         bg="#f0f0f0", fg="#333")
        titulo.pack(pady=20)
        
        # Canvas para desenhar a forca
        self.canvas = tk.Canvas(self.root, width=300, height=250, 
                               bg="white", relief="solid", borderwidth=1)
        self.canvas.pack(pady=10)
        
        # Label para mostrar a palavra
        self.label_palavra = tk.Label(self.root, text="", 
                                     font=("Courier", 20, "bold"), 
                                     bg="#f0f0f0", fg="#333")
        self.label_palavra.pack(pady=20)
        
        # Frame para entrada de letra
        frame_entrada = tk.Frame(self.root, bg="#f0f0f0")
        frame_entrada.pack(pady=10)
        
        tk.Label(frame_entrada, text="Digite uma letra:", 
                font=("Arial", 12), bg="#f0f0f0").pack(side=tk.LEFT)
        
        self.entry_letra = tk.Entry(frame_entrada, font=("Arial", 14), 
                                   width=3, justify="center")
        self.entry_letra.pack(side=tk.LEFT, padx=10)
        self.entry_letra.bind("<Return>", self.processar_tentativa)
        
        self.btn_tentar = tk.Button(frame_entrada, text="Tentar", 
                                   command=self.processar_tentativa,
                                   font=("Arial", 12), bg="#4CAF50", 
                                   fg="white", padx=20)
        self.btn_tentar.pack(side=tk.LEFT, padx=5)
        
        # Labels para informações do jogo
        self.label_erradas = tk.Label(self.root, text="Letras erradas: ", 
                                     font=("Arial", 12), bg="#f0f0f0")
        self.label_erradas.pack(pady=5)
        
        self.label_tentativas = tk.Label(self.root, text="", 
                                        font=("Arial", 12), bg="#f0f0f0")
        self.label_tentativas.pack(pady=5)
        
        # Botão para novo jogo
        self.btn_novo_jogo = tk.Button(self.root, text="Novo Jogo", 
                                      command=self.iniciar_novo_jogo,
                                      font=("Arial", 12), bg="#2196F3", 
                                      fg="white", padx=20)
        self.btn_novo_jogo.pack(pady=20)
        
        # Label de status
        self.label_status = tk.Label(self.root, text="Buscando palavra...", 
                                    font=("Arial", 10), bg="#f0f0f0", fg="#666")
        self.label_status.pack(pady=5)
    
    def obter_palavra(self):
        """Busca uma palavra aleatória da API"""
        try:
            response = requests.get("https://random-word-api.herokuapp.com/word", timeout=5)
            if response.status_code == 200:
                palavras = response.json()
                return palavras[0].upper()
            else:
                return self.palavra_backup()
        except:
            return self.palavra_backup()
    
    def palavra_backup(self):
        """Retorna uma palavra de backup"""
        palavras_backup = ["PYTHON", "PROGRAMACAO", "COMPUTADOR", "DESENVOLVIMENTO", 
                          "ALGORITMO", "VARIAVEL", "FUNCAO", "CLASSE", "OBJETO",
                          "INTERFACE", "GRAFICO", "TKINTER", "APLICACAO", "SOFTWARE"]
        return random.choice(palavras_backup)
    
    def iniciar_novo_jogo(self):
        """Inicia um novo jogo"""
        self.label_status.config(text="Buscando palavra...")
        self.root.update()
        
        # Busca palavra em thread separada para não travar a interface
        def buscar_palavra():
            self.palavra = self.obter_palavra()
            self.letras_palavra = set(self.palavra)
            self.letras_corretas = set()
            self.letras_erradas = set()
            
            # Atualiza interface na thread principal
            self.root.after(0, self.atualizar_interface)
        
        thread = threading.Thread(target=buscar_palavra)
        thread.daemon = True
        thread.start()
    
    def atualizar_interface(self):
        """Atualiza todos os elementos da interface"""
        self.desenhar_forca()
        self.atualizar_palavra()
        self.atualizar_letras_erradas()
        self.atualizar_tentativas()
        self.label_status.config(text="Jogo em andamento")
        self.entry_letra.config(state="normal")
        self.btn_tentar.config(state="normal")
        self.entry_letra.focus()
    
    def desenhar_forca(self):
        """Desenha a forca baseado no número de erros"""
        self.canvas.delete("all")
        
        # Base da forca
        self.canvas.create_line(50, 230, 150, 230, width=3, fill="brown")  # Base
        self.canvas.create_line(100, 230, 100, 30, width=3, fill="brown")   # Poste
        self.canvas.create_line(100, 30, 200, 30, width=3, fill="brown")    # Topo
        self.canvas.create_line(200, 30, 200, 60, width=3, fill="brown")    # Corda
        
        erros = len(self.letras_erradas)
        
        # Desenha partes do boneco baseado nos erros
        if erros >= 1:  # Cabeça
            self.canvas.create_oval(185, 60, 215, 90, outline="black", width=2)
        
        if erros >= 2:  # Corpo
            self.canvas.create_line(200, 90, 200, 150, width=2, fill="black")
        
        if erros >= 3:  # Braço esquerdo
            self.canvas.create_line(200, 110, 170, 130, width=2, fill="black")
        
        if erros >= 4:  # Braço direito
            self.canvas.create_line(200, 110, 230, 130, width=2, fill="black")
        
        if erros >= 5:  # Perna esquerda
            self.canvas.create_line(200, 150, 170, 180, width=2, fill="black")
        
        if erros >= 6:  # Perna direita
            self.canvas.create_line(200, 150, 230, 180, width=2, fill="black")
    
    def atualizar_palavra(self):
        """Atualiza a exibição da palavra"""
        resultado = ""
        for letra in self.palavra:
            if letra in self.letras_corretas:
                resultado += letra + " "
            else:
                resultado += "_ "
        self.label_palavra.config(text=resultado)
    
    def atualizar_letras_erradas(self):
        """Atualiza a exibição das letras erradas"""
        if self.letras_erradas:
            texto = "Letras erradas: " + " ".join(sorted(self.letras_erradas))
        else:
            texto = "Letras erradas: "
        self.label_erradas.config(text=texto)
    
    def atualizar_tentativas(self):
        """Atualiza o número de tentativas restantes"""
        restantes = self.max_erros - len(self.letras_erradas)
        self.label_tentativas.config(text=f"Tentativas restantes: {restantes}")
    
    def processar_tentativa(self, event=None):
        """Processa a tentativa do jogador"""
        tentativa = self.entry_letra.get().upper().strip()
        self.entry_letra.delete(0, tk.END)
        
        # Valida a entrada
        if len(tentativa) != 1 or not tentativa.isalpha():
            messagebox.showwarning("Entrada inválida", "Por favor, digite apenas uma letra.")
            return
        
        # Verifica se a letra já foi tentada
        if tentativa in self.letras_corretas or tentativa in self.letras_erradas:
            messagebox.showinfo("Letra repetida", "Você já tentou essa letra!")
            return
        
        # Processa a tentativa
        if tentativa in self.letras_palavra:
            self.letras_corretas.add(tentativa)
        else:
            self.letras_erradas.add(tentativa)
        
        # Atualiza a interface
        self.atualizar_interface()
        
        # Verifica se o jogo terminou
        self.verificar_fim_jogo()
    
    def verificar_fim_jogo(self):
        """Verifica se o jogo terminou e exibe o resultado"""
        if len(self.letras_erradas) >= self.max_erros:
            # Jogador perdeu
            self.entry_letra.config(state="disabled")
            self.btn_tentar.config(state="disabled")
            self.label_status.config(text="Você perdeu!")
            messagebox.showinfo("Fim de Jogo", f"Você perdeu!\nA palavra era: {self.palavra}")
        
        elif len(self.letras_palavra - self.letras_corretas) == 0:
            # Jogador ganhou
            self.entry_letra.config(state="disabled")
            self.btn_tentar.config(state="disabled")
            self.label_status.config(text="Você ganhou!")
            messagebox.showinfo("Parabéns!", "Você acertou a palavra!")

def main():
    root = tk.Tk()
    jogo = JogoForcaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
