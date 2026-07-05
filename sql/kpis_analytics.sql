-- Analytics: KPIs de Monitoramento de Agua

-- 1. Volume e SLA por setor (ultimos 30 dias)
SELECT setor, COUNT(*) AS total,
    SUM(CASE WHEN status='Resolvido' THEN 1 ELSE 0 END) AS resolvidos,
    ROUND(AVG(tempo_resolucao_h), 2) AS tempo_medio_h,
    ROUND(SUM(dentro_sla)*100.0/COUNT(*), 1) AS taxa_sla_pct
FROM fato_manifestacoes
WHERE data >= DATE('now','-30 days')
GROUP BY setor ORDER BY total DESC;

-- 2. Ranking de tecnicos com Window Functions
WITH stats AS (
    SELECT tecnico_responsavel,
        COUNT(*) AS atendimentos,
        ROUND(AVG(tempo_resolucao_h), 2) AS tempo_medio_h,
        ROUND(SUM(dentro_sla)*100.0/COUNT(*), 1) AS taxa_sla_pct
    FROM fato_manifestacoes WHERE status='Resolvido'
    GROUP BY tecnico_responsavel
)
SELECT *,
    RANK() OVER (ORDER BY taxa_sla_pct DESC) AS rank_sla,
    RANK() OVER (ORDER BY tempo_medio_h ASC)  AS rank_velocidade
FROM stats ORDER BY taxa_sla_pct DESC;

-- 3. Tendencia semanal com Running Total
SELECT semana, ano, COUNT(*) AS ocorrencias,
    SUM(COUNT(*)) OVER (PARTITION BY ano ORDER BY semana ROWS UNBOUNDED PRECEDING) AS acumulado
FROM fato_manifestacoes GROUP BY semana, ano ORDER BY ano, semana;

-- 4. Alertas de SLA vencido
SELECT setor, tipo_ocorrencia, COUNT(*) AS fora_sla,
    ROUND(AVG(desvio_sla_h), 2) AS desvio_medio_h
FROM fato_manifestacoes WHERE dentro_sla=0
GROUP BY setor, tipo_ocorrencia HAVING fora_sla >= 2
ORDER BY desvio_medio_h DESC;