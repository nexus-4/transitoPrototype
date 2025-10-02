import streamlit as st

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

        # Por enquanto, apenas exibimos uma mensagem de sucesso
        # No futuro, aqui chamaremos a função do `pipeline.py`
        with st.spinner("Iniciando o processo... (Etapa de placeholder)"):
            st.success("Processo iniciado! (Em breve, a mágica acontecerá aqui).")
            st.balloons() # Uma pequena comemoração!
else:
    st.warning("Aguardando o upload das imagens para continuar.")