"""load.py -- Carga no banco SQLite via SQLAlchemy."""
import pandas as pd
from sqlalchemy import create_engine, text
from loguru import logger
from pathlib import Path

DB_PATH = "data/operacional.db"


def get_engine():
    Path("data").mkdir(exist_ok=True)
    return create_engine(f"sqlite:///{DB_PATH}", echo=False)


def criar_schema(engine):
    logger.info("Criando schema...")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS fato_manifestacoes (
                id_manifestacao INTEGER PRIMARY KEY,
                data DATE, setor TEXT, tipo_ocorrencia TEXT, status TEXT,
                tempo_resolucao_h REAL, tecnico_responsavel TEXT, prioridade TEXT,
                ano INTEGER, mes INTEGER, semana INTEGER, dia_semana TEXT,
                sla_horas REAL, dentro_sla INTEGER, desvio_sla_h REAL, critico INTEGER
            )
        """))
        conn.commit()


def carregar(df: pd.DataFrame, engine, modo="replace"):
    cols = ["id_manifestacao","data","setor","tipo_ocorrencia","status",
            "tempo_resolucao_h","tecnico_responsavel","prioridade",
            "ano","mes","semana","dia_semana","sla_horas","dentro_sla","desvio_sla_h","critico"]
    df[cols].to_sql("fato_manifestacoes", engine, if_exists=modo, index=False)
    logger.success(f"{len(df)} registros carregados")