import time

import gradio as gr


def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.05)
        yield "You typed: " + message[: i + 1]


with gr.Blocks() as chat_interface:
    gr.Markdown("""
    ## Chat para consultar informações sobre bulas e estoque de medicamentos do Sistema HÓRUS
    Desenvolvido por [Ana Claudia Cabral](https://www.linkedin.com/in/anaclaudiacabral/) e [Marilia Ribeiro da Silva](https://www.linkedin.com/in/mariliaribeirodasilva/) durante o desenvolvimento do trabalho de conclusão da Pós Graduação em Processamento de Linguagem Natural da [UFG](https://ufg.br/) em parceria com a [AKCIT](https://akcit.ufg.br/).
    Código fonte disponível no [GitHub](https://github.com/mariliaribeiro/tcc_ufg_akcit_nlp).
    """)
    gr.ChatInterface(
        slow_echo,
        type="messages",
        autofocus=True,
        save_history=True,
    )
