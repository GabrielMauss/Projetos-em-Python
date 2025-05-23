import requests
import random
import os
import time

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_palavra():
    """Busca uma palavra aleatória da API"""
    try:
        # Usando a API Random Word para obter palavras em inglês
        response = requests.get("https://random-word-api.herokuapp.com/word")
        if response.status_code == 200:
            palavras = response.json()
            return palavras[0].upper()
        else:
            # Palavras de backup caso a API falhe
            palavras_backup = ["PYTHON", "PROGRAMACAO", "COMPUTADOR", "DESENVOLVIMENTO", 
                              "ALGORITMO", "VARIAVEL", "FUNCAO", "CLASSE", "OBJETO"]
            return random.choice(palavras_backup)
    except:
        # Palavras de backup caso a API falhe
        palavras_backup = ["PYTHON", "PROGRAMACAO", "COMPUTADOR", "DESENVOLVIMENTO", 
                          "ALGORITMO", "VARIAVEL", "FUNCAO", "CLASSE", "OBJETO"]
        return random.choice(palavras_backup)

def exibir_forca(erros):
    """Exibe o estado atual da forca baseado no número de erros"""
    estagios = [
        """
           --------
           |      |
           |      
           |    
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |    
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |      |
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |     /|
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |      
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / 
           |     
           -
        """,
        """
           --------
           |      |
           |      O
           |     /|\\
           |     / \\
           |     
           -
        """
    ]
    return estagios[erros]

def exibir_palavra(palavra, letras_corretas):
    """Exibe a palavra com as letras adivinhadas e _ para as não adivinhadas"""
    resultado = ""
    for letra in palavra:
        if letra in letras_corretas:
            resultado += letra + " "
        else:
            resultado += "_ "
    return resultado

def jogar_forca():
    """Função principal do jogo da forca"""
    print("Buscando palavra...")
    palavra = obter_palavra()
    letras_palavra = set(palavra)  # Conjunto de letras únicas na palavra
    letras_corretas = set()  # Letras corretas adivinhadas
    letras_erradas = set()  # Letras erradas adivinhadas
    max_erros = 6  # Número máximo de erros permitidos
    
    # Loop principal do jogo
    while len(letras_erradas) < max_erros and len(letras_palavra - letras_corretas) > 0:
        limpar_tela()
        
        # Exibe o estado atual do jogo
        print("\n=== JOGO DA FORCA ===\n")
        print(exibir_forca(len(letras_erradas)))
        print("\nPalavra: " + exibir_palavra(palavra, letras_corretas))
        print("\nLetras erradas: " + " ".join(letras_erradas))
        print(f"Tentativas restantes: {max_erros - len(letras_erradas)}")
        
        # Solicita uma letra ao jogador
        tentativa = input("\nDigite uma letra: ").upper()
        
        # Valida a entrada
        if len(tentativa) != 1 or not tentativa.isalpha():
            print("Por favor, digite apenas uma letra.")
            time.sleep(1)
            continue
        
        # Verifica se a letra já foi tentada
        if tentativa in letras_corretas or tentativa in letras_erradas:
            print("Você já tentou essa letra!")
            time.sleep(1)
            continue
        
        # Verifica se a letra está na palavra
        if tentativa in letras_palavra:
            letras_corretas.add(tentativa)
            print("Letra correta!")
        else:
            letras_erradas.add(tentativa)
            print("Letra errada!")
        
        time.sleep(0.5)
    
    # Fim do jogo
    limpar_tela()
    print("\n=== JOGO DA FORCA ===\n")
    print(exibir_forca(len(letras_erradas)))
    print("\nPalavra: " + exibir_palavra(palavra, letras_corretas))
    
    # Verifica se o jogador ganhou ou perdeu
    if len(letras_erradas) >= max_erros:
        print(f"\nVocê perdeu! A palavra era: {palavra}")
    else:
        print("\nParabéns! Você acertou a palavra!")
    
    # Pergunta se o jogador quer jogar novamente
    jogar_novamente = input("\nDeseja jogar novamente? (S/N): ").upper()
    if jogar_novamente == "S":
        jogar_forca()

# Inicia o jogo
if __name__ == "__main__":
    print("Bem-vindo ao Jogo da Forca!")
    print("Tente adivinhar a palavra secreta letra por letra.")
    print("Você tem 6 tentativas antes de ser enforcado!")
    input("Pressione Enter para começar...")
    jogar_forca()
