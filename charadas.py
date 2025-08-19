from tkinter import *
from tkinter import messagebox

root = Tk()
root.configure(bg="black") 
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
# Variáveis para armazenar as perguntas e respostas
questions = [
    "Charada 1:\nEu sou um gostoso \neu sou leal e inteligente\n\nAlém disso, se você olhar para Pi, eu estarei lá.\nQuem eu sou?",
    "Charada 2:\nSou um número primo menor que 10.\nSe me elevar ao quadrado, subtraírem 6 e multiplicarem por 3, obterás 81. Qual é o meu número?",
    "Charada 3:\nUm corpo acelerando em direção ao rosto do seu amigo a 10 m/s²\ntem massa similar a de uma xícara de 300 g,\nqual a força mínima que você tem que aplicar para que ele não se machuque?",
    "Charada 4:\nEu sou um número inteiro positivo.\nQuando dividido por 2, resulto em um quociente inteiro e resto zero.\nAlém disso, minha origem está na soma dos cinco primeiros números primos consecutivos,\ndividida por um primo distinto de 2.\nVocê sabe quem sou eu?",
    "Charada 5:\nSou um número primo menor que 10.\nSe me multiplicarem por 4, subtraírem 10 e depois dividirem por 2, obterão 9.\nQual é o meu número??",
    "Charada 6:\nUm corpo acelerando em direção ao rosto do seu amigo a 10 m/s²\ntem massa similar a de uma xícara de 200 g,\nqual a força mínima que você tem que aplicar para que ele não se machuque.",
    "Parabéns, você concluiu a PRIMEIRA etapa :) 🎆🎆\nAgora seu desafio será muito maior,o que teremos a seguir nesse angar de naves ??? hehe\nBoa sorte!\n\nEm um hangar de naves,\nEncontrei um tesouro perdido,\nCom ele, posso montar um código,\nQue, em um mundo digital,\nMe levará a um novo caminho.\n\n",
    "Meu Deus, você não desiste hein, vamos dificultar um pouquinho agora 👿\n\nAgora vamos pegar você espertinho🔪😡\n\n**Em uma espaçonave,\nDois mistérios estão escondidos,\nUm deles é uma cifra,\nO outro é uma chave.\nJuntos, eles formam um mistério,\nMas qual é esse mistério?**\n\n",
]

answers = [
    "Gui",  # 5
    "1",  # 7
    "1",  # 3
    "1",  # 4
    "1",  # 7
    "1",  # 2
    "onepieto",  #! Dica : O tesouro perdido são as peças do ábaco, que representam os dígitos de um número na tabela ASCII.
    "1",
]

# Dicas para cada charada
hints = [
    "Dica: Pense no que aparece nos primeiros dígitos de π (pi) = 3,14159...",
    "Dica: Teste os números primos menores que 10: 2, 3, 5, 7. Qual deles satisfaz a equação?",
    "Dica: Use F = m × a. Massa = 300g = 0,3kg, aceleração = 10 m/s²",
    "Dica: Os 5 primeiros primos são: 2, 3, 5, 7, 11. Some todos e divida por um primo diferente de 2",
    "Dica: Teste cada primo menor que 10 na fórmula: (x × 4 - 10) ÷ 2 = 9",
    "Dica: Use F = m × a. Massa = 200g = 0,2kg, aceleração = 10 m/s²",
    "Dica: 'onepieto' pode estar relacionado com One Piece + algo mais...",
    "Dica: Pense em criptografia. Cifra + Chave = ?",
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

# Função para iniciar o jogo
def start_game():
    global game_started
    game_started = True
    
    # Esconder elementos da tela inicial
    title_label.pack_forget()
    start_button.pack_forget()
    
    # Mostrar elementos do jogo
    question.pack(pady=15)
    hint_label.pack(pady=10)  # Espaço para a dica
    answer_entry.pack(pady=15)
    answer_entry.focus_set()  # Faz o cursor aparecer na caixa de entrada
    
    # BOTÃO DE DICA PRIMEIRO - bem visível
    hint_button.pack(pady=15)
    
    # Depois o botão de verificar
    check_button.pack(pady=10)
    
    # Timer por último
    timer_label.pack(pady=15)
    
    # Iniciar o temporizador
    update_timer()

# Tela inicial
title_label = Label(
    root, 
    text="🎮 JOGO DE CHARADAS 🎮\n\nVocê terá 40 minutos para responder 8 charadas!\n\nSistema de Penalidades por pergunta:\n1º erro: -5s | 2º erro: -10s | 3º+ erro: -15s\nDica: -60s\n\nBoa sorte! 🍀", 
    fg="white", 
    bg="black", 
    font=("Helvetica", 22),
    justify=CENTER
)
title_label.pack(expand=True)

start_button = Button(
    root,
    text="🚀 INICIAR JOGO 🚀",
    command=start_game,
    fg="black",
    bg="green",
    font=("Helvetica", 35, "bold"),
    padx=30,
    pady=15
)
start_button.pack(expand=True)

# Criar elementos do jogo (inicialmente ocultos)
question = Label(
    root, text=questions[question_index], fg="white", bg="black", font=("Helvetica", 30)
)

# Label para mostrar a dica (inicialmente vazio)
hint_label = Label(
    root, text="", fg="yellow", bg="black", font=("Helvetica", 20), wraplength=800
)

answer_entry = Entry(root, width=50, fg="white", bg="black", font=("Helvetica", 30))


# Função para mostrar dica
def show_hint():
    global time_left, hint_used
    if not hint_used:
        # Penalizar em 60 segundos
        time_left -= 60
        hint_used = True
        
        # Mostrar a dica
        hint_label.config(text=hints[question_index])
        hint_button.config(state=DISABLED, text=" DICA USADA", bg="gray", fg="black")
        
        messagebox.showinfo("Dica", f"Dica revelada! Penalidade: -60 segundos\n\n{hints[question_index]}")
    else:
        messagebox.showinfo("Dica", "Você já usou a dica desta pergunta!")


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


# Adicionar um rótulo para o temporizador (inicialmente oculto)
timer_label = Label(
    root,
    text=f"Tempo restante: {time_left} segundos",
    fg="red",
    bg="black",
    font=("Helvetica", 59),
)


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
        hint_button.config(state=NORMAL, text=" DICA (-60s)", bg="red", fg="white")
        
        # Se ainda houver perguntas, mostrar a próxima pergunta
        if question_index < len(questions):
            question.config(text=questions[question_index])
            # Limpar a entrada de texto
            answer_entry.delete(0, "end")
        else:
            messagebox.showinfo("Fim", "Parabéns, você respondeu todas as perguntas!")
    else:
        # Incrementar contador de erros na pergunta atual
        errors_count += 1
        
        # Sistema de penalidade progressiva (máximo 15s)
        if errors_count == 1:
            penalty = 5
            message = "1º erro nesta pergunta: -5 segundos"
        elif errors_count == 2:
            penalty = 10
            message = "2º erro nesta pergunta: -10 segundos"
        else:  # 3 ou mais erros - sempre 15s (não acumulativo)
            penalty = 15
            message = f"{errors_count}º erro nesta pergunta: -15 segundos"
        
        # Aplicar penalidade
        time_left -= penalty
        messagebox.showinfo("Resposta Incorreta", f"{message}\n\nTente novamente!")


# Criar botões (inicialmente ocultos)
hint_button = Button(
    root,
    text=" DICA (-60s)",
    command=show_hint,
    fg="white",
    bg="red",
    font=("Helvetica", 30, "bold"),
    padx=40,
    pady=15
)

check_button = Button(
    root,
    text="✅ VERIFICAR RESPOSTA",
    command=check_answer,
    fg="white",
    bg="blue",
    font=("Helvetica", 25, "bold"),
    padx=30,
    pady=10
)

# Iniciar o loop principal (o timer só inicia quando o jogo começar)
root.mainloop()
