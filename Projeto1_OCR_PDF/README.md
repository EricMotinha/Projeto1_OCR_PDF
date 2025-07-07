# 📄 Projeto 1 — PDF Reader and Organizer Automation with Python / Automatizador de PDF com OCR (Python)

## 🇺🇸 Overview

This project automatically extracts data from PDF files using Python, renames them based on extracted content (like client name, date and document number), organizes them into folders, and creates a structured CSV index.

## 🇧🇷 Visão Geral

Este projeto automatiza a leitura de arquivos PDF com Python, extrai dados como nome do cliente, número e data do documento, renomeia os arquivos com base nessas informações, organiza em pastas e gera um índice CSV com todos os dados.

---

## 🛠️ Tecnologias | Technologies

- Python 3.x
- pdfplumber
- re (Regex)
- shutil / os
- csv
- (opcional para expansão futura: pytesseract, pdf2image)

---

## 📁 Estrutura do Projeto | Project Structure

Projeto1_OCR_PDF/
├── src/
│ └── Projeto1_OCR_PDF.py # Script principal
├── output/ # Pastas com PDFs organizados
├── samples/ # PDFs de entrada
├── exportdata/
│ └── index.csv # CSV com dados extraídos
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

---

## ▶️ Como executar | How to run

1. Instale as dependências:

```bash
pip install -r requirements.txt
