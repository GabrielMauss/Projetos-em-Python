#Um aplicativo simples de previsão de tempo com interface grafica diretamente conectada com o site OpenWeatherMap.

import sys
import json
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFrame, QGridLayout, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicativo de Clima")
        self.setMinimumSize(500, 500)
        self.setStyleSheet("background-color: #f0f8ff;")
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Título
        title = QLabel("Previsão do Tempo")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title)
        
        # Layout de pesquisa
        search_layout = QHBoxLayout()
        
        # Campo de entrada
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Digite o nome da cidade...")
        self.city_input.setFont(QFont("Arial", 12))
        self.city_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px;
                background-color: white;
            }
        """)
        search_layout.addWidget(self.city_input)
        
        # Botão de pesquisa
        search_button = QPushButton("Buscar")
        search_button.setFont(QFont("Arial", 12, QFont.Bold))
        search_button.setCursor(Qt.PointingHandCursor)
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 10px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        search_button.clicked.connect(self.search_weather)
        search_layout.addWidget(search_button)
        
        main_layout.addLayout(search_layout)
        
        # Frame para os resultados
        self.results_frame = QFrame()
        self.results_frame.setFrameShape(QFrame.StyledPanel)
        self.results_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                margin-top: 20px;
            }
        """)
        self.results_frame.setVisible(False)
        
        results_layout = QVBoxLayout()
        self.results_frame.setLayout(results_layout)
        
        # Cidade e país
        self.location_label = QLabel()
        self.location_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.location_label.setAlignment(Qt.AlignCenter)
        self.location_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        results_layout.addWidget(self.location_label)
        
        # Layout para ícone e temperatura
        temp_layout = QHBoxLayout()
        
        # Ícone do clima
        self.weather_icon = QLabel()
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_icon.setMinimumSize(100, 100)
        temp_layout.addWidget(self.weather_icon)
        
        # Temperatura
        self.temp_label = QLabel()
        self.temp_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("color: #e74c3c;")
        temp_layout.addWidget(self.temp_label)
        
        results_layout.addLayout(temp_layout)
        
        # Descrição do clima
        self.desc_label = QLabel()
        self.desc_label.setFont(QFont("Arial", 14))
        self.desc_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setStyleSheet("color: #7f8c8d; margin-bottom: 10px;")
        results_layout.addWidget(self.desc_label)
        
        # Grid para detalhes adicionais
        details_grid = QGridLayout()
        
        # Sensação térmica
        details_grid.addWidget(QLabel("Sensação térmica:"), 0, 0)
        self.feels_like_label = QLabel()
        self.feels_like_label.setFont(QFont("Arial", 12, QFont.Bold))
        details_grid.addWidget(self.feels_like_label, 0, 1)
        
        # Umidade
        details_grid.addWidget(QLabel("Umidade:"), 1, 0)
        self.humidity_label = QLabel()
        self.humidity_label.setFont(QFont("Arial", 12, QFont.Bold))
        details_grid.addWidget(self.humidity_label, 1, 1)
        
        # Velocidade do vento
        details_grid.addWidget(QLabel("Velocidade do vento:"), 2, 0)
        self.wind_label = QLabel()
        self.wind_label.setFont(QFont("Arial", 12, QFont.Bold))
        details_grid.addWidget(self.wind_label, 2, 1)
        
        # Pressão
        details_grid.addWidget(QLabel("Pressão:"), 3, 0)
        self.pressure_label = QLabel()
        self.pressure_label.setFont(QFont("Arial", 12, QFont.Bold))
        details_grid.addWidget(self.pressure_label, 3, 1)
        
        results_layout.addLayout(details_grid)
        main_layout.addWidget(self.results_frame)
        
        # Conectar o evento Enter no campo de entrada
        self.city_input.returnPressed.connect(search_button.click)
    
    def search_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Erro", "Por favor, digite o nome de uma cidade.")
            return
        
        try:
            # Usando a API OpenWeatherMap (sem chave API para este exemplo)
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=da6b1f8cc0a2c8a73e6e9d8a4f53d1a0&units=metric&lang=pt_br"
            response = requests.get(url)
            
            if response.status_code == 200:
                self.display_weather(response.json())
            else:
                error_message = "Cidade não encontrada. Verifique a ortografia."
                if response.status_code == 401:
                    error_message = "Erro de autenticação na API."
                QMessageBox.warning(self, "Erro", error_message)
        
        except requests.exceptions.RequestException:
            QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao serviço de clima. Verifique sua conexão com a internet.")
    
    def display_weather(self, data):
        # Mostrar o frame de resultados
        self.results_frame.setVisible(True)
        
        # Atualizar os dados
        city = data["name"]
        country = data["sys"]["country"]
        self.location_label.setText(f"{city}, {country}")
        
        # Temperatura
        temp = data["main"]["temp"]
        self.temp_label.setText(f"{temp:.1f}°C")
        
        # Descrição
        description = data["weather"][0]["description"].capitalize()
        self.desc_label.setText(description)
        
        # Ícone (simulado com texto, em um app real usaríamos imagens)
        weather_id = data["weather"][0]["id"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Em um app real, baixaríamos a imagem
        # Para este exemplo, apenas mostramos um texto representativo
        self.weather_icon.setText("☁️")
        self.weather_icon.setFont(QFont("Arial", 48))
        
        # Detalhes adicionais
        feels_like = data["main"]["feels_like"]
        self.feels_like_label.setText(f"{feels_like:.1f}°C")
        
        humidity = data["main"]["humidity"]
        self.humidity_label.setText(f"{humidity}%")
        
        wind_speed = data["wind"]["speed"]
        self.wind_label.setText(f"{wind_speed} m/s")
        
        pressure = data["main"]["pressure"]
        self.pressure_label.setText(f"{pressure} hPa")

# Iniciar a aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
