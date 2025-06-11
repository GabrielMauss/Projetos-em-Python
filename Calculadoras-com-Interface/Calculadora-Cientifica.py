#Calculadora Cientifica com varias funções e funcionalidades com interface grafico.


import tkinter as tk
from tkinter import ttk, messagebox
import math
import cmath
import numpy as np
from fractions import Fraction

class CientificCalculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#2c3e50")
        
        # Variáveis para armazenar a expressão e o modo
        self.expressao = ""
        self.modo_radianos = True
        self.memoria = 0
        self.resultado_anterior = 0
        self.modo_complexo = False
        
        # Criar a interface
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Display da calculadora
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display = tk.Entry(
            main_frame,
            textvariable=self.display_var,
            font=("Arial", 20),
            justify="right",
            state="readonly",
            bg="#34495e",
            fg="white",
            bd=0,
            relief="flat"
        )
        display.pack(fill=tk.X, padx=10, pady=10, ipady=10)
        
        # Display secundário para histórico
        self.historico_var = tk.StringVar()
        self.historico_var.set("")
        
        historico = tk.Entry(
            main_frame,
            textvariable=self.historico_var,
            font=("Arial", 12),
            justify="right",
            state="readonly",
            bg="#34495e",
            fg="#95a5a6",
            bd=0,
            relief="flat"
        )
        historico.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=5)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Estilo para o notebook
        style = ttk.Style()
        style.configure("TNotebook", background="#2c3e50", borderwidth=0)
        style.configure("TNotebook.Tab", background="#34495e", foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "#27ae60")])
        
        # Abas
        self.tab_basica = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_cientifica = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_trigonometrica = tk.Frame(self.notebook, bg="#2c3e50")
        self.tab_avancada = tk.Frame(self.notebook, bg="#2c3e50")
        
        self.notebook.add(self.tab_basica, text="Básica")
        self.notebook.add(self.tab_cientifica, text="Científica")
        self.notebook.add(self.tab_trigonometrica, text="Trigonometria")
        self.notebook.add(self.tab_avancada, text="Avançada")
        
        # Criar botões para cada aba
        self.criar_aba_basica()
        self.criar_aba_cientifica()
        self.criar_aba_trigonometrica()
        self.criar_aba_avancada()
        
        # Barra de status
        self.status_frame = tk.Frame(main_frame, bg="#2c3e50", height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        
        # Indicador de modo (radianos/graus)
        self.modo_var = tk.StringVar()
        self.modo_var.set("RAD" if self.modo_radianos else "DEG")
        
        self.modo_label = tk.Label(
            self.status_frame,
            textvariable=self.modo_var,
            bg="#2c3e50",
            fg="#27ae60",
            font=("Arial", 10, "bold")
        )
        self.modo_label.pack(side=tk.LEFT, padx=5)
        
        # Indicador de modo complexo
        self.complexo_var = tk.StringVar()
        self.complexo_var.set("REAL")
        
        self.complexo_label = tk.Label(
            self.status_frame,
            textvariable=self.complexo_var,
            bg="#2c3e50",
            fg="#e74c3c",
            font=("Arial", 10, "bold")
        )
        self.complexo_label.pack(side=tk.RIGHT, padx=5)
    
    def criar_aba_basica(self):
        botoes = [
            ('C', 0, 0, '#e74c3c'), ('±', 0, 1, '#95a5a6'), ('√', 0, 2, '#95a5a6'), ('÷', 0, 3, '#f39c12'),
            ('7', 1, 0, '#34495e'), ('8', 1, 1, '#34495e'), ('9', 1, 2, '#34495e'), ('×', 1, 3, '#f39c12'),
            ('4', 2, 0, '#34495e'), ('5', 2, 1, '#34495e'), ('6', 2, 2, '#34495e'), ('-', 2, 3, '#f39c12'),
            ('1', 3, 0, '#34495e'), ('2', 3, 1, '#34495e'), ('3', 3, 2, '#34495e'), ('+', 3, 3, '#f39c12'),
            ('0', 4, 0, '#34495e'), ('.', 4, 1, '#34495e'), ('⌫', 4, 2, '#95a5a6'), ('=', 4, 3, '#27ae60')
        ]
        
        for (texto, linha, coluna, cor) in botoes:
            btn = tk.Button(
                self.tab_basica,
                text=texto,
                font=("Arial", 16, "bold"),
                bg=cor,
                fg="white",
                bd=0,
                relief="flat",
                command=lambda t=texto: self.clique_botao(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew", ipady=15)
        
        # Configurar o grid para ser responsivo
        for i in range(5):
            self.tab_basica.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.tab_basica.grid_columnconfigure(i, weight=1)
    
    def criar_aba_cientifica(self):
        botoes = [
            ('x²', 0, 0, '#95a5a6'), ('x³', 0, 1, '#95a5a6'), ('xʸ', 0, 2, '#95a5a6'), ('eˣ', 0, 3, '#95a5a6'), ('10ˣ', 0, 4, '#95a5a6'),
            ('log', 1, 0, '#95a5a6'), ('ln', 1, 1, '#95a5a6'), ('(', 1, 2, '#95a5a6'), (')', 1, 3, '#95a5a6'), ('n!', 1, 4, '#95a5a6'),
            ('1/x', 2, 0, '#95a5a6'), ('|x|', 2, 1, '#95a5a6'), ('π', 2, 2, '#95a5a6'), ('e', 2, 3, '#95a5a6'), ('mod', 2, 4, '#95a5a6'),
            ('MC', 3, 0, '#3498db'), ('MR', 3, 1, '#3498db'), ('M+', 3, 2, '#3498db'), ('M-', 3, 3, '#3498db'), ('MS', 3, 4, '#3498db'),
            ('RAD/DEG', 4, 0, '#27ae60'), ('FRAC', 4, 1, '#27ae60'), ('COMP', 4, 2, '#27ae60'), ('ANS', 4, 3, '#27ae60'), ('RND', 4, 4, '#27ae60')
        ]
        
        for (texto, linha, coluna, cor) in botoes:
            btn = tk.Button(
                self.tab_cientifica,
                text=texto,
                font=("Arial", 14, "bold"),
                bg=cor,
                fg="white",
                bd=0,
                relief="flat",
                command=lambda t=texto: self.clique_botao_cientifico(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew", ipady=10)
        
        # Configurar o grid para ser responsivo
        for i in range(5):
            self.tab_cientifica.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.tab_cientifica.grid_columnconfigure(i, weight=1)
    
    def criar_aba_trigonometrica(self):
        botoes = [
            ('sin', 0, 0, '#95a5a6'), ('cos', 0, 1, '#95a5a6'), ('tan', 0, 2, '#95a5a6'),
            ('asin', 1, 0, '#95a5a6'), ('acos', 1, 1, '#95a5a6'), ('atan', 1, 2, '#95a5a6'),
            ('sinh', 2, 0, '#95a5a6'), ('cosh', 2, 1, '#95a5a6'), ('tanh', 2, 2, '#95a5a6'),
            ('asinh', 3, 0, '#95a5a6'), ('acosh', 3, 1, '#95a5a6'), ('atanh', 3, 2, '#95a5a6'),
            ('sec', 0, 3, '#95a5a6'), ('csc', 1, 3, '#95a5a6'), ('cot', 2, 3, '#95a5a6'),
            ('asec', 0, 4, '#95a5a6'), ('acsc', 1, 4, '#95a5a6'), ('acot', 2, 4, '#95a5a6'),
            ('→DEG', 3, 3, '#27ae60'), ('→RAD', 3, 4, '#27ae60')
        ]
        
        for (texto, linha, coluna, cor) in botoes:
            btn = tk.Button(
                self.tab_trigonometrica,
                text=texto,
                font=("Arial", 14, "bold"),
                bg=cor,
                fg="white",
                bd=0,
                relief="flat",
                command=lambda t=texto: self.clique_botao_trigonometrico(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew", ipady=15)
        
        # Configurar o grid para ser responsivo
        for i in range(4):
            self.tab_trigonometrica.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.tab_trigonometrica.grid_columnconfigure(i, weight=1)
    
    def criar_aba_avancada(self):
        # Frame para matrizes e vetores
        matriz_frame = tk.LabelFrame(self.tab_avancada, text="Matrizes e Vetores", bg="#2c3e50", fg="white", font=("Arial", 12))
        matriz_frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        botoes_matriz = [
            ('Det', 0, 0), ('Inv', 0, 1), ('Transp', 0, 2), ('Eigen', 0, 3),
            ('Dot', 1, 0), ('Cross', 1, 1), ('Norm', 1, 2), ('Solve', 1, 3)
        ]
        
        for (texto, linha, coluna) in botoes_matriz:
            btn = tk.Button(
                matriz_frame,
                text=texto,
                font=("Arial", 12, "bold"),
                bg="#3498db",
                fg="white",
                bd=0,
                relief="flat",
                command=lambda t=texto: self.clique_botao_matriz(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew", ipady=10)
        
        # Frame para estatística
        estat_frame = tk.LabelFrame(self.tab_avancada, text="Estatística", bg="#2c3e50", fg="white", font=("Arial", 12))
        estat_frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        botoes_estat = [
            ('Mean', 0, 0), ('Median', 0, 1), ('Std', 0, 2), ('Var', 0, 3),
            ('Min', 1, 0), ('Max', 1, 1), ('Sum', 1, 2), ('Count', 1, 3)
        ]
        
        for (texto, linha, coluna) in botoes_estat:
            btn = tk.Button(
                estat_frame,
                text=texto,
                font=("Arial", 12, "bold"),
                bg="#9b59b6",
                fg="white",
                bd=0,
                relief="flat",
                command=lambda t=texto: self.clique_botao_estatistico(t)
            )
            btn.grid(row=linha, column=coluna, padx=2, pady=2, sticky="nsew", ipady=10)
        
        # Frame para conversão de unidades
        conv_frame = tk.LabelFrame(self.tab_avancada, text="Conversão de Unidades", bg="#2c3e50", fg="white", font=("Arial", 12))
        conv_frame.pack(fill=tk.X, padx=5, pady=5, ipady=5)
        
        # Dropdown para tipo de conversão
        self.tipo_conv = tk.StringVar()
        self.tipo_conv.set("Comprimento")
        
        tipos = ["Comprimento", "Massa", "Temperatura", "Tempo", "Área", "Volume"]
        
        tipo_label = tk.Label(conv_frame, text="Tipo:", bg="#2c3e50", fg="white", font=("Arial", 12))
        tipo_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        tipo_menu = ttk.Combobox(conv_frame, textvariable=self.tipo_conv, values=tipos, state="readonly", width=15)
        tipo_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tipo_menu.bind("<<ComboboxSelected>>", self.atualizar_unidades)
        
        # Dropdown para unidade de origem
        self.unidade_de = tk.StringVar()
        self.unidade_de.set("metro")
        
        de_label = tk.Label(conv_frame, text="De:", bg="#2c3e50", fg="white", font=("Arial", 12))
        de_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.de_menu = ttk.Combobox(conv_frame, textvariable=self.unidade_de, state="readonly", width=15)
        self.de_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Dropdown para unidade de destino
        self.unidade_para = tk.StringVar()
        self.unidade_para.set("centímetro")
        
        para_label = tk.Label(conv_frame, text="Para:", bg="#2c3e50", fg="white", font=("Arial", 12))
        para_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        
        self.para_menu = ttk.Combobox(conv_frame, textvariable=self.unidade_para, state="readonly", width=15)
        self.para_menu.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Botão de conversão
        converter_btn = tk.Button(
            conv_frame,
            text="Converter",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            bd=0,
            relief="flat",
            command=self.converter_unidade
        )
        converter_btn.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew", ipady=5)
        
        # Inicializar as unidades
        self.atualizar_unidades()
        
        # Configurar o grid para ser responsivo
        for i in range(2):
            matriz_frame.grid_rowconfigure(i, weight=1)
            estat_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            matriz_frame.grid_columnconfigure(i, weight=1)
            estat_frame.grid_columnconfigure(i, weight=1)
            conv_frame.grid_columnconfigure(i, weight=1)
    
    def atualizar_unidades(self, event=None):
        tipo = self.tipo_conv.get()
        
        unidades = {
            "Comprimento": ["metro", "centímetro", "milímetro", "quilômetro", "polegada", "pé", "jarda", "milha"],
            "Massa": ["grama", "quilograma", "miligrama", "tonelada", "libra", "onça"],
            "Temperatura": ["Celsius", "Fahrenheit", "Kelvin"],
            "Tempo": ["segundo", "minuto", "hora", "dia", "semana", "mês", "ano"],
            "Área": ["metro²", "centímetro²", "quilômetro²", "hectare", "acre", "polegada²", "pé²"],
            "Volume": ["metro³", "centímetro³", "litro", "mililitro", "galão", "onça fluida"]
        }
        
        self.de_menu['values'] = unidades[tipo]
        self.para_menu['values'] = unidades[tipo]
        
        self.unidade_de.set(unidades[tipo][0])
        self.unidade_para.set(unidades[tipo][1])
    
    def converter_unidade(self):
        try:
            valor = float(self.display_var.get())
            tipo = self.tipo_conv.get()
            de = self.unidade_de.get()
            para = self.unidade_para.get()
            
            # Converter para unidade base
            if tipo == "Comprimento":
                # Converter para metros
                fatores = {
                    "metro": 1,
                    "centímetro": 0.01,
                    "milímetro": 0.001,
                    "quilômetro": 1000,
                    "polegada": 0.0254,
                    "pé": 0.3048,
                    "jarda": 0.9144,
                    "milha": 1609.34
                }
                valor_base = valor * fatores[de]
                resultado = valor_base / fatores[para]
            
            elif tipo == "Massa":
                # Converter para gramas
                fatores = {
                    "grama": 1,
                    "quilograma": 1000,
                    "miligrama": 0.001,
                    "tonelada": 1000000,
                    "libra": 453.592,
                    "onça": 28.3495
                }
                valor_base = valor * fatores[de]
                resultado = valor_base / fatores[para]
            
            elif tipo == "Temperatura":
                # Conversões especiais para temperatura
                if de == "Celsius" and para == "Fahrenheit":
                    resultado = (valor * 9/5) + 32
                elif de == "Celsius" and para == "Kelvin":
                    resultado = valor + 273.15
                elif de == "Fahrenheit" and para == "Celsius":
                    resultado = (valor - 32) * 5/9
                elif de == "Fahrenheit" and para == "Kelvin":
                    resultado = (valor - 32) * 5/9 + 273.15
                elif de == "Kelvin" and para == "Celsius":
                    resultado = valor - 273.15
                elif de == "Kelvin" and para == "Fahrenheit":
                    resultado = (valor - 273.15) * 9/5 + 32
                else:
                    resultado = valor  # Mesma unidade
            
            elif tipo == "Tempo":
                # Converter para segundos
                fatores = {
                    "segundo": 1,
                    "minuto": 60,
                    "hora": 3600,
                    "dia": 86400,
                    "semana": 604800,
                    "mês": 2592000,  # Aproximadamente 30 dias
                    "ano": 31536000  # Aproximadamente 365 dias
                }
                valor_base = valor * fatores[de]
                resultado = valor_base / fatores[para]
            
            elif tipo == "Área":
                # Converter para metros quadrados
                fatores = {
                    "metro²": 1,
                    "centímetro²": 0.0001,
                    "quilômetro²": 1000000,
                    "hectare": 10000,
                    "acre": 4046.86,
                    "polegada²": 0.00064516,
                    "pé²": 0.092903
                }
                valor_base = valor * fatores[de]
                resultado = valor_base / fatores[para]
            
            elif tipo == "Volume":
                # Converter para metros cúbicos
                fatores = {
                    "metro³": 1,
                    "centímetro³": 0.000001,
                    "litro": 0.001,
                    "mililitro": 0.000001,
                    "galão": 0.00378541,
                    "onça fluida": 0.0000295735
                }
                valor_base = valor * fatores[de]
                resultado = valor_base / fatores[para]
            
            # Atualizar o display
            self.expressao = str(resultado)
            self.display_var.set(self.expressao)
            self.historico_var.set(f"{valor} {de} = {resultado} {para}")
            
            # Armazenar o resultado
            self.resultado_anterior = resultado
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na conversão: {str(e)}")
    
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
    
    def clique_botao_cientifico(self, valor):
        if valor == 'x²':
            self.potencia(2)
        elif valor == 'x³':
            self.potencia(3)
        elif valor == 'xʸ':
            self.adicionar_operador('^')
        elif valor == 'eˣ':
            self.exponencial('e')
        elif valor == '10ˣ':
            self.exponencial('10')
        elif valor == 'log':
            self.logaritmo(10)
        elif valor == 'ln':
            self.logaritmo(math.e)
        elif valor == '(':
            self.adicionar_numero('(')
        elif valor == ')':
            self.adicionar_numero(')')
        elif valor == 'n!':
            self.fatorial()
        elif valor == '1/x':
            self.inverso()
        elif valor == '|x|':
            self.valor_absoluto()
        elif valor == 'π':
            self.adicionar_constante(math.pi)
        elif valor == 'e':
            self.adicionar_constante(math.e)
        elif valor == 'mod':
            self.adicionar_operador('%')
        elif valor == 'MC':
            self.memoria = 0
        elif valor == 'MR':
            self.adicionar_numero(str(self.memoria))
        elif valor == 'M+':
            try:
                self.memoria += float(self.display_var.get())
            except:
                pass
        elif valor == 'M-':
            try:
                self.memoria -= float(self.display_var.get())
            except:
                pass
        elif valor == 'MS':
            try:
                self.memoria = float(self.display_var.get())
            except:
                pass
        elif valor == 'RAD/DEG':
            self.modo_radianos = not self.modo_radianos
            self.modo_var.set("RAD" if self.modo_radianos else "DEG")
        elif valor == 'FRAC':
            self.converter_fracao()
        elif valor == 'COMP':
            self.modo_complexo = not self.modo_complexo
            self.complexo_var.set("COMPLEXO" if self.modo_complexo else "REAL")
        elif valor == 'ANS':
            self.adicionar_numero(str(self.resultado_anterior))
        elif valor == 'RND':
            import random
            self.adicionar_numero(str(random.random()))
    
    def clique_botao_trigonometrico(self, valor):
        if valor in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                    'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
                    'sec', 'csc', 'cot', 'asec', 'acsc', 'acot']:
            self.funcao_trigonometrica(valor)
        elif valor == '→DEG':
            try:
                # Converter de radianos para graus
                valor = float(self.display_var.get())
                resultado = math.degrees(valor)
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{valor} rad = {resultado}°")
            except:
                messagebox.showerror("Erro", "Valor inválido para conversão")
        elif valor == '→RAD':
            try:
                # Converter de graus para radianos
                valor = float(self.display_var.get())
                resultado = math.radians(valor)
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{valor}° = {resultado} rad")
            except:
                messagebox.showerror("Erro", "Valor inválido para conversão")
    
    def clique_botao_matriz(self, valor):
        # Estas funções exigiriam uma interface mais complexa para entrada de matrizes
        # Por simplicidade, vamos apenas mostrar uma mensagem
        messagebox.showinfo("Matriz/Vetor", f"Função {valor} selecionada. Esta função requer entrada de matriz/vetor.")
        
        # Em uma implementação completa, você abriria uma janela para entrada de matriz
        # e então aplicaria a função selecionada
    
    def clique_botao_estatistico(self, valor):
        # Solicitar entrada de dados
        dialog = tk.Toplevel(self.root)
        dialog.title("Entrada de Dados")
        dialog.geometry("400x200")
        dialog.configure(bg="#2c3e50")
        
        tk.Label(dialog, text="Digite os valores separados por vírgula:", bg="#2c3e50", fg="white", font=("Arial", 12)).pack(pady=10)
        
        entrada = tk.Text(dialog, height=5, width=40, bg="#34495e", fg="white", font=("Arial", 12))
        entrada.pack(pady=10, padx=10)
        
        def calcular_estatistica():
            try:
                texto = entrada.get("1.0", tk.END).strip()
                valores = [float(x.strip()) for x in texto.split(",")]
                
                if not valores:
                    messagebox.showerror("Erro", "Nenhum valor fornecido")
                    return
                
                resultado = None
                
                if valor == "Mean":
                    resultado = np.mean(valores)
                    descricao = "Média"
                elif valor == "Median":
                    resultado = np.median(valores)
                    descricao = "Mediana"
                elif valor == "Std":
                    resultado = np.std(valores)
                    descricao = "Desvio Padrão"
                elif valor == "Var":
                    resultado = np.var(valores)
                    descricao = "Variância"
                elif valor == "Min":
                    resultado = np.min(valores)
                    descricao = "Mínimo"
                elif valor == "Max":
                    resultado = np.max(valores)
                    descricao = "Máximo"
                elif valor == "Sum":
                    resultado = np.sum(valores)
                    descricao = "Soma"
                elif valor == "Count":
                    resultado = len(valores)
                    descricao = "Contagem"
                
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{descricao} de {len(valores)} valores = {resultado}")
                self.resultado_anterior = resultado
                
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
        
        tk.Button(
            dialog,
            text="Calcular",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            bd=0,
            relief="flat",
            command=calcular_estatistica
        ).pack(pady=10)
    
    def limpar(self):
        self.expressao = ""
        self.display_var.set("0")
        self.historico_var.set("")
    
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
            if self.display_var.get() == "0" and numero != ".":
                self.expressao = numero
            else:
                self.expressao += numero
        self.display_var.set(self.expressao)
    
    def adicionar_operador(self, operador):
        if self.expressao and self.expressao[-1] not in ['/', '*', '+', '-', '%', '^']:
            # Converter símbolos para operadores Python
            if operador == '÷':
                self.expressao += '/'
            elif operador == '×':
                self.expressao += '*'
            elif operador == '^':
                self.expressao += '**'
            else:
                self.expressao += operador
            self.display_var.set(self.expressao.replace('/', '÷').replace('*', '×').replace('**', '^'))
    
    def trocar_sinal(self):
        if self.expressao and self.expressao != "0":
            if self.expressao.startswith('-'):
                self.expressao = self.expressao[1:]
            else:
                self.expressao = '-' + self.expressao
            self.display_var.set(self.expressao.replace('/', '÷').replace('*', '×').replace('**', '^'))
    
    def raiz_quadrada(self):
        try:
            if self.expressao:
                if self.modo_complexo:
                    valor = complex(self.expressao)
                    resultado = cmath.sqrt(valor)
                    self.expressao = str(resultado).replace('(', '').replace(')', '')
                else:
                    valor = float(self.expressao)
                    if valor < 0:
                        messagebox.showerror("Erro", "Não é possível calcular a raiz quadrada de um número negativo no modo real")
                        return
                    resultado = math.sqrt(valor)
                    self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"√({valor}) = {resultado}")
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def potencia(self, expoente):
        try:
            if self.expressao:
                if self.modo_complexo:
                    valor = complex(self.expressao)
                    resultado = valor ** expoente
                    self.expressao = str(resultado).replace('(', '').replace(')', '')
                else:
                    valor = float(self.expressao)
                    resultado = valor ** expoente
                    self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{valor}^{expoente} = {resultado}")
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def exponencial(self, base):
        try:
            if self.expressao:
                valor = float(self.expressao)
                if base == 'e':
                    resultado = math.exp(valor)
                    self.historico_var.set(f"e^{valor} = {resultado}")
                else:
                    resultado = 10 ** valor
                    self.historico_var.set(f"10^{valor} = {resultado}")
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def logaritmo(self, base):
        try:
            if self.expressao:
                valor = float(self.expressao)
                if valor <= 0:
                    messagebox.showerror("Erro", "Logaritmo não definido para valores não positivos")
                    return
                if base == math.e:
                    resultado = math.log(valor)
                    self.historico_var.set(f"ln({valor}) = {resultado}")
                else:
                    resultado = math.log10(valor)
                    self.historico_var.set(f"log({valor}) = {resultado}")
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def fatorial(self):
        try:
            if self.expressao:
                valor = float(self.expressao)
                if valor < 0 or not valor.is_integer():
                    messagebox.showerror("Erro", "Fatorial só é definido para inteiros não negativos")
                    return
                valor = int(valor)
                resultado = math.factorial(valor)
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{valor}! = {resultado}")
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def inverso(self):
        try:
            if self.expressao:
                if self.modo_complexo:
                    valor = complex(self.expressao)
                    if valor == 0:
                        messagebox.showerror("Erro", "Divisão por zero")
                        return
                    resultado = 1 / valor
                    self.expressao = str(resultado).replace('(', '').replace(')', '')
                else:
                    valor = float(self.expressao)
                    if valor == 0:
                        messagebox.showerror("Erro", "Divisão por zero")
                        return
                    resultado = 1 / valor
                    self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"1/{valor} = {resultado}")
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def valor_absoluto(self):
        try:
            if self.expressao:
                if self.modo_complexo:
                    valor = complex(self.expressao)
                    resultado = abs(valor)
                    self.expressao = str(resultado)
                else:
                    valor = float(self.expressao)
                    resultado = abs(valor)
                    self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"|{valor}| = {resultado}")
                self.resultado_anterior = resultado
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def adicionar_constante(self, constante):
        self.expressao = str(constante)
        self.display_var.set(self.expressao)
    
    def converter_fracao(self):
        try:
            if self.expressao:
                valor = float(self.expressao)
                fracao = Fraction(valor).limit_denominator()
                self.expressao = str(fracao)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{valor} = {fracao}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na conversão: {str(e)}")
    
    def funcao_trigonometrica(self, funcao):
        try:
            if self.expressao:
                valor = float(self.expressao)
                
                # Converter para radianos se estiver em graus
                if not self.modo_radianos:
                    valor_rad = math.radians(valor)
                else:
                    valor_rad = valor
                
                # Funções trigonométricas básicas
                if funcao == 'sin':
                    resultado = math.sin(valor_rad)
                elif funcao == 'cos':
                    resultado = math.cos(valor_rad)
                elif funcao == 'tan':
                    resultado = math.tan(valor_rad)
                elif funcao == 'asin':
                    if valor < -1 or valor > 1:
                        messagebox.showerror("Erro", "Valor fora do domínio [-1, 1]")
                        return
                    resultado = math.asin(valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                elif funcao == 'acos':
                    if valor < -1 or valor > 1:
                        messagebox.showerror("Erro", "Valor fora do domínio [-1, 1]")
                        return
                    resultado = math.acos(valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                elif funcao == 'atan':
                    resultado = math.atan(valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                
                # Funções hiperbólicas
                elif funcao == 'sinh':
                    resultado = math.sinh(valor_rad)
                elif funcao == 'cosh':
                    resultado = math.cosh(valor_rad)
                elif funcao == 'tanh':
                    resultado = math.tanh(valor_rad)
                elif funcao == 'asinh':
                    resultado = math.asinh(valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                elif funcao == 'acosh':
                    if valor < 1:
                        messagebox.showerror("Erro", "Valor fora do domínio [1, ∞)")
                        return
                    resultado = math.acosh(valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                elif funcao == 'atanh':
                    if valor <= -1 or valor >= 1:
                        messagebox.showerror("Erro", "Valor fora do domínio (-1, 1)")
                        return
                    resultado = math.atanh(valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                
                # Funções trigonométricas adicionais
                elif funcao == 'sec':
                    resultado = 1 / math.cos(valor_rad)
                elif funcao == 'csc':
                    resultado = 1 / math.sin(valor_rad)
                elif funcao == 'cot':
                    resultado = 1 / math.tan(valor_rad)
                elif funcao == 'asec':
                    if -1 <= valor <= 1:
                        messagebox.showerror("Erro", "Valor fora do domínio (-∞, -1] ∪ [1, ∞)")
                        return
                    resultado = math.acos(1 / valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                elif funcao == 'acsc':
                    if -1 <= valor <= 1:
                        messagebox.showerror("Erro", "Valor fora do domínio (-∞, -1] ∪ [1, ∞)")
                        return
                    resultado = math.asin(1 / valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                elif funcao == 'acot':
                    resultado = math.atan(1 / valor)
                    if not self.modo_radianos:
                        resultado = math.degrees(resultado)
                
                self.expressao = str(resultado)
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{funcao}({valor}) = {resultado}")
                self.resultado_anterior = resultado
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cálculo: {str(e)}")
    
    def calcular(self):
        try:
            if self.expressao:
                # Substituir operadores para avaliação
                expr_eval = self.expressao.replace('÷', '/').replace('×', '*').replace('^', '**')
                
                if self.modo_complexo:
                    # Tentar avaliar como número complexo
                    try:
                        # Verificar se há números complexos na expressão
                        if 'j' in expr_eval:
                            resultado = eval(expr_eval)
                        else:
                            # Avaliar normalmente e converter para string
                            resultado = eval(expr_eval)
                    except:
                        messagebox.showerror("Erro", "Expressão complexa inválida")
                        return
                else:
                    # Avaliar normalmente
                    resultado = eval(expr_eval)
                
                # Formatar o resultado
                if isinstance(resultado, complex):
                    self.expressao = str(resultado).replace('(', '').replace(')', '')
                else:
                    if isinstance(resultado, float) and resultado.is_integer():
                        resultado = int(resultado)
                    self.expressao = str(resultado)
                
                self.display_var.set(self.expressao)
                self.historico_var.set(f"{expr_eval.replace('**', '^')} = {resultado}")
                self.resultado_anterior = resultado
                
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Divisão por zero não é permitida")
            self.limpar()
        except Exception as e:
            messagebox.showerror("Erro", f"Expressão inválida: {str(e)}")
            self.limpar()

# Criar e executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    calculadora = CientificCalculadora(root)
    
    print("Calculadora Científica iniciada!")
    print("Funcionalidades disponíveis:")
    print("- Operações básicas: +, -, ×, ÷")
    print("- Funções trigonométricas: sin, cos, tan, etc.")
    print("- Funções logarítmicas e exponenciais")
    print("- Funções estatísticas")
    print("- Conversão de unidades")
    print("- Suporte a números complexos")
    print("- Frações e constantes matemáticas")
    
    root.mainloop()
