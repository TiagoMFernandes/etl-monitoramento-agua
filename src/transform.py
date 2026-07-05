"""transform.py -- Transformacao e enriquecimento dos dados."""
import pandas as pd
from loguru import logger

SLA_HORAS = {"Critica": 2.0, "Alta": 6.0, "Media": 12.0, "Baixa": 24.0}


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicatas, trata nulos e padroniza strings."""
    logger.info("Limpando dados...")
    df = df.drop_duplicates(subset=["id_manifestacao"])
    df["tecnico_responsavel"] = df["tecnico_responsavel"].fillna("Nao_atribuido")
    df["prioridade"] = df["prioridade"].fillna("Media")
    df["tempo_resolucao_h"] = df["tempo_resolucao_h"].fillna(df["tempo_resolucao_h"].median())
    df["setor"] = df["setor"].str.strip().str.upper()
    return df


def enriquecer_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas calculadas para analise."""
    logger.info("Enriquecendo dataset...")
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["semana"] = df["data"].dt.isocalendar().week.astype(int)
    df["dia_semana"] = df["data"].dt.day_name()
    df["sla_horas"] = df["prioridade"].map(SLA_HORAS)
    df["dentro_sla"] = (df["tempo_resolucao_h"] <= df["sla_horas"]).astype(int)
    df["desvio_sla_h"] = df["tempo_resolucao_h"] - df["sla_horas"]
    df["critico"] = df["prioridade"].isin(["Critica", "Alta"]).astype(int)
    return df


def calcular_kpis(df: pd.DataFrame) -> dict:
    """Calcula KPIs principais do periodo."""
    total = len(df)
    resolvidos = (df["status"] == "Resolvido").sum()
    return {
        "total_manifestacoes": total,
        "taxa_resolucao_pct": round(resolvidos / total * 100, 1),
        "taxa_sla_pct": round(df["dentro_sla"].sum() / total * 100, 1),
        "tempo_medio_resolucao_h": round(df["tempo_resolucao_h"].mean(), 2),
        "setor_mais_critico": df.groupby("setor")["critico"].sum().idxmax(),
        "tipo_mais_frequente": df["tipo_ocorrencia"].value_counts().index[0],
    }


def transformar(df: pd.DataFrame):
    df = limpar_dados(df)
    df = enriquecer_dados(df)
    kpis = calcular_kpis(df)
    return df, kpis