import os
import pdfplumber
import re
import shutil
import csv
import unicodedata
import pytesseract
from pdf2image import convert_from_path

# Caminho do Poppler (ajuste se necessário)
POPPLER_PATH = r"C:\Users\ericb\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extrair_texto_ocr(caminho_pdf):
    try:
        imagens = convert_from_path(caminho_pdf, dpi=300, poppler_path=POPPLER_PATH)
        texto_ocr = ""
        for img in imagens:
            texto_ocr += pytesseract.image_to_string(img, lang='por') + "\n"
        return texto_ocr
    except Exception as e:
        print(f"❌ Falha ao aplicar OCR no arquivo: {caminho_pdf} - Erro: {e}")
        return ""

# Caminhos
PASTA_ORIGEM = r"C:\Storage\PDF_PROJETO"
PASTA_DESTINO = r"C:\Storage\PDF_PROJETO\output"
CAMINHO_CSV = r"C:\Storage\PDF_PROJETO\exportdata\index.csv"

# Função para limpar nomes inválidos
def limpar_nome(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'[<>:"/\\|?*\n\r]', '_', texto).strip()

# Regex mais flexíveis
REGEX_NOME = r"(?:Cliente|Raz[aã]o Social|Nome)[\s:]*([^\n\r]+)"
REGEX_NUMERO = r"(?:Documento(?:\s*n[oº°])?|N[oº°])[:\-]?\s*(\d+)"
REGEX_DATA = r"Data(?:\s*da Emiss[aã]o)?[:\-]?\s*(\d{2}[/\-]\d{2}[/\-]\d{4})"

registros = []

for nome_arquivo in os.listdir(PASTA_ORIGEM):
    if not nome_arquivo.lower().endswith('.pdf'):
        continue

    caminho_pdf = os.path.join(PASTA_ORIGEM, nome_arquivo)
    print(f"\n📄 Lendo: {nome_arquivo}")

    texto = ""
    metodo_extracao = "pdfplumber"

    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            for pagina in pdf.pages:
                pagina_texto = pagina.extract_text()
                if pagina_texto:
                    texto += pagina_texto + "\n"
    except Exception as e:
        print(f"⚠️ Erro ao ler '{nome_arquivo}': {e}")
        continue

    if not texto.strip():
        print(f"⚠️ PDF sem texto extraível com pdfplumber. Tentando OCR: {nome_arquivo}")
        texto = extrair_texto_ocr(caminho_pdf)
        metodo_extracao = "OCR"

        if not texto.strip():
            print(f"❌ Nenhum texto extraído com OCR. Pulando arquivo: {nome_arquivo}")
            continue

    # Tenta extrair usando regex direto
    nome_match = re.search(REGEX_NOME, texto, re.IGNORECASE)
    numero_match = re.search(REGEX_NUMERO, texto, re.IGNORECASE)
    data_match = re.search(REGEX_DATA, texto, re.IGNORECASE)

    # Fallback linha a linha se necessário
    if not nome_match or not numero_match or not data_match:
        for linha in texto.splitlines():
            if not nome_match and "cliente" in linha.lower():
                nome_match = re.search(r"[:\-]?\s*(.+)", linha)
            if not numero_match and ("nº" in linha.lower() or "documento" in linha.lower()):
                numero_match = re.search(r"[:\-]?\s*(\d+)", linha)
            if not data_match and "data" in linha.lower():
                data_match = re.search(r"(\d{2}[/\-]\d{2}[/\-]\d{4})", linha)

    nome = nome_match.group(1).strip().title() if nome_match else "Desconhecido"
    numero = numero_match.group(1) if numero_match else "0000"
    data = data_match.group(1).replace('/', '-') if data_match else "0000-00-00"

    # Sanitizar nome e montar caminho final
    nome_limpo = limpar_nome(nome)
    novo_nome = f"{nome_limpo.replace(' ', '_')}_{data}_Num{numero}.pdf"
    nova_pasta = os.path.join(PASTA_DESTINO, nome_limpo.replace(" ", "_"))
    novo_caminho = os.path.join(nova_pasta, novo_nome)

    os.makedirs(nova_pasta, exist_ok=True)
    shutil.copy2(caminho_pdf, novo_caminho)
    print(f"✅ Arquivo salvo em: {novo_caminho}")

    registros.append([nome, numero, data, novo_caminho, metodo_extracao])

# Cria pasta do CSV se não existir
os.makedirs(os.path.dirname(CAMINHO_CSV), exist_ok=True)

# Salva os dados extraídos
with open(CAMINHO_CSV, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Nome', 'NumeroDocumento', 'Data', 'CaminhoArquivo', 'Metodo'])
    writer.writerows(registros)

print("\n📁 Processamento finalizado com sucesso. Arquivos organizados e index.csv criado.")
