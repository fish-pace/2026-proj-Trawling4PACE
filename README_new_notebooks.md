# 🛰️🐟 Trawling4PACE Toolkit

**Interactive ML pipeline for correlating NASA PACE ocean color products with bottom trawl survey data.**

> NASA PACE Hackweek 2026

---

## 📦 Notebooks Incluídos

| Notebook | Função |
|----------|--------|
| `download_pace_earthdata.ipynb` | Download de produtos PACE via EarthAccess |
| `pace_preprocessor_gui.ipynb` | Composição temporal e matching espacial |
| `ml_prediction_dashboard_autorun.ipynb` | Treinamento de modelos ML + SHAP |
| `ml_model_comparison_dashboard.ipynb` | Comparação e ranking de modelos |

---

## 🔑 Conceitos Importantes

### 1. Janela Temporal (±4 dias) — Composite Mode

**O problema:** Dados de satélite têm cobertura espacial incompleta devido a nuvens, glint solar, e geometria de órbita. Em um único dia, muitas estações de arrasto podem não ter dado PACE correspondente.

**A solução:** O modo **Composite** busca dados em uma janela de ±4 dias ao redor da data-alvo:

```
Data do arrasto: 2024-06-15

Busca no composite (prioridade):
  1. 2024-06-15 (data exata)           ← prioridade máxima
  2. 2024-06-14, 2024-06-16            ← ±1 dia
  3. 2024-06-13, 2024-06-17            ← ±2 dias
  4. 2024-06-12, 2024-06-18            ← ±3 dias
  5. 2024-06-11, 2024-06-19            ← ±4 dias (limite)
```

**Quando usar qual:**
- **Daily:** Análises que exigem correspondência temporal estrita (ex: validação de algoritmos)
- **Composite:** Maximizar cobertura espacial para ML (recomendado para a maioria dos casos)

> ⚠️ A janela de 4 dias é configurável no código (`TEMPORAL_WINDOW = 4`)

---

### 2. Tratamento de NaN — Qual Modelo Usar?

Dados oceanográficos sempre têm valores faltantes (nuvens, terra, flags de qualidade). Nem todos os modelos lidam bem com isso:

| Modelo | Aceita NaN? | Notas |
|--------|-------------|-------|
| **HistGradientBoosting** | ✅ Sim | Trata NaN nativamente como uma categoria separada |
| RandomForest | ❌ Não | Requer imputação prévia |
| GradientBoosting | ❌ Não | Requer imputação prévia |
| ExtraTrees | ❌ Não | Requer imputação prévia |
| AdaBoost | ❌ Não | Requer imputação prévia |
| Ridge/Lasso/ElasticNet | ❌ Não | Requer imputação prévia |
| KNN | ❌ Não | Requer imputação prévia |
| MLP (Neural Network) | ❌ Não | Requer imputação prévia |

**Recomendação:** Para dados com muitos NaN, comece com **HistGradientBoosting**. É robusto e geralmente performa bem sem necessidade de pré-processamento complexo.

O dashboard aplica automaticamente **imputação por mediana** para modelos que não aceitam NaN.

---

### 3. Estratégias de Split — Evitando Overfitting

Este é um conceito crítico para dados oceanográficos com autocorrelação espaço-temporal.

#### 🏝️ O Conceito de "Ilhas Temporais"

Dados de cruzeiros oceanográficos vêm em "ilhas" — períodos contíguos de coleta separados por gaps (mudança de área, mau tempo, etc.):

```
Ilha 1          Ilha 2              Ilha 3
[===]    gap    [=======]    gap    [====]
Jun 1-3         Jun 10-17           Jun 25-28
```

Amostras dentro da mesma ilha são **autocorrelacionadas** — usar uma para treinar e outra (muito próxima) para testar causa **data leakage**.

#### As 3 Estratégias Disponíveis

| Estratégia | Pasta de Saída | Descrição | Risco de Overfitting |
|------------|----------------|-----------|----------------------|
| `random` | `overfit/` | Split aleatório por amostra | 🔴 **Alto** — amostras vizinhas podem ir para train e test |
| `random_islands` | `random/` | Ilhas inteiras vão para train OU test | 🟡 Médio — sem leakage intra-ilha, mas pode ter ilhas temporalmente próximas em train e test |
| `max_distance` | `max_time_dist/` | Maximiza distância temporal entre train e test | 🟢 **Baixo** — melhor para generalização real |

#### Visualização do Split

O dashboard gera um gráfico mostrando a distribuição temporal das ilhas:

```
TRAIN (azul)  ████████░░░░████████░░░░████████
TEST (vermelho)       ████        ████        ████
              ───────────────────────────────────→ tempo
```

**Métricas importantes:**
- **Avg Distance:** Distância temporal média entre ilhas de train e test
- **Min Distance:** Menor distância (quanto maior, melhor)

---

### 4. Detecção de Overfitting — R² Gap

O dashboard calcula automaticamente o **R² Gap**:

```
R² Gap = R²_train - R²_test
```

| R² Gap | Interpretação |
|--------|---------------|
| < 0.05 | ✅ Excelente generalização |
| 0.05 - 0.15 | ⚠️ Overfitting moderado |
| > 0.15 | 🔴 Overfitting severo — modelo memorizou o treino |

**Exemplo:**
```
HistGradientBoosting:  R²_train=0.85, R²_test=0.78  → Gap=0.07 ✅
RandomForest:          R²_train=0.99, R²_test=0.65  → Gap=0.34 🔴
```

O RandomForest com R² de 0.99 no treino parece bom, mas generalizou muito pior. Prefira modelos com gap baixo.

---

### 5. Gap de Detecção de Ilhas (gap_hours)

O parâmetro `gap_hours=24` define o que constitui uma "quebra" entre ilhas:

```python
gap_hours=24  # Gap > 24h = nova ilha
```

Se seus dados têm coletas diárias mas com gaps ocasionais de 12h:
- `gap_hours=24` → agrupa dias consecutivos na mesma ilha
- `gap_hours=6` → separa mais agressivamente

**Para cruzeiros típicos de arrasto:** 24h funciona bem.

---

### 6. SHAP — Interpretação de Features

O dashboard gera análise SHAP (SHapley Additive exPlanations) para entender quais variáveis PACE são mais importantes:

- **Summary Plot:** Ranking de importância das features
- **Beeswarm:** Distribuição do impacto de cada feature

**Interpretação:**
- Features no topo têm maior impacto nas predições
- Cor vermelha = valores altos da feature
- Posição à direita = aumenta a predição

---

## 🚀 Workflow Recomendado

```
1. download_pace_earthdata.ipynb
   └── Baixar produtos PACE para região/período do cruzeiro

2. pace_preprocessor_gui.ipynb
   └── Gerar composites (±4 dias) para datas das estações
   └── Modo: COMPOSITE (não Daily)

3. ml_prediction_dashboard_autorun.ipynb
   └── Carregar CSV com dados de arrasto + features PACE
   └── Rodar com split_strategy = "max_distance"
   └── Começar com HistGradientBoosting (aceita NaN)

4. ml_model_comparison_dashboard.ipynb
   └── Comparar todos os modelos
   └── Verificar R² gap e escolher o melhor
```

---

## 📁 Estrutura de Saída

```
results/
├── max_time_dist/          ← Split com máxima distância temporal
│   ├── HistGradientBoosting/
│   │   ├── *_metrics.csv
│   │   ├── *_predictions.csv
│   │   ├── *_feature_importance.csv
│   │   └── figures/
│   ├── RandomForest/
│   └── ...
├── random/                 ← Split aleatório por ilhas
└── overfit/                ← Split aleatório (cuidado!)
```

---

## ⚠️ Troubleshooting

### "No PACE files found"
Verifique se os arquivos seguem o padrão: `pace_{product}_{YYYYMMDD}.nc`

### "All NaN values in feature X"
O composite não encontrou dados válidos na janela de ±4 dias. Considere aumentar `TEMPORAL_WINDOW` ou verificar cobertura de nuvens.

### R² negativo no teste
O modelo é pior que a média. Causas comuns:
- Features não correlacionadas com o target
- Overfitting extremo
- Dados de teste muito diferentes do treino

### SHAP muito lento
Para datasets grandes, SHAP calcula em uma subamostra. Se ainda lento, desabilite nas opções.

---

## 📚 Referências

- [NASA PACE Mission](https://pace.gsfc.nasa.gov/)
- [EarthAccess Documentation](https://earthaccess.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [scikit-learn Regressors](https://scikit-learn.org/stable/supervised_learning.html)

---

*Trawling4PACE — NASA PACE Hackweek 2026*
