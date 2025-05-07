import os
import streamlit as st
import zipfile
import time
from processamento import processar_arquivo
import shutil

# --- Diretórios ---
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
for folder in (UPLOAD_FOLDER, PROCESSED_FOLDER):
    os.makedirs(folder, exist_ok=True)

# --- Estado Inicial ---
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'files' not in st.session_state:
    st.session_state.files = []
if 'processed_count' not in st.session_state:
    st.session_state.processed_count = 0
if 'current_upload_files' not in st.session_state:
    st.session_state.current_upload_files = []

# --- Configuração da Página ---
st.set_page_config(
    page_title="Projeto Prometeus",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Funções Auxiliares ---
def limpar_diretorios():
    """Limpa os diretórios de upload e processamento"""
    for fld in (UPLOAD_FOLDER, PROCESSED_FOLDER):
        shutil.rmtree(fld, ignore_errors=True)
        os.makedirs(fld, exist_ok=True)
    st.session_state.files = []
    st.session_state.processed_count = 0
    return True

def processar_arquivo_seguro(file_path, prompt, mode):
    """Processa arquivo com tratamento de erros adequado"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        # Verifica extensão
        ext = os.path.splitext(file_path)[1].lower()
        allowed_exts = {'.png', '.jpg', '.jpeg', '.pdf', '.txt', '.docx'}
        if ext not in allowed_exts:
            raise ValueError(f"Formato de arquivo não suportado: {ext}")
        
        # Processa o arquivo
        output_name = processar_arquivo(file_path, prompt, mode)
        st.session_state.processed_count += 1
        return output_name
    
    except Exception as e:
        st.error(f"❌ Erro ao processar {os.path.basename(file_path)}: {str(e)}")
        return None

# --- Barra Lateral de Configurações ---
st.sidebar.header("Configurações")
mode_option = st.sidebar.radio(
    "Modo de Processamento",
    ["Texto (digitais)", "OCR (imagens/PDF)"],
    index=0,
    help="Escolha 'Texto' para arquivos digitais (TXT, DOCX) ou 'OCR' para imagens e PDFs escaneados"
)
mode = 'ocr' if mode_option.startswith('OCR') else 'texto'

prompt = st.sidebar.text_area(
    "Prompt de Correção",
    "Corrija o texto mantendo formatação e ortografia.",
    help="Instruções para o modelo de IA sobre como corrigir o texto"
)

if st.sidebar.button("Limpar Tudo", help="Remove todos os arquivos carregados e processados"):
    if limpar_diretorios():
        st.sidebar.success("✨ Tudo limpo!")
        st.rerun()

# --- Conteúdo Centralizado ---
col1, col_center, col3 = st.columns([1, 4, 1])
with col_center:
    # Logo centralizada
    logo_path = 'logo.png'
    if os.path.exists(logo_path):
        lcol1, lcol2, lcol3 = st.columns([2, 2, 1])
        lcol2.image(logo_path, width=250)
    
    # Título e subtítulo
    st.title("Projeto Prometeus")
    st.subheader("Correção Textual Inteligente")

    # Instruções
    st.markdown(
        """
        📝 **Instruções:**
        1. Selecione um ou mais arquivos para processar
        2. Para múltiplos arquivos, você pode usar um arquivo ZIP
        3. Escolha o modo de processamento adequado na barra lateral
        4. Defina o prompt de correção desejado
        5. Clique em 'Iniciar Processamento'
        """
    )

    # Upload de arquivos
    uploaded = st.file_uploader(
        "Carregar Arquivos",
        type=['png','jpg','jpeg','pdf','txt','docx','zip'],
        accept_multiple_files=True,
        help="Arraste os arquivos ou clique para selecionar"
    )

    if uploaded:
        # Limpa as listas anteriores
        st.session_state.files = []
        st.session_state.current_upload_files = []
        
        with st.spinner("Preparando arquivos..."):
            for f in uploaded:
                dest = os.path.join(UPLOAD_FOLDER, f.name)
                # Salva o arquivo
                with open(dest, 'wb') as out:
                    out.write(f.getvalue())
                
                # Se for ZIP, extrai e remove o arquivo ZIP
                if f.name.lower().endswith('.zip'):
                    try:
                        with zipfile.ZipFile(dest, 'r') as zf:
                            zf.extractall(UPLOAD_FOLDER)
                        os.remove(dest)
                        # Adiciona arquivos do ZIP à lista atual
                        for fn in os.listdir(UPLOAD_FOLDER):
                            if fn.lower().endswith(('png','jpg','jpeg','pdf','txt','docx')):
                                file_path = os.path.join(UPLOAD_FOLDER, fn)
                                if file_path not in st.session_state.current_upload_files:
                                    st.session_state.current_upload_files.append(file_path)
                                    st.session_state.files.append(file_path)
                    except Exception as e:
                        st.error(f"❌ Erro ao extrair ZIP {f.name}: {str(e)}")
                else:
                    # Adiciona arquivo não-ZIP à lista atual
                    if f.name.lower().endswith(('png','jpg','jpeg','pdf','txt','docx')):
                        st.session_state.current_upload_files.append(dest)
                        st.session_state.files.append(dest)
            
            st.session_state.current_upload_files = sorted(st.session_state.current_upload_files)
            st.session_state.files = sorted(st.session_state.files)

    # Lista de arquivos prontos
    if st.session_state.current_upload_files:
        with st.expander("📂 Arquivos prontos para processar", expanded=True):
            for path in st.session_state.current_upload_files:
                st.markdown(f"- {os.path.basename(path)}")

    # Botão de processamento
    process_btn = st.button(
        "🚀 Iniciar Processamento",
        disabled=st.session_state.processing or not st.session_state.files,
        help="Clique para iniciar o processamento dos arquivos"
    )

    if process_btn:
        st.session_state.processing = True
        progress = st.progress(0)
        status = st.empty()
        
        total = len(st.session_state.files)
        successful = 0
        
        for i, path in enumerate(st.session_state.files, start=1):
            status.info(f"⏳ Processando {os.path.basename(path)} ({i}/{total})...")
            
            output = processar_arquivo_seguro(path, prompt, mode)
            if output:
                successful += 1
                st.success(f"✅ Arquivo processado: {output}")
            
            progress.progress(i / total)
            time.sleep(0.1)  # Pequena pausa para feedback visual
        
        status.success(f"🎉 Processamento concluído! {successful}/{total} arquivos processados com sucesso.")
        st.balloons()
        st.session_state.processing = False

    # Resultados
    processed_files = sorted(os.listdir(PROCESSED_FOLDER))
    if processed_files:
        st.header("📥 Arquivos Processados")
        for fn in processed_files:
            with st.expander(fn):
                col1, col2 = st.columns([3,1])
                with col1:
                    st.markdown(f"**Nome:** {fn}")
                with col2:
                    with open(os.path.join(PROCESSED_FOLDER, fn), 'rb') as file:
                        st.download_button(
                            "⬇️ Baixar",
                            data=file,
                            file_name=fn,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
