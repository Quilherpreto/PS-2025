import tkinter as tk
from tkinter import ttk
import pygame
import math
from PIL import Image, ImageTk
import os

# ============================================================================
# 🖼️ CONFIGURE SUA IMAGEM AQUI:
# ============================================================================
CAMINHO_IMAGEM = "/home/guilherme-andrade-mendes/Área de trabalho/DROID/PS-2025/Captura de tela de 2025-08-13 12-04-25.png"  # <- MUDE AQUI! Ex: "minha_foto.jpg"
# ============================================================================

# Frequência correta
FREQ_CORRETA = 101.50

# Inicializa pygame mixer
pygame.mixer.init()

def tocar_audio(caminho):
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play()

class RadioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📻 RÁDIO VINTAGE 📻")
        
        # Configurar tela cheia
        self.root.configure(bg="#1a1a1a")
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))

        # Variável da frequência
        self.freq_var = tk.DoubleVar(value=80.00)
        
        # Criar o rádio visual
        self.criar_radio()

    def criar_radio(self):
        # Frame principal (tela toda)
        self.frame_radio = tk.Frame(self.root, bg="#1a1a1a")
        self.frame_radio.pack(fill=tk.BOTH, expand=True)

        # Canvas para desenhar o rádio (tela toda)
        self.canvas = tk.Canvas(self.frame_radio, bg="#8B4513", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Desenhar corpo do rádio (proporções da tela)
        self.canvas.update()
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 1200
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 800
        
        # Margens proporcionais
        margin_x = w * 0.05  # 5% da largura
        margin_y = h * 0.05  # 5% da altura
        
        self.canvas.create_rectangle(margin_x, margin_y, w-margin_x, h-margin_y, 
                                   fill="#654321", outline="#3d2914", width=8)
        self.canvas.create_rectangle(margin_x+20, margin_y+20, w-margin_x-20, h-margin_y-20, 
                                   fill="#8B4513", outline="#654321", width=4)

        # Desenhar alto-falante (lado esquerdo)
        speaker_x = margin_x + w * 0.08
        speaker_y = margin_y + h * 0.25
        speaker_size = min(w * 0.25, h * 0.35)
        
        self.canvas.create_oval(speaker_x, speaker_y, speaker_x + speaker_size, speaker_y + speaker_size, 
                              fill="#2F4F4F", outline="#1a1a1a", width=6)
        self.canvas.create_oval(speaker_x+20, speaker_y+20, speaker_x + speaker_size-20, speaker_y + speaker_size-20, 
                              fill="#708090", outline="#2F4F4F", width=4)
        
        # Grade do alto-falante
        for i in range(8):
            for j in range(8):
                x = speaker_x + 40 + i * (speaker_size-80) / 8
                y = speaker_y + 40 + j * (speaker_size-80) / 8
                self.canvas.create_oval(x, y, x+4, y+4, fill="#1a1a1a", outline="")

        # Desenhar display da frequência (centro-superior)
        display_x = w * 0.4
        display_y = margin_y + h * 0.15
        display_w = w * 0.35
        display_h = h * 0.08
        
        self.canvas.create_rectangle(display_x, display_y, display_x + display_w, display_y + display_h, 
                                   fill="#000000", outline="#333333", width=3)
        self.canvas.create_rectangle(display_x+10, display_y+10, display_x + display_w-10, display_y + display_h-10, 
                                   fill="#003300", outline="#006600", width=2)
        
        # Texto da frequência no display
        self.freq_display = self.canvas.create_text(display_x + display_w/2, display_y + display_h/2, 
                                                  text="80.00 MHz", font=("Courier", int(h*0.035), "bold"), fill="#00FF00")

        # Desenhar escala de frequência (centro)
        self.scale_x = w * 0.4
        self.scale_y = margin_y + h * 0.35
        self.scale_w = w * 0.35
        self.desenhar_escala()

        # Desenhar ponteiro da frequência
        self.ponteiro = self.desenhar_ponteiro()

        # Desenhar knobs (lado direito)
        knob_x = w * 0.82
        knob_y1 = margin_y + h * 0.3
        knob_y2 = margin_y + h * 0.45
        knob_size = min(w * 0.06, h * 0.08)
        
        self.canvas.create_oval(knob_x, knob_y1, knob_x + knob_size, knob_y1 + knob_size, 
                              fill="#C0C0C0", outline="#696969", width=4)
        self.canvas.create_text(knob_x + knob_size/2, knob_y1 + knob_size/2, 
                              text="VOL", font=("Arial", int(h*0.015), "bold"))

        self.canvas.create_oval(knob_x, knob_y2, knob_x + knob_size, knob_y2 + knob_size, 
                              fill="#C0C0C0", outline="#696969", width=4)
        self.canvas.create_text(knob_x + knob_size/2, knob_y2 + knob_size/2, 
                              text="TONE", font=("Arial", int(h*0.015), "bold"))

        # Desenhar LED de status
        led_x = w * 0.85
        led_y = margin_y + h * 0.65
        led_size = min(w * 0.03, h * 0.04)
        
        self.led = self.canvas.create_oval(led_x, led_y, led_x + led_size, led_y + led_size, 
                                         fill="#FF0000", outline="#8B0000", width=3)
        self.canvas.create_text(led_x + led_size/2, led_y + led_size + 20, 
                              text="POWER", font=("Arial", int(h*0.012), "bold"), fill="white")

        # BOTÃO SINTONIZAR simples como rádio real (botão redondo) - MOVIDO MAIS PARA CIMA
        btn_x = w * 0.45
        btn_y = margin_y + h * 0.6  # Era 0.7, agora é 0.6 (mais para cima)
        btn_size = min(w * 0.08, h * 0.1)
        
        # Criar botão redondo como elemento do canvas
        self.btn_sintonizar = self.canvas.create_oval(btn_x, btn_y, btn_x + btn_size, btn_y + btn_size,
                                                    fill="#FF4500", outline="#8B0000", width=4)
        self.btn_texto = self.canvas.create_text(btn_x + btn_size/2, btn_y + btn_size/2,
                                               text="TUNE",
                                               font=("Arial", int(h*0.02), "bold"), fill="white")
        
        # Bind do clique no botão
        self.canvas.tag_bind(self.btn_sintonizar, "<Button-1>", lambda e: self.verificar_frequencia())
        self.canvas.tag_bind(self.btn_texto, "<Button-1>", lambda e: self.verificar_frequencia())

        # Controles de sintonização integrados
        self.criar_controles_integrados()

    def desenhar_escala(self):
        """Desenha a escala de frequência no rádio"""
        # Escala principal (adaptativa)
        start_x = self.scale_x
        end_x = self.scale_x + self.scale_w
        start_y = self.scale_y
        
        # Linha da escala
        self.canvas.create_line(start_x, start_y, end_x, start_y, fill="white", width=3)
        
        # Marcações da escala
        for freq in range(80, 109, 2):
            x = start_x + (freq - 80) * self.scale_w / 28
            self.canvas.create_line(x, start_y-15, x, start_y+15, fill="white", width=2)
            self.canvas.create_text(x, start_y+30, text=str(freq), font=("Arial", 10), fill="white")

    def desenhar_ponteiro(self):
        """Desenha o ponteiro indicador da frequência"""
        freq = self.freq_var.get()
        start_x = self.scale_x
        start_y = self.scale_y
        
        # Calcular posição do ponteiro
        x = start_x + (freq - 80) * self.scale_w / 28
        
        # Desenhar ponteiro (triângulo)
        return self.canvas.create_polygon(x-8, start_y-25, x+8, start_y-25, x, start_y-5, 
                                        fill="#FF4500", outline="#8B0000", width=2)

    def atualizar_ponteiro(self):
        """Atualiza a posição do ponteiro"""
        freq = self.freq_var.get()
        start_x = self.scale_x
        start_y = self.scale_y
        
        # Calcular nova posição
        x = start_x + (freq - 80) * self.scale_w / 28
        
        # Atualizar ponteiro
        self.canvas.delete(self.ponteiro)
        self.ponteiro = self.canvas.create_polygon(x-8, start_y-25, x+8, start_y-25, x, start_y-5, 
                                                 fill="#FF4500", outline="#8B0000", width=2)

    def criar_controles_integrados(self):
        """Cria controles integrados ao design do rádio"""
        # Usar posições relativas à tela
        w = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 1200
        h = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 800
        
        # Botões de ajuste fino como knobs pequenos na parte inferior
        knob_size = min(w * 0.04, h * 0.05)
        knob_y = h * 0.85
        
        # Posições dos botões de ajuste (com precisão decimal)
        positions = [
            (w * 0.15, "◀◀◀", -1.0, "#8B0000"),
            (w * 0.25, "◀◀", -0.5, "#CD5C5C"),
            (w * 0.35, "◀", -0.1, "#FFA500"),
            (w * 0.45, "◁", -0.01, "#FFD700"),  # Nova precisão decimal
            (w * 0.55, "▷", 0.01, "#FFD700"),   # Nova precisão decimal
            (w * 0.65, "▶", 0.1, "#FFA500"),
            (w * 0.75, "▶▶", 0.5, "#CD5C5C"),
            (w * 0.85, "▶▶▶", 1.0, "#8B0000")
        ]
        
        for x, text, delta, color in positions:
            # Criar knob
            knob = self.canvas.create_oval(x - knob_size/2, knob_y - knob_size/2, 
                                         x + knob_size/2, knob_y + knob_size/2,
                                         fill=color, outline="#333333", width=3)
            
            # Texto do knob
            knob_text = self.canvas.create_text(x, knob_y, text=text, 
                                              font=("Arial", int(h*0.02), "bold"), fill="white")
            
            # Bind dos cliques
            self.canvas.tag_bind(knob, "<Button-1>", lambda e, d=delta: self.ajustar_freq(d))
            self.canvas.tag_bind(knob_text, "<Button-1>", lambda e, d=delta: self.ajustar_freq(d))

        # Slider principal integrado (como uma linha no rádio)
        slider_y = h * 0.55
        slider_x = w * 0.4
        slider_w = w * 0.35
        
        # Linha do slider
        self.canvas.create_line(slider_x, slider_y, slider_x + slider_w, slider_y, 
                              fill="#FFD700", width=6)
        
        # Marcador do slider (círculo que se move)
        freq = self.freq_var.get()
        marker_x = slider_x + (freq - 80) * slider_w / 28
        self.slider_marker = self.canvas.create_oval(marker_x - 8, slider_y - 8, 
                                                   marker_x + 8, slider_y + 8,
                                                   fill="#FF4500", outline="#8B0000", width=3)
        
        # Bind para arrastar o slider
        self.canvas.tag_bind(self.slider_marker, "<B1-Motion>", self.arrastar_slider)
        self.canvas.tag_bind(self.slider_marker, "<Button-1>", self.iniciar_arrasto)
        
        # Variáveis para controle do slider
        self.slider_x = slider_x
        self.slider_y = slider_y
        self.slider_w = slider_w

    def iniciar_arrasto(self, event):
        """Inicia o arrasto do slider"""
        self.arrastar_slider(event)

    def arrastar_slider(self, event):
        """Controla o arrasto do marcador do slider"""
        # Converter coordenadas do evento para posição no slider
        x = self.canvas.canvasx(event.x)
        
        # Limitar à área do slider
        if x < self.slider_x:
            x = self.slider_x
        elif x > self.slider_x + self.slider_w:
            x = self.slider_x + self.slider_w
        
        # Calcular frequência
        freq = 80 + (x - self.slider_x) * 28 / self.slider_w
        
        # Atualizar
        self.freq_var.set(freq)
        self.atualizar_display(freq)
        
        # Mover marcador
        self.canvas.coords(self.slider_marker, x - 8, self.slider_y - 8, x + 8, self.slider_y + 8)

    def ajustar_freq(self, delta):
        """Ajustar frequência com precisão"""
        freq_atual = self.freq_var.get()
        nova_freq = freq_atual + delta
        
        # Limitar entre 80.00 e 108.00
        if 80.00 <= nova_freq <= 108.00:
            self.freq_var.set(nova_freq)
            self.atualizar_display(nova_freq)

    def atualizar_display(self, value):
        """Atualiza o display da frequência e o ponteiro"""
        freq = float(value)
        self.canvas.itemconfig(self.freq_display, text=f"{freq:.2f} MHz")
        self.atualizar_ponteiro()
        
        # Mudar cor do LED baseado na proximidade da frequência correta
        if abs(freq - 101.50) < 0.05:
            self.canvas.itemconfig(self.led, fill="#00FF00")  # Verde se muito próximo
        elif abs(freq - 101.50) < 0.2:
            self.canvas.itemconfig(self.led, fill="#FFFF00")  # Amarelo se próximo
        else:
            self.canvas.itemconfig(self.led, fill="#FF0000")  # Vermelho se longe

    def verificar_frequencia(self):
        freq = round(self.freq_var.get(), 2)
        if freq == FREQ_CORRETA:
            self.tela_morse()

    def tela_morse(self):
        # Limpa tela do rádio
        self.frame_radio.pack_forget()

        # Nova tela (tela cheia também)
        frame_morse = tk.Frame(self.root, bg="#0a0a0a")
        frame_morse.pack(fill=tk.BOTH, expand=True)

        # Canvas para mostrar a imagem personalizada (tela toda)
        self.canvas_morse = tk.Canvas(frame_morse, bg="#000000", highlightthickness=0)
        self.canvas_morse.pack(fill=tk.BOTH, expand=True)

        # Carregar e mostrar sua imagem personalizada
        self.mostrar_imagem_personalizada()

        # Botão para sair (no canto)
        btn_sair = tk.Button(frame_morse, text="🚪 SAIR", command=self.root.quit,
                            font=("Arial", 16, "bold"), bg="red", fg="white", padx=20, pady=10)
        btn_sair.place(x=10, y=10)  # Posicionar no canto superior esquerdo

    def mostrar_imagem_personalizada(self):
        """Mostra sua imagem personalizada ocupando toda a tela"""
        
        # Usar a variável global definida no início do arquivo
        caminho_imagem = CAMINHO_IMAGEM
        
        try:
            # Verificar se o arquivo existe
            if os.path.exists(caminho_imagem):
                # Obter dimensões do canvas (tela toda)
                self.canvas_morse.update()
                canvas_width = self.canvas_morse.winfo_width()
                canvas_height = self.canvas_morse.winfo_height()
                
                # Carregar a imagem
                image = Image.open(caminho_imagem)
                
                # Redimensionar a imagem para ocupar toda a tela mantendo proporção
                image_ratio = image.width / image.height
                canvas_ratio = canvas_width / canvas_height
                
                if image_ratio > canvas_ratio:
                    # Imagem mais larga - ajustar pela largura
                    new_width = canvas_width
                    new_height = int(canvas_width / image_ratio)
                else:
                    # Imagem mais alta - ajustar pela altura
                    new_height = canvas_height
                    new_width = int(canvas_height * image_ratio)
                
                # Redimensionar
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Converter para formato tkinter
                photo = ImageTk.PhotoImage(image)
                
                # Limpar canvas e adicionar imagem centralizada
                self.canvas_morse.delete("all")
                
                # Centralizar imagem na tela
                x = canvas_width // 2
                y = canvas_height // 2
                self.canvas_morse.create_image(x, y, image=photo, anchor="center")
                
                # Manter referência da imagem (importante para tkinter)
                self.canvas_morse.image = photo
                
            else:
                # Se a imagem não existir, mostrar código Morse padrão
                self.desenhar_codigo_morse(self.canvas_morse)
                
        except Exception as e:
            # Se der erro, mostrar código Morse padrão
            self.desenhar_codigo_morse(self.canvas_morse)

    def desenhar_codigo_morse(self, canvas):
        """Desenha código Morse visual para 'PARABÉNS'"""
        # Código Morse para PARABÉNS
        morse_code = {
            'P': '.--.', 'A': '.-', 'R': '.-.', 'B': '-...', 
            'É': '..-..', 'N': '-.', 'S': '...'
        }
        
        y = 200
        x_start = 50
        
        # Título
        canvas.create_text(600, 50, text="CÓDIGO MORSE INTERCEPTADO", 
                          font=("Arial", 24, "bold"), fill="#00FF00")
        
        palavra = "PARABÉNS"
        x = x_start
        
        for letra in palavra:
            if letra in morse_code:
                # Desenhar letra
                canvas.create_text(x, y-60, text=letra, font=("Arial", 20, "bold"), fill="#FFFFFF")
                
                # Desenhar código morse
                codigo = morse_code[letra]
                x_morse = x
                
                for simbolo in codigo:
                    if simbolo == '.':
                        # Ponto (círculo pequeno)
                        canvas.create_oval(x_morse-5, y-5, x_morse+5, y+5, fill="#FFD700", outline="#FF8C00", width=2)
                    elif simbolo == '-':
                        # Traço (retângulo)
                        canvas.create_rectangle(x_morse-15, y-5, x_morse+15, y+5, fill="#FFD700", outline="#FF8C00", width=2)
                    
                    x_morse += 35
                
                x += max(len(codigo) * 35 + 40, 100)
        
        # Desenhar ondas de rádio
        self.desenhar_ondas_radio(canvas)

    def desenhar_ondas_radio(self, canvas):
        """Desenha ondas de rádio animadas"""
        for i in range(5):
            canvas.create_arc(500, 300, 700+i*50, 100+i*50, start=180, extent=180, 
                            outline="#00BFFF", width=3, style="arc")
            canvas.create_arc(500, 300, 700+i*50, 500-i*50, start=0, extent=180, 
                            outline="#00BFFF", width=3, style="arc")

# Criar janela
root = tk.Tk()
app = RadioApp(root)
root.mainloop()
