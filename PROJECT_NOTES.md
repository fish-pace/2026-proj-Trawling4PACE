# Project Notes / Message Board (2026-proj-Trawling4PACE)

This file is a shared place for **all participants** to leave short notes, updates, and reminders.
Please add your message under **Today’s notes** or create a dated section.

---

## Important repo note: local data is ignored

The repository includes a `.gitignore` rule for:

- `/data/`

Reason: CSV files in `./data` can be very large (some exceed GitHub’s size limits).  
Please keep large datasets **local** (or use an external data store such as Zenodo, S3, Drive, or Git LFS if the project decides to adopt it).

---

## Tool update (Leandro): Trawling4PACE Explorer v2.1

I added a Jupyter Notebook called **“Trawling4PACE Explorer – v2.1”** to explore the CSV files located in `./data`.

### What the tool does
**Trawling4PACE Explorer** is an interactive dashboard inside a Jupyter Notebook for exploring bottom trawl survey data and environmental variables:

- **Loads CSV files** and auto-detects latitude/longitude columns
- Provides **filters** (species, year, month, depth)
- Supports **up to 4 map layers** simultaneously (scatter or density), each with:
  - Independent opacity/transparency
  - Plotly and **CMOcean** colorscales
  - Linear or **log scale** color mapping
- **Reactive updates** (changes apply automatically)
- Includes a **loading indicator** and a **Cancel** button for long operations
- Disables controls during rendering to prevent race conditions
- Computes an **auto bounding box** (with a 2° margin) for quick framing
- Compatible with **2i2c JupyterHub** and the **Plotly MapLibre API** (no deprecation warnings)

### Smart defaults on file load
On load, the notebook tries to pick sensible defaults, e.g.:
- `SURFTEMP` as an environmental/density layer (thermal colormap)
- `EXPCATCHWT` as a catch/scatter layer (haline colormap, log scale)

Author: **Leandro (USP/IEAPM)**  
Project: **2026-proj-Trawling4PACE / NASA PACE Hackweek 2026**

---

## Today’s notes
- YYYY-MM-DD — _Add your message here_

