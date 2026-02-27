# Projeto RFV - Segmentação de Clientes

Este é um aplicativo web desenvolvido em Streamlit para realizar a segmentação de clientes utilizando a técnica RFV (Recência, Frequência e Valor).

## 📋 Sobre o Projeto

O RFV é uma metodologia de segmentação de clientes baseada no comportamento de compras. Ela considera três dimensões:

- **Recência (R):** Quantidade de dias desde a última compra do cliente.
- **Frequência (F):** Quantidade total de compras realizadas pelo cliente no período.
- **Valor (V):** Total de dinheiro gasto pelo cliente nas compras do período.

Com base nessas métricas, os clientes são classificados em grupos (de A a D) para orientar ações de marketing e CRM.

## 🚀 Aplicação em Produção

A aplicação está disponível online no seguinte endereço:

🔗 **https://deploy-streamlit.onrender.com**

## 🛠️ Funcionalidades

- Upload de arquivo CSV ou Excel com os dados de compras.
- Cálculo automático das métricas de Recência, Frequência e Valor.
- Segmentação dos clientes em quartis (A, B, C, D).
- Geração de scores RFV (ex: AAA, ABB, DCC, etc.).
- Sugestões de ações de marketing baseadas no score do cliente.
- Download dos resultados em formato Excel.

## 📁 Estrutura do Repositório
.
├── app.py # Aplicação principal Streamlit
├── requirements.txt # Dependências do projeto
├── runtime.txt # Versão do Python utilizada
└── README.md # Documentação do projeto


## 🐍 Versão do Python

Este projeto foi desenvolvido e testado com **Python 3.11.9**. A versão é explicitamente definida no arquivo `runtime.txt` e também via variável de ambiente no Render para garantir compatibilidade.

## 📦 Dependências

As principais bibliotecas utilizadas são:

- streamlit
- pandas
- numpy
- xlsxwriter
- Pillow

Para instalar as dependências localmente:

```bash
pip install -r requirements.txt