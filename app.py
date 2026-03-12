import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA

# ── Classes do pipeline (necessárias para carregar o pickle) ──────────────────

num_cols_pipe = ['qtd_filhos', 'idade', 'tempo_emprego', 'qt_pessoas_residencia', 'renda']
cat_cols_pipe = ['sexo', 'posse_de_veiculo', 'posse_de_imovel',
                 'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia']

class ImputadorMisto(BaseEstimator, TransformerMixin):
    def __init__(self, num_cols, cat_cols):
        self.num_cols = num_cols
        self.cat_cols = cat_cols

    def fit(self, X, y=None):
        X = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X
        self.medianas_ = X[self.num_cols].median()
        self.modas_    = X[self.cat_cols].mode().iloc[0]
        return self

    def transform(self, X, y=None):
        X = X.copy()
        for col in self.num_cols:
            X[col] = X[col].fillna(self.medianas_[col])
        for col in self.cat_cols:
            X[col] = X[col].fillna(self.modas_[col])
        return X


class WinsorizadorOutliers(BaseEstimator, TransformerMixin):
    def __init__(self, num_cols, p_low=0.01, p_high=0.99):
        self.num_cols = num_cols
        self.p_low    = p_low
        self.p_high   = p_high

    def fit(self, X, y=None):
        X = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X
        self.lower_ = X[self.num_cols].quantile(self.p_low)
        self.upper_ = X[self.num_cols].quantile(self.p_high)
        return self

    def transform(self, X, y=None):
        X = X.copy()
        for col in self.num_cols:
            X[col] = X[col].clip(self.lower_[col], self.upper_[col])
        return X


class CriadorDummies(BaseEstimator, TransformerMixin):
    def __init__(self, cat_cols):
        self.cat_cols = cat_cols

    def fit(self, X, y=None):
        X = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X
        self.encoder_ = OneHotEncoder(
            sparse_output=False, handle_unknown='ignore', drop='first')
        self.encoder_.fit(X[self.cat_cols])
        self.other_cols_ = [c for c in X.columns if c not in self.cat_cols]
        return self

    def transform(self, X, y=None):
        X = pd.DataFrame(X) if not isinstance(X, pd.DataFrame) else X
        dummies = pd.DataFrame(
            self.encoder_.transform(X[self.cat_cols]),
            columns=self.encoder_.get_feature_names_out(self.cat_cols),
            index=X.index)
        return pd.concat([X[self.other_cols_].reset_index(drop=True),
                          dummies.reset_index(drop=True)], axis=1)


class AplicadorPCA(BaseEstimator, TransformerMixin):
    def __init__(self, n_components=5):
        self.n_components = n_components

    def fit(self, X, y=None):
        self.pca_ = PCA(n_components=self.n_components, random_state=42)
        self.pca_.fit(X)
        return self

    def transform(self, X, y=None):
        return self.pca_.transform(X)


# ── Aplicação Streamlit ───────────────────────────────────────────────────────

st.set_page_config(page_title="Credit Scoring", page_icon="💳", layout="wide")
st.title("💳 Credit Scoring — Escoragem de Crédito")
st.markdown("Faça upload de um CSV e obtenha a probabilidade de inadimplência para cada cliente.")

@st.cache_resource
def carregar_modelo():
    with open("model_final.pkl", "rb") as f:
        return pickle.load(f)

model = carregar_modelo()

st.sidebar.header("📂 Carregar dados")
arquivo = st.sidebar.file_uploader("Selecione um arquivo CSV", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)
    st.subheader("Pré-visualização dos dados")
    st.dataframe(df.head(10))
    st.info(f"Total de registros: {len(df):,}")

    colunas_remover = [c for c in ["data_ref", "index", "mau"] if c in df.columns]
    X = df.drop(columns=colunas_remover)

    if st.sidebar.button("🚀 Escorar base"):
        with st.spinner("Calculando scores..."):
            try:
                probs = model.predict_proba(X)[:, 1]
                df_resultado = df.copy()
                df_resultado["score_mau"] = probs.round(4)
                df_resultado["classificacao"] = np.where(probs >= 0.5, "Mau", "Bom")

                st.subheader("✅ Resultado da escoragem")
                st.dataframe(df_resultado)

                col1, col2, col3 = st.columns(3)
                col1.metric("Total de clientes", f"{len(df_resultado):,}")
                col2.metric("% Previstos como Mau",
                            f"{(df_resultado['classificacao']=='Mau').mean():.1%}")
                col3.metric("Score médio", f"{probs.mean():.4f}")

                csv_resultado = df_resultado.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Baixar resultado em CSV",
                                   data=csv_resultado,
                                   file_name="resultado_scoring.csv",
                                   mime="text/csv")

                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(probs, bins=40, color="steelblue", edgecolor="white")
                ax.axvline(0.5, color="red", linestyle="--", label="Threshold 0.5")
                ax.set_xlabel("Probabilidade de Inadimplência")
                ax.set_ylabel("Frequência")
                ax.set_title("Distribuição dos Scores")
                ax.legend()
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Erro ao escorar a base: {e}")
else:
    st.info("⬅️ Faça upload de um CSV na barra lateral para começar.")
    st.markdown("""
### Colunas esperadas no CSV:
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
    """)
