"""extract.py -- Extracao de dados de manifestacoes operacionais."""
import pandas as pd
from loguru import logger


def extract_from_csv(filepath: str) -> pd.DataFrame:
    """Le CSV de manifestacoes e retorna DataFrame bruto."""
    logger.info(f"Extraindo dados de: {filepath}")
    try:
        df = pd.read_csv(filepath, parse_dates=["data"])
        logger.success(f"{len(df)} registros carregados")
        return df
    except FileNotFoundError:
        logger.error(f"Arquivo nao encontrado: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Erro na extracao: {e}")
        raise