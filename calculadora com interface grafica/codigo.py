import tkinter as tk
from tkinter import messagebox
import math

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("300x440")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        # Variável para armazenar a expressão
        self.expressao = ""
        
        # Criar a interface
        self.criar_interface()
    
    def criar_interface(self):
        # Display da calculadora
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display = tk.Entry(
            self.root,
            textvariable=self.display_var,
            font=("Arial", 20),
            justify="right",
            state="readonly",
            bg="#34495e",
            fg="black",
            bd=0,
            relief="flat"
        )
        display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew", ipady=10)
        
        # Botões da calculadora
        botoes = [
            ('C', 1, 0, '#e74c3c'), ('±', 1, 1, '#95a5a6'), ('√', 1, 2, '#95a5a6'), ('÷', 1, 3, '#f39c12'),
            ('7', 2, 0, '#34495e'), ('8', 2, 1, '#34495e'), ('9', 2, 2, '#34495e'), ('×', 2, 3, '#f39c12'),
            ('4', 3, 0, '#34495e'), ('5', 3, 1, '#34495e'), ('6', 3, 2, '#34495e'), ('-', 3, 3, '#f39c12'),
            ('1', 4, 0, '#34495e'), ('2', 4, 1, '#34495e'), ('3', 4, 2, '#34495e'), ('+', 4, 3, '#f39c12'),
            ('0', 5, 0, '#34495e'), ('.', 5, 1, '#34495e'), ('⌫', 5, 2, '#95a5a6'), ('=', 5, 3, '#27ae60')
        ]
        
        for (texto, linha, coluna, cor) in botoes:
            if texto == '0':
                # Botão 0 ocupa duas colunas
                btn = tk.Button(
                    self.root,
                    text=texto,
                    font=("Arial", 16, "bold"),
                    bg=cor,
                    fg="white",
                    bd=0,
                    relief="flat",
                    command=lambda t=texto: self.clique_botao(t)
                )
                btn.grid(row=linha, column=coluna, columnspan=2, padx=2, pady=2, sticky="ew", ipady=15)
            else:
                btn = tk.Button(
                    self.root,
                    text=texto,
                    font=("Arial", 16, "bold"),
                    bg=cor,
                    fg="white",
                    bd=0,
                    relief="flat",
                    command=lambda t=texto: self.clique_botao(t)
                )
                btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="ew", ipady=15)
        
        # Configurar o grid para ser responsivo
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
    
    def clique_botao(self, valor):
        if valor == 'C':
            self.limpar()
        elif valor == '=':
            self.calcular()
        elif valor == '⌫':
            self.apagar()
        elif valor == '±':
            self.trocar_sinal()
        elif valor == '√':
            self.raiz_quadrada()
        elif valor in ['÷', '×', '+', '-']:
            self.adicionar_operador(valor)
        else:
            self.adicionar_numero(valor)
    
    def limpar(self):
        self.expressao = ""
        self.display_var.set("0")
    
    def apagar(self):
        if self.expressao:
            self.expressao = self.expressao[:-1]
            if self.expressao:
                self.display_var.set(self.expressao)
            else:
                self.display_var.set("0")
    
    def adicionar_numero(self, numero):
        if self.display_var.get() == "0" and numero != ".":
            self.expressao = numero
        else:
            if self.display_var.get() == "0":
                self.expressao = numero
            else:
                self.expressao += numero
        self.display_var.set(self.expressao)
    
    def adicionar_operador(self, operador):
        if self.expressao and self.expressao[-1] not in ['÷', '×', '+', '-']:
            # Converter símbolos para operadores Python
            if operador == '÷':
                self.expressao += '/'
            elif operador == '×':
                self.expressao += '*'
            else:
                self.expressao += operador
            self.display_var.set(self.expressao.replace('/', '÷').replace('*', '×'))
    
    def trocar_sinal(self):
        if self.expressao and self.expressao != "0":
            if self.expressao.startswith('-'):
                self.expressao = self.expressao[1:]
            else:
                self.expressao = '-' + self.expressao
            self.display_var.set(self.expressao.replace('/', '÷').replace('*', '×'))
    
    def raiz_quadrada(self):
        try:
            if self.expressao:
                resultado = math.sqrt(float(self.expressao))
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
        except ValueError:
            messagebox.showerror("Erro", "Não é possível calcular a raiz quadrada de um número negativo")
        except Exception as e:
            messagebox.showerror("Erro", "Erro no cálculo")
    
    def calcular(self):
        try:
            if self.expressao:
                # Avaliar a expressão
                resultado = eval(self.expressao)
                
                # Formatar o resultado
                if isinstance(resultado, float) and resultado.is_integer():
                    resultado = int(resultado)
                
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Divisão por zero não é permitida")
            self.limpar()
        except Exception as e:
            messagebox.showerror("Erro", "Expressão inválida")
            self.limpar()

# Criar e executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    calculadora = Calculadora(root)
    
    print("Calculadora iniciada!")
    print("Funcionalidades disponíveis:")
    print("- Operações básicas: +, -, ×, ÷")
    print("- Raiz quadrada (√)")
    print("- Trocar sinal (±)")
    print("- Limpar (C)")
    print("- Apagar último dígito (⌫)")
    print("- Números decimais (.)")
    
    root.mainloop()
