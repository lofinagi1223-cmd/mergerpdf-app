import streamlit as st
import os
import time
from Database import Database
from merger import PDFMerger

class PDFApp:
    def __init__(self):
        self.db = Database()
        st.set_page_config(page_title="PDF Merge", page_icon="C:\Users\Rafael\Desktop\mergerpdf-app\unnamed-removebg-preview.png", layout="centered")

    
    # LOGIN
    
    def tela_login(self):
        st.title("📌 PDF Merge")
        st.write("Acesso apenas com usuários pré-definidos.")

        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            valido, nome = self.db.validar_usuario(email, senha)
            if valido:
                st.session_state["usuario"] = nome
                st.session_state["email"] = email
                self.db.registrar_login(email)

                with st.spinner("Em andamento"):
                    time.sleep(5)
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")
                url = "https://gmail.com"
                st.write("Se perdeu o acesso, envie e-mail relatando para [pdfmerge-company@gmail.com](%s) (retorno em até 24h)" % url)
                

    
    # ÁREA DE MERGE
    
    def tela_merge(self):
        if st.button("Sair"):
            st.session_state.clear()
            st.success("Você saiu com sucesso!")
            time.sleep(2)
            st.rerun()

        st.divider()
        st.write(f"👋 Olá, **{st.session_state['usuario']}**! Faça o upload dos PDFs que deseja mesclar.")

        uploaded_files = st.file_uploader(
            "Selecione PDFs para mesclar", type="pdf", accept_multiple_files=True
        )

        if uploaded_files and len(uploaded_files) > 1:
            if st.button("Mesclar PDFs"):
                pasta_uploads = "uploads"
                os.makedirs(pasta_uploads, exist_ok=True)

                caminhos = []
                for arquivo in uploaded_files:
                    caminho = os.path.join(pasta_uploads, arquivo.name)
                    with open(caminho, "wb") as f:
                        f.write(arquivo.getbuffer())
                    caminhos.append(caminho)

                merger = PDFMerger()
                merger.add_files(caminhos)
                caminho_saida = os.path.join(pasta_uploads, "PDF_Mesclado.pdf")
                merger.save(caminho_saida)
                st.success("✅ PDFs mesclados com sucesso!")

                # Registra o merge no Firestore
                self.db.registrar_merge(
                    st.session_state["usuario"],
                    [a.name for a in uploaded_files]
                )

                with open(caminho_saida, "rb") as f:
                    st.download_button(
                        label="⬇️ Baixar PDF Mesclado",
                        data=f,
                        file_name="PDF_Mesclado.pdf",
                        mime="application/pdf"
                    )

        elif uploaded_files and len(uploaded_files) == 1:
            st.warning("⚠️ **Mínimo 2 PDFs**")

    
    # EXECUÇÃO PRINCIPAL
    
    def run(self):
        if "usuario" not in st.session_state:
            self.tela_login()
        else:
            self.tela_merge()



    # MAIN

if __name__ == "__main__":
    app = PDFApp()
    app.run()
