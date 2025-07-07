import pdfplumber
import os

# Caminho da pasta onde estão os PDFs
CAMINHO_PASTA = r"C:\Storage\PDF_PROJETO"  #Raw string evita problemas com \

# Listar todos os arquivos da pasta
arquivos = os.listdir(CAMINHO_PASTA)

# Filtrar apenas os que terminam com .pdf
pdfs = [arq for arq in arquivos if arq.lower().endswith('.pdf')]

for nome_arquivo in pdfs:
    caminho_completo = os.path.join(CAMINHO_PASTA, nome_arquivo)

    print(f"\n📄 Lendo: {nome_arquivo}")
    
    with pdfplumber.open(caminho_completo) as pdf:
        texto_total = ""
        for pagina in pdf.pages:
            texto_total += pagina.extract_text() + "\n"

        print(texto_total[:500])  # Mostra só os primeiros 500 caractere