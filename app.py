# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git remote add origin https://github.com/nicoig/GPT-Clone.git
# git commit -m "Initial commit"
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

################################################

import streamlit as st
from fpdf import FPDF
import os
from dotenv import load_dotenv
import openai
import base64
import io

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.markdown("<h1 style='text-align: center;'>ChatGPT Clon</h1>", unsafe_allow_html=True)

model_options = {
    "GPT-4 Turbo": "gpt-4-1106-preview",
    "GPT-4": "gpt-4",
    "GPT-3.5-turbo": "gpt-3.5-turbo"
}

selected_model = st.selectbox("Selecciona el modelo de GPT", options=list(model_options.keys()), index=list(model_options.keys()).index("GPT-4 Turbo"))

col1, col2, col3 = st.columns([5, 1, 1])
with col2:
    if st.button("🗑️"):
        st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy ChatGPT, ¿En qué puedo ayudarte?"}]
        st.experimental_rerun()


with col3:
    def save_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for msg in st.session_state["messages"]:
            role = "Tú: " if msg["role"] == "user" else "ChatGPT: "
            pdf.multi_cell(0, 10, role + msg["content"])
        pdf_file_path = "ChatGPT_conversation.pdf"
        pdf.output(pdf_file_path)
        return pdf_file_path

    def download_pdf():
        pdf_file_path = save_pdf()
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
        pdf_bio = io.BytesIO(pdf_data)
        pdf_bio.name = pdf_file_path
        st.download_button(
            label="Descargar PDF",
            data=pdf_bio,
            file_name=pdf_file_path,
            mime="application/pdf",
            key="download-pdf-button",
            on_click=lambda: None,
            args=()
        )
    
    if st.button("💾"):
        download_pdf()
        

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hola, soy ChatGPT, ¿En qué puedo ayudarte?"}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner(text='Cargando...'):
        response = openai.ChatCompletion.create(
            model=model_options[selected_model],
            messages=st.session_state["messages"]
        )
        responseMessage = response['choices'][0]['message']['content']
        st.session_state["messages"].append({"role": "assistant", "content": responseMessage})
        st.chat_message("assistant").write(responseMessage)