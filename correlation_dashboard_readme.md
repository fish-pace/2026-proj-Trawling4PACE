# Correlation Dashboard for Trawling4PACE

## Overview

This interactive Jupyter notebook (`correlation_dashboard.ipynb`) automatically matches **environmental satellite/model data** with **in-situ trawl survey observations**, generating correlation analyses and a **paired DataFrame ready for Gradient Boosting**.

---

## How It Works

### The Magic: Automatic Detection & Pairing

Simply organize your data like this:

```
data/
├── filtered_bts.csv              # Trawl survey (biological + observed environmental)
│
├── fsle/                         # ← Just create a folder with NetCDFs
│   ├── fsle_20240307.nc
│   ├── fsle_20240308.nc
│   └── ...
│
├── curl/                         # ← Another folder = another variable source
│   ├── cmems_wind_20240307.nc
│   └── ...
│
├── glorys/                       # ← 3D data works too (auto-detects depth)
│   ├── glorys_20240307.nc
│   └── ...
│
└── [any_new_folder]/             # ← Add more anytime!
    └── your_data_YYYYMMDD.nc
```

**The dashboard will automatically:**

1. **Scan** all subfolders inside `data/`
2. **Detect** variables, date range, depth levels, and longitude convention
3. **Match** each CSV row (lat/lon/date) with the corresponding NetCDF file
4. **Interpolate** environmental values to the exact trawl location
5. **Pair** everything into a single DataFrame
6. **Output** correlation matrix + ready-to-use data for Gradient Boosting

---

## Input Data

### CSV: Trawl Survey Data (`filtered_bts.csv`)

Contains biological catch data AND observed environmental measurements from the survey:

| Column | Description |
|--------|-------------|
| `DECDEG_BEGLAT`, `DECDEG_BEGLON` | Trawl location |
| `BEGIN_GMT_TOWDATE` | Date/time |
| `SURFTEMP`, `BOTTEMP` | **Observed** surface/bottom temperature |
| `SURFSALIN`, `BOTSALIN` | **Observed** surface/bottom salinity |
| `EXPCATCHNUM`, `EXPCATCHWT` | Catch (number/weight) |
| `SCIENTIFIC_NAME` | Species |

### NetCDF: Environmental Model/Satellite Data

Each subfolder in `data/` is treated as a **variable source**. Requirements:

- Files named with date: `*YYYYMMDD*.nc` (e.g., `fsle_20240307.nc`)
- Standard coordinates: `lat`/`latitude`, `lon`/`longitude`
- Optional: `time`, `depth` dimensions (auto-handled)

**Currently available (pre-downloaded):**

| Folder | Source | Variables | Purpose |
|--------|--------|-----------|---------|
| `fsle/` | AVISO | `fsle_max` | Lagrangian transport barriers |
| `curl/` | CMEMS Wind | `stress_curl` | Ekman upwelling indicator |
| `glorys/` | GLORYS12 | `thetao`, `so`, `bottomT`, `mlotst`, `uo`, `vo` | 3D ocean state |

🔗 **Pre-downloaded data:** https://drive.google.com/drive/folders/1p31TMjK4KRlffTHu4MXMVlUBr5EQDfqx

---

## Output: Ready for Gradient Boosting

The dashboard produces a **paired DataFrame** where each row is a trawl observation with all environmental covariates interpolated to that exact location and date:

```
correlation_data.csv
─────────────────────────────────────────────────────────────────────────
DECDEG_BEGLAT | DECDEG_BEGLON | DATE       | BOTTEMP | SURFTEMP | EXPCATCHNUM_log | fsle_fsle_max | curl_stress_curl | glorys_mlotst_surface | glorys_thetao_surface_grad
──────────────┼───────────────┼────────────┼─────────┼──────────┼─────────────────┼───────────────┼──────────────────┼───────────────────────┼──────────────────────────
39.929        | -73.412       | 2024-03-22 | 7.05    | 7.03     | 1.146           | 0.082         | -1.91e-07        | 23.7                  | 0.0012
39.785        | -73.551       | 2024-03-22 | 7.12    | 7.08     | 2.301           | 0.045         | -2.05e-07        | 25.1                  | 0.0008
...
```

This DataFrame goes directly into Gradient Boosting to predict catch from environmental conditions.

---

## Adding New Data Sources

Want to add bathymetry? Chlorophyll? Any other variable?

1. Create a folder: `data/bathymetry/`
2. Put NetCDF files inside: `bathymetry_20240307.nc` (or just `bathymetry.nc` for static data)
3. Click **"Scan Folders"** in the dashboard
4. Select your new variables
5. Done!

The dashboard handles:
- ✅ Different longitude conventions (0-360° vs -180-180°)
- ✅ Data with/without time dimension
- ✅ 2D and 3D variables (with depth selection)
- ✅ Missing dates (finds nearest within 7 days)

---

## Key Features

### Pairwise Correlation
Each variable pair uses only points where BOTH have valid data. Sample size `n` shown in every cell.

### Horizontal Gradient (∇)
Extract **front intensity** instead of raw values:
```
|∇T| = sqrt((∂T/∂x)² + (∂T/∂y)²)   [°C/km]
```
Useful for detecting thermal/salinity fronts where fish aggregate.

### Observed vs Modeled
The CSV already contains **observed** temperature and salinity from the trawl survey. Use these with higher weight in Gradient Boosting! Model data is useful for:
- Variables not observed (mixed layer depth, FSLE)
- Spatial gradients
- Gap-filling

---

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────────────────┐
│  1. PREPARE                                                             │
│     data/                                                               │
│     ├── filtered_bts.csv    ← biological + observed env                 │
│     ├── fsle/               ← satellite Lagrangian                      │
│     ├── curl/               ← wind stress                               │
│     └── glorys/             ← model reanalysis                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  2. RUN correlation_dashboard.ipynb                                     │
│     • Scan folders → auto-detects all variables                         │
│     • Select what you want to analyze                                   │
│     • Extract → interpolates to each trawl point                        │
│     • Plot → see correlations                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│  3. OUTPUT                                                              │
│     • correlation_matrix.png      ← visualization                       │
│     • correlation_metrics.csv     ← r, r², p-values                     │
│     • correlation_data.csv        ← PAIRED DATAFRAME → Gradient Boost   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
# 1. Download pre-processed environmental data
# From: https://drive.google.com/drive/folders/1p31TMjK4KRlffTHu4MXMVlUBr5EQDfqx

# 2. Place in data/ folder
mv ~/Downloads/fsle ~/Downloads/curl ~/Downloads/glorys data/

# 3. Run notebook
jupyter notebook correlation_dashboard.ipynb

# 4. Use the output for Gradient Boosting
# → correlation_data.csv is ready!
```

---

## Environmental Variables Explained

### FSLE (Finite-Size Lyapunov Exponents)
Measures Lagrangian transport barriers — regions where water parcels are "trapped" by submesoscale stirring. High FSLE = strong fronts and filaments that concentrate prey.

### Wind Stress Curl
Positive curl → Ekman upwelling → nutrients rise → phytoplankton bloom → trophic cascade. This drives the **90-day trophic memory** in our LAG-FISH hypothesis.

### GLORYS Variables
- `mlotst`: Mixed layer depth — stratification indicator
- `thetao`: Temperature (use gradient for fronts)
- `so`: Salinity (water mass identification)
- `bottomT`: Bottom temperature for demersal species

---

## Questions?

Ping @leandro on Slack or open an issue!
