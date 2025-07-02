# 📄 Projeto Prometeus - Correção Textual Inteligente

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![Status](https://img.shields.io/badge/status-Estável-brightgreen)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-red)
![OCR](https://img.shields.io/badge/OCR-Google%20Vision-blue)

---

## 📝 Descrição

**Prometeus** é uma plataforma para processamento e correção inteligente de textos, permitindo:

- 📝 Correção ortográfica e estrutural de arquivos .txt, .docx e PDFs digitais
- 👁️ OCR em imagens e PDFs escaneados usando Google Cloud Vision
- 🧠 Correção e reescrita contextual com modelos Cohere
- 💾 Download dos arquivos corrigidos em .docx
- 🔄 Processamento em lote com interface Streamlit

Ideal para editoras, professores, alunos e equipes de revisão de conteúdo.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** para interface web
- **Cohere API** para correção textual inteligente
- **Google Cloud Vision API** para OCR
- **PyMuPDF (fitz)** para processamento de PDFs
- **python-docx** para exportação em DOCX

---
## 📂 Estrutura do Projeto
```
ProjetoPrometeus/
├── app_streamlit.py
├── processamento.py
├── uploads/
├── processed/
├── requirements.txt
└── README.md
```
---

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/ProjetoPrometeus.git
cd ProjetoPrometeus
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Configure suas chaves de API no arquivo config.py ou como variáveis de ambiente:

GOOGLE_API_KEY para OCR

COHERE_API_KEY para correção textual

5. Execute o aplicativo Streamlit:
```bash
streamlit run app_streamlit.py
```
✨ Funcionalidades Principais

✅ Upload de arquivos em múltiplos formatos (.png, .jpg, .jpeg, .pdf, .txt, .docx)

✅ OCR em imagens e PDFs escaneados

✅ Correção textual inteligente com prompts personalizados

✅ Processamento em lote com barra de progresso

✅ Download dos arquivos corrigidos em formato .docx

## 🤝 Contribuições

Contribuições são bem-vindas! Abra issues ou pull requests com melhorias, novos recursos ou correções.

## 🙌 Colabodores

Este projeto foi desenvolvido por Luã Saunders - @saunderz](https://github.com/saunderz) - para [Globaltec Educacional](https://github.com/globalteceducacional).

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.







