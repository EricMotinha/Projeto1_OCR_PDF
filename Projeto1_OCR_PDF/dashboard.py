# dashboard.py
# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o CSV
CAMINHO_CSV = r"C:\Storage\PDF_PROJETO\exportdata\index.csv"

st.set_page_config(page_title="Dashboard OCR PDF", layout="wide")

# Título
st.title("📄 Dashboard - PDFs Automatizados com OCR")

# Carregando os dados
@st.cache_data
def carregar_dados():
    return pd.read_csv(CAMINHO_CSV)

df = carregar_dados()

# Filtros laterais
st.sidebar.header("🔎 Filtros")
nomes = st.sidebar.multiselect("Filtrar por Nome:", df["Nome"].unique(), default=df["Nome"].unique())
df_filtrado = df[df["Nome"].isin(nomes)]

# Quantidade de PDFs por nome
st.subheader("📊 Quantidade de PDFs por Nome")
qtd_por_nome = df_filtrado["Nome"].value_counts()
st.bar_chart(qtd_por_nome)

# Tabela de dados
st.subheader("📁 Tabela de Documentos")
st.dataframe(df_filtrado)

# Link de download
st.download_button("📥 Baixar CSV filtrado", df_filtrado.to_csv(index=False), "pdf_index_filtrado.csv", "text/csv")

