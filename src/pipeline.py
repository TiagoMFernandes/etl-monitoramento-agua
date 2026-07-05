"""pipeline.py -- Orquestrador do ETL. Execute: python src/pipeline.py"""
import sys
from pathlib import Path
from loguru import logger

sys.path.insert(0, str(Path(__file__).parent))
from extract import extract_from_csv
from transform import transformar
from load import get_engine, criar_schema, carregar

logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")


def run(csv_path="data/manifestacoes_sample.csv"):
    logger.info("Iniciando Pipeline ETL -- Monitoramento de Agua")
    df_raw = extract_from_csv(csv_path)
    df, kpis = transformar(df_raw)
    engine = get_engine()
    criar_schema(engine)
    carregar(df, engine)
    logger.success("Pipeline concluido!")
    for k, v in kpis.items():
        logger.info(f"   {k}: {v}")
    return df, kpis


if __name__ == "__main__":
    run()