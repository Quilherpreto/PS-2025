from tkinter import *
from tkinter import messagebox

root = Tk()
root.configure(bg="black") 
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

# Variáveis para armazenar as perguntas e respostas
questions = [
    "Charada 1:\n\n*Não se pode ver, não se pode sentir,*\n\n*Não se pode cheirar, não se pode ouvir.*\n\n*Está sob as colinas e além das estrelas,*\n\n*Cavidades vazias – ele vai enchê-las.*\n\n*De tudo vem antes e vem em seguida,*\n\n*Do riso é a morte, é o fim da vida.*\n\nIMPORTANTE: Responda em letras minúsculas!",
    "Charada 2:\n\n*Essa é a coisa que a tudo devora*\n\n*Feras, aves, plantas, flora.*\n\n*Aço e ferro são sua comida,*\n\n*E a dura pedra por ele moída;*\n\n*Aos reis abate, à cidade arruína,*\n\n*E a alta montanha faz pequenina.*",
    "Charada 3:\n\nJuntos, um Mago, um Cavalheiro, um Bárbaro e um Eremita receberam 70 Esmeraldas.\n\nCada um recebeu um número inteiro de Esmeraldas e cada um recebeu pelo menos um.\n\nO Mago recebeu mais do que cada um dos outros.\n\nO Cavalheiro e o Bárbaro receberam, juntos, 45 Esmeraldas.\n\nQuantas Esmeraldas sobraram para o Eremita?",
    "Charada 4:\n\nCerto dia, um sábio matemático, disposto de seu Camelo, caminhavam longamente em direção à cidade de Bagdá. No entanto, em seu caminho, encontrou três irmãos em profundo debate. Ao se informar da situação, eis o problema:\n\n• Um antigo nobre partiu em sua jornada final e deixou 17 Camelos como herança para a partilha entre seus três filhos, ordenando a seguinte divisão:\n• O mais velho deverá receber a metade.\n• O do meio deverá receber a terça parte.\n• O mais novo deverá receber apenas a nona parte.\n\nPorém, ao tentar dividir, os irmãos se desesperaram: 17 não se divide exatamente nessas partes.\n\nQuantos Camelos serão dispostos a cada irmão de modo que a partilha seja exata e ninguém fique em desvantagem?\n\n(Separe os números encontrados por vírgula e sem espaços)",
    "Charada 5:\n\nObserve atentamente esta sequência numérica:\n\n1, 4, 9, 16, 25, __ ?\n\nQual é o próximo número e por quê?\n\nResponda apenas o número que completa a sequência.",
    "Charada 6:\n\nVocê tem 3 caixas: uma com bolas vermelhas, uma com bolas azuis, e uma com bolas mistas (vermelhas e azuis).\n\nTodas as etiquetas das caixas estão trocadas.\n\nVocê pode tirar apenas 1 bola de uma caixa para descobrir o conteúdo de todas.\n\nDe qual caixa você deve tirar?\n\nResponda: vermelhas, azuis ou mistas",
    "Charada 7:\n\nEm uma família há 5 meninas e alguns meninos.\n\nO número total de filhos é 8.\n\nQuantos meninos há na família?\n\nResponda apenas o número.",
    "Charada 8:\n\nUm pai tem 32 anos e seu filho tem 8 anos.\n\nEm quantos anos a idade do pai será o dobro da idade do filho?\n\nResponda apenas o número de anos.",
]

answers = [
    "escuro",  # Charada 1 - O Hobbit
    "tempo",   # Charada 2 - O Hobbit
    "1",       # Charada 3 - Esmeraldas do Eremita
    "9,6,2",   # Charada 4 - Divisão dos Camelos
    "36",      # Charada 5 - Sequência dos quadrados perfeitos
    "mistas",  # Charada 6 - Problema das caixas com bolas
    "3",       # Charada 7 - Problema simples dos meninos (8 total - 5 meninas = 3 meninos)
    "16",      # Charada 8 - Problema das idades (em 16 anos: pai 48, filho 24)
]

# Dicas para cada charada
hints = [
    "Dica: Pense no que não pode ser percebido pelos sentidos, mas está em todo lugar. Uma palavra de 6 letras...",
    "Dica: Pense no que desgasta tudo, envelhece reis e montanhas. Uma palavra de 5 letras...",
    "Dica: Total = 70. Cavalheiro + Bárbaro = 45. Restam 25 para Mago + Eremita. O Mago tem mais que todos os outros...",
    "Dica: O sábio emprestou seu camelo! Com 18 camelos: metade=9, terça parte=6, nona parte=2. Total: 17!",
    "Dica: Pense nos quadrados! 1² = 1, 2² = 4, 3² = 9... Qual seria 6²?",
    "Dica: Tire da caixa que tem certeza de que não é o que está escrito. Qual caixa te dará mais informação?",
    "Dica: Uma conta simples! Se há 5 meninas e o total é 8 filhos, quantos meninos restam? 8 - 5 = ?",
    "Dica: Pai: 32+x anos, Filho: 8+x anos. Quando pai = 2×filho? Monte a equação: 32+x = 2(8+x)",
]

# Índice da pergunta atual
question_index = 0

# Variável para controlar se o jogo foi iniciado
game_started = False

# Variável para controlar se a dica foi usada na pergunta atual
hint_used = False

# Variável para contar erros na pergunta atual
errors_count = 0

# Variável para armazenar o tempo restante
time_left = 2400  # 40 minutos

# Função para mostrar dica
def show_hint():
    global time_left, hint_used
    if not hint_used:
        # Penalizar em 60 segundos
        time_left -= 60
        hint_used = True
        
        # Mostrar a dica
        hint_label.config(text=hints[question_index])
        hint_button.config(state=DISABLED, text="DEUSES INVOCADOS", bg="gray", fg="black")
        
        messagebox.showinfo("Sabedoria dos Antigos", f"Os deuses sussurram em seu ouvido! Penalidade: -60 segundos\n\n{hints[question_index]}")
    else:
        messagebox.showinfo("Silêncio dos Deuses", "Os antigos já lhe concederam sua sabedoria nesta câmara!")


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
    global question_index, time_left, hint_used, errors_count
    # Pegar o valor da entrada de texto
    answer = answer_entry.get()
    # Verificar se a resposta está correta
    if answer == answers[question_index]:
        # Avançar para a próxima pergunta
        question_index += 1
        # Resetar a dica e erros para a próxima pergunta
        hint_used = False
        errors_count = 0
        hint_label.config(text="")
        hint_button.config(state=NORMAL, text="INVOCAR OS DEUSES (-60s)", bg="darkred", fg="white")
        
        # Se ainda houver perguntas, mostrar a próxima pergunta
        if question_index < len(questions):
            question.config(text=questions[question_index])
            # Limpar a entrada de texto
            answer_entry.delete(0, "end")
        else:
            # Tela final épica - esconder elementos do jogo (mas manter o timer)
            question.pack_forget()
            hint_label.pack_forget()
            answer_entry.pack_forget()
            hint_button.pack_forget()
            check_button.pack_forget()
            
            # Criar tela final misteriosa
            final_screen = Label(
                root,
                text="""PARABÉNS, AVENTUREIRO!

Você decifrou todos os enigmas antigos com maestria!
Como um verdadeiro explorador, superou cada desafio com coragem.

═══════════════════════════════════════════════════════════════

O TEMPLO REVELA SEUS SEGREDOS...

PRÓXIMA MISSÃO: 
Dirija-se rapidamente ao TABULEIRO DE XADREZ!
Lá encontrará seu próximo desafio arqueológico.

═══════════════════════════════════════════════════════════════

MISTÉRIO FINAL:

Sussurros ecoam pelas paredes antigas...
Duas máquinas místicas aguardam em silêncio...

Uma delas guarda frequências perdidas no tempo,
Ondas que atravessam dimensões...
Uma LUZ de origens desconhecidas...

Após conquistar o xadrez,
As frequências se revelarão,
E você descobrirá que nem tudo
É o que parece ser...

═══════════════════════════════════════════════════════════════

A aventura está apenas começando...
O tempo é precioso - CORRA!""",
                fg="gold",
                bg="black",
                font=("Courier", 16),
                justify=CENTER
            )
            final_screen.pack(expand=True)
            # Timer continua visível na tela final
            timer_label.pack(pady=10)
    else:
        # Incrementar contador de erros na pergunta atual
        errors_count += 1
        
        # Sistema de penalidade progressiva (máximo 15s)
        if errors_count == 1:
            penalty = 5
            message = "Perigos menores ativados! -5 segundos"
        elif errors_count == 2:
            penalty = 10
            message = "Armadilhas antigas dispararam! -10 segundos"
        else:  # 3 ou mais erros - sempre 15s (não acumulativo)
            penalty = 15
            message = f"Fuga urgente necessária! -{penalty} segundos"
        
        # Aplicar penalidade
        time_left -= penalty
        messagebox.showinfo("Perigo no Templo!", f"{message}\n\nTente decifrar novamente o enigma!")


# Criar elementos do jogo (inicialmente ocultos)
question = Label(
    root, text=questions[question_index], fg="white", bg="black", 
    font=("Helvetica", 18), wraplength=1000, justify=LEFT
)

# Label para mostrar a dica (inicialmente vazio)
hint_label = Label(
    root, text="", fg="yellow", bg="black", font=("Helvetica", 16), wraplength=1000
)

answer_entry = Entry(root, width=50, fg="white", bg="black", font=("Helvetica", 18))

# Adicionar um rótulo para o temporizador (inicialmente oculto)
timer_label = Label(
    root,
    text=f"Tempo restante: {time_left} segundos",
    fg="red",
    bg="black",
    font=("Helvetica", 16),
)

# Criar botões (inicialmente ocultos)
hint_button = Button(
    root,
    text="INVOCAR OS DEUSES (-60s)",
    command=show_hint,
    fg="white",
    bg="darkred",
    font=("Helvetica", 25, "bold"),
    padx=30,
    pady=15
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
    
    # Esconder elementos da tela inicial
    title_label.pack_forget()
    start_button.pack_forget()
    
    # Mostrar elementos do jogo
    question.pack(pady=20)
    hint_label.pack(pady=5)  # Espaço para a dica
    answer_entry.pack(pady=15)
    answer_entry.focus_set()  # Faz o cursor aparecer na caixa de entrada
    
    # BOTÃO DE DICA PRIMEIRO - bem visível
    hint_button.pack(pady=10)
    
    # Depois o botão de verificar
    check_button.pack(pady=10)
    
    # Timer por último
    timer_label.pack(pady=10)
    
    # Iniciar o temporizador
    update_timer()

# Tela inicial
title_label = Label(
    root, 
    text="EXPEDIÇÃO ARQUEOLÓGICA\nTEMPLO DOS ENIGMAS PERDIDOS\n\nVocê adentra um templo misterioso com 8 câmaras antigas!\nCada câmara guarda um enigma ancestral que deve ser decifrado.\n\nTEMPO LIMITE: 40 minutos antes que as armadilhas se ativem!\n\nSISTEMA DE PENALIDADES POR CÂMARA:\n• 1º erro: Perigos menores (-5s)\n• 2º erro: Armadilhas ativadas (-10s) \n• 3º+ erro: Fuga urgente (-15s)\n• Pedir ajuda aos deuses: (-60s)\n\nQue os antigos o protejam nesta jornada!", 
    fg="gold", 
    bg="black", 
    font=("Helvetica", 20),
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

# Iniciar o loop principal (o timer só inicia quando o jogo começar)
root.mainloop()
