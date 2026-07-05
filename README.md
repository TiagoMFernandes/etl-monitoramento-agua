# ETL Pipeline - Monitoramento de Distribuicao de Agua

Pipeline ETL para coleta, transformacao e analise de dados operacionais de distribuicao de agua.

## Objetivo
Automatizar o fluxo de dados de manifestacoes e ocorrencias operacionais, gerando KPIs por setor.

## Arquitetura
```
CSV/API -> [Extract] -> [Transform] -> [Load] -> SQLite DB -> [SQL Analytics]
```

## Stack
| Camada | Tecnologia |
|--------|------------|
| Extracao | Python, Pandas |
| Transformacao | Pandas, NumPy |
| Carga | SQLite, SQLAlchemy |
| Analytics | SQL (CTEs, Window Functions) |
| Logging | Loguru |

## Como executar
```bash
git clone https://github.com/TiagoMFernandes/etl-monitoramento-agua
cd etl-monitoramento-agua
pip install -r requirements.txt
python src/pipeline.py
```

## KPIs gerados
- Volume de manifestacoes por setor e periodo
- Tempo medio de resolucao por tipo de ocorrencia
- Taxa de cumprimento de SLA por prioridade
- Setores criticos com maior indice de reclamacoes
- Ranking de desempenho por tecnico (Window Functions)
- Tendencia semanal com acumulado (Running Total)

## Contexto
Desenvolvido com base em experiencia pratica de monitoramento operacional de redes de distribuicao de agua em multiplos setores urbanos, com volume de 100 a 1000+ manifestacoes diarias.