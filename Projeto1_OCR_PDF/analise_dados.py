# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o CSV gerado pelo projeto
CAMINHO_CSV = r"C:\Storage\PDF_PROJETO\exportdata\index.csv"

# Lê o CSV
df = pd.read_csv(CAMINHO_CSV)

# Gráfico 1: Quantidade de PDFs por método de extração
df['Metodo'].value_counts().plot(kind='bar', color=['#4CAF50', '#FF9800'])
plt.title('Quantidade de PDFs por Método de Extração')
plt.xlabel('Método')
plt.ylabel('Número de Arquivos')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Gráfico 2: Datas extraídas por método (distribuição)
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
df.dropna(subset=['Data'], inplace=True)
df.groupby('Metodo')['Data'].count().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Distribuição de Datas extraídas por Método')
plt.ylabel('')
plt.tight_layout()
plt.show()
