-- DDL: Criacao das tabelas do banco operacional

CREATE TABLE IF NOT EXISTS fato_manifestacoes (
    id_manifestacao   INTEGER PRIMARY KEY,
    data              DATE NOT NULL,
    setor             TEXT NOT NULL,
    tipo_ocorrencia   TEXT NOT NULL,
    status            TEXT NOT NULL,
    tempo_resolucao_h REAL,
    tecnico_responsavel TEXT,
    prioridade        TEXT,
    ano INTEGER, mes INTEGER, semana INTEGER, dia_semana TEXT,
    sla_horas REAL, dentro_sla INTEGER, desvio_sla_h REAL, critico INTEGER
);

CREATE INDEX IF NOT EXISTS idx_data   ON fato_manifestacoes(data);
CREATE INDEX IF NOT EXISTS idx_setor  ON fato_manifestacoes(setor);
CREATE INDEX IF NOT EXISTS idx_status ON fato_manifestacoes(status);