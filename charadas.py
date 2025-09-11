from tkinter import *
from tkinter import messagebox

root = Tk()
root.configure(bg="black") 
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Variáveis para armazenar as perguntas e respostas
questions = [
    "Charada 1:\n\nVocê tem 3 caixas: uma com bolas vermelhas, uma com bolas azuis, e uma com bolas mistas (vermelhas e azuis).\n\nTodas as etiquetas das caixas estão trocadas.\n\nVocê pode tirar apenas 1 bola de uma caixa para descobrir o conteúdo de todas.\n\nDe qual caixa você deve tirar?\n\nResponda: vermelhas, azuis ou mistas\n\nIMPORTANTE: Responda em letras minúsculas!",
    "Charada 2:\n\nObserve atentamente esta sequência numérica:\n\n1, 4, 9, 16, 25, __ ?\n\nQual é o próximo número e por quê?\n\nResponda apenas o número que completa a sequência.",
    "Charada 3:\n\nUm pai tem 32 anos e seu filho tem 8 anos.\n\nEm quantos anos a idade do pai será o dobro da idade do filho?\n\nResponda apenas o número de anos.",
    "Charada 4:\n\nJuntos, um Mago, um Cavalheiro, um Bárbaro e um Príncipe receberam 70 Esmeraldas.\n\nCada um recebeu um número inteiro de Esmeraldas e cada um recebeu pelo menos um.\n\nO Mago recebeu mais do que cada um dos outros.\n\nO Cavalheiro e o Bárbaro receberam, juntos, 45 Esmeraldas.\n\nQuantas Esmeraldas sobraram para o Príncipe?",
    "Charada 5:\n\n*Essa é a coisa que a tudo devora*\n\n*Feras, aves, plantas, flora.*\n\n*Aço e ferro são sua comida,*\n\n*E a dura pedra por ele moída;*\n\n*Aos reis abate, à cidade arruína,*\n\n*E a alta montanha faz pequenina.*\n\nIMPORTANTE: Responda em letras minúsculas!",
    "Charada 6:\n\n*Não se pode ver, não se pode sentir,*\n\n*Não se pode cheirar, não se pode ouvir.*\n\n*Está sob as colinas e além das estrelas,*\n\n*Cavidades vazias – ele vai enchê-las.*\n\n*De tudo vem antes e vem em seguida,*\n\n*Do riso é a morte, é o fim da vida.*\n\nIMPORTANTE: Responda em letras minúsculas!",
    "DESAFIO FINAL - XADREZ:\n\nPARABÉNS! Você decifrou todos os enigmas do templo!\n\nAgora, para escapar definitivamente, você deve resolver o último mistério:\n\nO TABULEIRO DE XADREZ na sala contém a chave final.\n\nExamine-o cuidadosamente e encontre o CÓDIGO SECRETO.\n\nQuando descobrir, digite-o aqui para prosseguir.\n\n(Procure nas peças, no tabuleiro ou ao redor dele)",
]

answers = [
    "mistas",  # Charada 1 - Problema das caixas com bolas (FÁCIL)
    "36",      # Charada 2 - Sequência dos quadrados perfeitos (FÁCIL-MÉDIO)
    "16",      # Charada 3 - Problema das idades (MÉDIO)
    "1",       # Charada 4 - Esmeraldas do Príncipe (MÉDIO-DIFÍCIL)
    "tempo",   # Charada 5 - O Hobbit (DIFÍCIL)
    "escuro",  # Charada 6 - O Hobbit (DIFÍCIL)
    "XADREZ2025",  # Desafio Final - Código do tabuleiro de xadrez
]

# Índice da pergunta atual
question_index = 0

# Variável para controlar se o jogo foi iniciado
game_started = False

# Variável para contar erros na pergunta atual
errors_count = 0

# Variável para armazenar o tempo restante
time_left = 2400  # 40 minutos

# Função para descontar tempo baseado na dificuldade
def discount_time():
    global time_left
    
    # Não permitir no desafio do xadrez (última pergunta)
    if question_index == len(questions) - 1:
        messagebox.showinfo("Desafio Final", "Não é possível usar oráculos no desafio final! Examine o tabuleiro de xadrez na sala.")
        return
    
    # Definir desconto baseado na dificuldade
    if question_index <= 1:  # Charadas 1-2 (FÁCEIS)
        discount = 300  # 5 minutos
        oracle_type = "Oráculo Simples"
    elif question_index <= 3:  # Charadas 3-4 (MÉDIAS)
        discount = 180  # 3 minutos
        oracle_type = "Oráculo Complexo"
    else:  # Charadas 5-6 (DIFÍCEIS)
        discount = 120  # 2 minutos
        oracle_type = "Oráculo Supremo"
    
    # Aplicar desconto
    time_left -= discount
    
    # Desabilitar o botão após usar a única dica
    help_button.config(state=DISABLED, bg="gray")
    
    messagebox.showinfo("Oráculo Invocado", f"🔮 {oracle_type}\nPreço: -{discount//60} minutos")

# Função para atualizar o temporizador
def update_timer():
    global time_left
    # Só atualizar se o jogo foi iniciado
    if not game_started:
        return
        
    # Se ainda houver tempo restante, diminuir o tempo e atualizar o rótulo do temporizador
    if time_left > 0:
        time_left -= 1
        minutes = time_left // 60
        seconds = time_left % 60
        timer_label.config(
            text=f"Tempo restante: {minutes} minutos e {seconds} segundos"
        )
        # Agendar a próxima atualização para daqui a 1 segundo (1000 milissegundos)
        root.after(1000, update_timer)
    else:
        messagebox.showinfo("Tempo esgotado", "O tempo acabou!")


# Função para verificar a resposta
def check_answer():
    global question_index, time_left, errors_count
    answer = answer_entry.get()
    if answer == answers[question_index]:
        question_index += 1
        errors_count = 0
        
        if question_index < len(questions):
            question.config(text=questions[question_index])
            answer_entry.delete(0, "end")
            
            # REABILITAR BOTÃO VERMELHO PARA A NOVA CHARADA (exceto xadrez)
            if question_index == len(questions) - 1:
                help_button.config(state=DISABLED, bg="gray")
            else:
                help_button.config(state=NORMAL, bg="red")  # Reabilita para nova charada
        else:
            # Ir para tela final
            question.pack_forget()
            answer_entry.pack_forget()
            help_button.place_forget()
            check_button.pack_forget()
            timer_label.pack_forget()
            
            final_screen = Label(
                root, 
                text="""🏆 MISSÃO CONCLUÍDA COM SUCESSO! 🏆

Você decifrou todos os enigmas e o código do xadrez!
Como um verdadeiro arqueólogo, superou cada desafio.

═══════════════════════════════════════════════════════════════

⚡ O ÚLTIMO MISTÉRIO AGUARDA ⚡

Uma antiga lâmpada começa a piscar mysteriosamente...
Luzes que dançam em padrões ancestrais...
Mensagens codificadas através da luz e sombra...

👁️ OBSERVE ATENTAMENTE OS SINAIS DE LUZ 👁️

A lâmpada revelará sequências secretas...
Pontos e traços perdidos no tempo...
Um código que abrirá o cadeado final...

═══════════════════════════════════════════════════════════════

⚠️  INSTRUÇÕES FINAIS  ⚠️

1. Aguarde a lâmpada começar a piscar
2. Anote cada sequência de luz
3. Decodifique a mensagem ancestral  
4. Use o código para abrir o cadeado
5. Encontre o DROIDINHO DE CRISTAL escondido!

═══════════════════════════════════════════════════════════════

🔍 PROCUREM A LUZ QUE REVELARÁ O TESOURO FINAL! 🔍
O Droidinho de cristal os aguarda...

A aventura está quase no fim...
Que a luz guie seus passos! ⚡✨""", 
                fg="gold", 
                bg="black", 
                font=("Courier", 14), 
                justify=CENTER
            )
            final_screen.pack(expand=True)
            
            # Fazer a tela piscar sutilmente para simular a lâmpada
            def piscar_tela():
                cores = ["black", "#0a0a0a", "black", "#050505"]
                cor_atual = 0
                def alternar_cor():
                    nonlocal cor_atual
                    root.configure(bg=cores[cor_atual % len(cores)])
                    final_screen.configure(bg=cores[cor_atual % len(cores)])
                    cor_atual += 1
                    root.after(1500, alternar_cor)
                alternar_cor()
            
            # Iniciar o efeito de piscar após 2 segundos
            root.after(2000, piscar_tela)
    else:
        errors_count += 1
        if errors_count == 1:
            penalty = 5
            message = "Perigos menores! -5 segundos"
        elif errors_count == 2:
            penalty = 10
            message = "Armadilhas ativadas! -10 segundos"
        else:
            penalty = 15
            message = f"Fuga urgente! -{penalty} segundos"
        
        time_left -= penalty
        messagebox.showinfo("Perigo!", f"{message}\n\nTente novamente!")


# Criar elementos do jogo (inicialmente ocultos)
question = Label(
    root, text=questions[question_index], fg="white", bg="black", 
    font=("Helvetica", 18), wraplength=1000, justify=CENTER  # Mudança: CENTER
)

answer_entry = Entry(root, width=50, fg="white", bg="black", font=("Helvetica", 18), justify=CENTER)  # Mudança: justify=CENTER

# Adicionar um rótulo para o temporizador (inicialmente oculto)
timer_label = Label(
    root,
    text=f"Tempo restante: {time_left} segundos",
    fg="red",
    bg="black",
    font=("Helvetica", 16),
)

# Botão vermelho redondo no canto (sem texto)
help_button = Button(
    root,
    text="",
    command=discount_time,
    fg="white",
    bg="red",
    width=3,
    height=1
)

check_button = Button(
    root,
    text="DECIFRAR ENIGMA",
    command=check_answer,
    fg="white",
    bg="darkblue",
    font=("Helvetica", 25, "bold"),
    padx=30,
    pady=10
)

# Função para iniciar o jogo
def start_game():
    global game_started
    game_started = True
    
    title_label.pack_forget()
    start_button.pack_forget()
    
    # BOTÃO VERMELHO SEMPRE VISÍVEL
    help_button.place(x=root.winfo_screenwidth()-150, y=20)
    help_button.config(state=NORMAL, bg="red")
    
    question.pack(pady=(100, 30))
    answer_entry.pack(pady=20)
    answer_entry.focus_set()
    check_button.pack(pady=30)
    timer_label.pack(pady=20)
    
    update_timer()

# Tela inicial
title_label = Label(
    root, 
    text="EXPEDIÇÃO ARQUEOLÓGICA\nTEMPLO DOS ENIGMAS PERDIDOS\n\nVocê adentra um templo misterioso com 6 câmaras antigas!\nCada câmara guarda um enigma ancestral que deve ser decifrado.\n\nApós as charadas, o DESAFIO FINAL DO XADREZ o aguarda!\nE por fim, encontrem o lendário DROIDINHO DE CRISTAL!\n\nTEMPO LIMITE: 40 minutos antes que as armadilhas se ativem!\n\nSISTEMA DE PENALIDADES POR CÂMARA:\n• 1º erro: Perigos menores (-5s)\n• 2º erro: Armadilhas ativadas (-10s) \n• 3º+ erro: Fuga urgente (-15s)\n\n🔮 SISTEMA DE ORÁCULOS E DICAS ANCESTRAIS 🔮\nCada charada possui APENAS 1 DICA ÚNICA!\nOs 2 LADOS devem decidir estrategicamente quando usar:\n• Oráculos Simples: 1 dica fácil (-5 minutos)\n• Oráculos Complexos: 1 dica média (-3 minutos)\n• Oráculos Supremos: 1 dica difícil (-2 minutos)\n\n🚫 ATENÇÃO EXPLORADORES! 🚫\nNÃO APERTEM O BOTÃO VERMELHO!\nEle desconta tempo precioso da expedição!\nApenas os MESTRES da expedição podem ativá-lo!\n\nUma vez usado, não há mais dicas para aquela charada!\nEscolham sabiamente o momento certo!\n\n🤖 OBJETIVO FINAL: Encontrar o DROIDINHO DE CRISTAL! 🤖\n\nQue os antigos o protejam nesta jornada!", 
    fg="gold", 
    bg="black", 
    font=("Helvetica", 18),
    justify=CENTER
)
title_label.pack(expand=True)

start_button = Button(
    root,
    text="ENTRAR NO TEMPLO",
    command=start_game,
    fg="black",
    bg="gold",
    font=("Helvetica", 30, "bold"),
    padx=40,
    pady=20
)
start_button.pack(pady=20)

root.mainloop()
