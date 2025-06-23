import time

import gradio as gr
from src.agents.main import MyAgent
from src.config import EMBEDDING_PROVIDER, LLM_MAX_TOKENS, LLM_PROVIDER, LLM_TEMPERATURE


def my_agent(message, history):
    for i in range(len(message)):
        time.sleep(0.05)
        # yield "You typed: " + message[: i + 1]

        agent = MyAgent(
            llm_provider=LLM_PROVIDER,
            llm_temperature=LLM_TEMPERATURE,
            llm_max_tokens=LLM_MAX_TOKENS,
            embedding_provider=EMBEDDING_PROVIDER,
        )
        yield agent.invoke(message)


with gr.Blocks() as chat_interface:
    gr.Markdown("""
    ## Chat para consultar informações sobre bulas e estoque de medicamentos do Sistema HÓRUS
    Desenvolvido por [Ana Claudia Cabral](https://www.linkedin.com/in/anaclaudiacabral/) e [Marilia Ribeiro da Silva](https://www.linkedin.com/in/mariliaribeirodasilva/) durante o desenvolvimento do trabalho de conclusão da Pós Graduação em Processamento de Linguagem Natural da [UFG](https://ufg.br/) em parceria com a [AKCIT](https://akcit.ufg.br/).
    Código fonte disponível no [GitHub](https://github.com/mariliaribeiro/tcc_ufg_akcit_nlp).
    """)
    gr.ChatInterface(
        my_agent,
        type="messages",
        autofocus=True,
        save_history=True,
    )
