from fastapi import FastAPI

import gradio as gr
from src.api.routes.routes import router
from src.gradio.chat import chat_interface

app = FastAPI()
app.include_router(router)
app = gr.mount_gradio_app(app, chat_interface, path="")
