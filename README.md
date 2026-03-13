# Credit Scoring - M38 Streamlit + PyCaret

Projeto final do modulo 38 do curso Cientista de Dados (EBAC).
Construcao de um modelo de **credit scoring** para cartao de credito com 15 safras e 12 meses de performance.

---

## Demo

https://github.com/user-attachments/assets/bd3e418e-b6e5-42e0-89ea-6655e7f41f9f

---

## Estrutura do projeto

| Arquivo | Descricao |
|---|---|
| `app.py` | Aplicacao Streamlit para escoragem |
| `model_final.pkl` | Pipeline sklearn treinado (Regressao Logistica) |
| `model_pycaret_lgbm.pkl` | Modelo LightGBM via PyCaret |
| `M38_Projeto.ipynb` | Notebook principal do projeto |
| `M38_Sklearn pipeline.ipynb` | Exemplos de pipeline sklearn |
| `M38_Pycaret nos dados do projeto.ipynb` | Modelagem com PyCaret |
| `M38_Transformacao nos dados antes do treino.ipynb` | Pre-processamento |
| `M38_Exercicio1.ipynb` | Exercicio complementar |

---

## Como executar

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Modelo

- **Base de desenvolvimento:** 12 safras (jan/2015 a dez/2015) - 600.000 registros
- **Base out of time (OOT):** 3 safras (jan/2016 a mar/2016) - 150.000 registros
- **Pipeline:** imputacao + winzorizacao + dummies + StandardScaler + PCA + Regressao Logistica
- **Metrica principal:** AUC-ROC e KS

---

## Colunas esperadas no CSV

| Coluna | Tipo |
|---|---|
| sexo | M / F |
| posse_de_veiculo | S / N |
| posse_de_imovel | S / N |
| qtd_filhos | int |
| tipo_renda | str |
| educacao | str |
| estado_civil | str |
| tipo_residencia | str |
| idade | int |
| tempo_emprego | float (pode ser nulo) |
| qt_pessoas_residencia | float |
| renda | float |
