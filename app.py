import streamlit as st
import traceback
import tempfile
import subprocess
from processing.pipeline import run_colmap_pipeline
import os

# Config da pagina

st.set_page_config(
    page_title="MVP Pericia de Transito",
    page_icon=":car:",
    layout="wide",
)

# Titulo da pagina e Descricao
st.title("Ferramenta de reconstrucao 3D para pericia de transito")
st.markdown("""
    Esta é uma prova de conceito (MVP) para demonstrar a reconstrução de cenas de acidente a partir de um conjunto de fotos.
""")

# Modulo de upload de imagens
st.header("1. Faca o upload das imagens")

# Permitir upload de multiplos arquivos
uploaded_files = st.file_uploader(
    "Escolha as imagens", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

# Verifica se algum arquivo foi enviado
if uploaded_files:
    st.info(f"{len(uploaded_files)} arquivos enviados com sucesso!")
    st.markdown("---") # Linha divisoria

    # Modulo de processamento das imagens
    st.header("2. Inicie o processamento")
    st.write("Clique no botao abaixo para iniciar a reconstrução 3D.")

    # Botao para iniciar o processamento
    if st.button("Iniciar Processamento", type="primary"):
        # Diretorio temporario para gerenciar os arquivos do projeto
        with tempfile.TemporaryDirectory() as temp_dir:
            image_dir = os.path.join(temp_dir, "images")
            workspace_dir = os.path.join(temp_dir, "workspace")
            os.makedirs(image_dir, exist_ok=True)
            os.makedirs(workspace_dir, exist_ok=True)

            # Salva os arquivos enviados no diretorio de imagens temporario
            for uploaded_file in uploaded_files:
                with open(os.path.join(image_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            st.success("Arquivos salvos com sucesso!")

            with st.spinner("Processando as imagens, por favor aguarde..."):
                try:
                    # Chama a funcao do modulo de processamento
                    result_path = run_colmap_pipeline(image_dir=image_dir, workspace_dir=workspace_dir)

                    if result_path and os.path.exists(result_path):
                        st.success("Reconstrucao ESPARSA concluida com sucesso!")
                        st.info("O 'esqueleto' 3D da cena foi gerada em um arquivo PLY.")
                        st.balloons()

                        # Botao para download do arquivo PLY
                        with open(result_path, "rb") as file:
                            st.download_button(
                                label="Baixar modelo 3D (PLY)",
                                data=file,
                                file_name="sparse_model.ply",
                                mime="application/octet-stream"
                            )
                    else:
                        st.error("O pipeline foi executado, mas o arquivo de modelo 3D nao foi gerado.")

                except subprocess.CalledProcessError as e:
                    st.error(f"Ocorreu um erro durante o processamento: {e}")
                    st.code(e.stderr, language="bash")
                except Exception as e:
                    st.error(f"Ocorreu um erro inesperado: {e}")
                    st.code(traceback.format_exc(), language="bash")
else:
    st.warning("Aguardando o upload das imagens para continuar.")