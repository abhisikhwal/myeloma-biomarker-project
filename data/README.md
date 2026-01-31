# Data Directory
## Multiple Myeloma Biomarker Discovery Project

---

## Directory Structure

```
data/
├── raw/                 # Original data from GDC (gitignored)
└── processed/           # Clean, analysis-ready data
    └── patient_level_clean.csv
```

---

## Raw Data (Not Tracked in Git)

### Data Source
- **Project:** MMRF-COMMPASS
- **Portal:** NCI Genomic Data Commons (https://portal.gdc.cancer.gov/)
- **Access Level:** Controlled (requires dbGaP authentication for raw sequencing)
- **Processed Counts:** Open-access

### Required Files
Place these files in `data/raw/` directory:

1. **clinical.tsv** - Patient demographics, ISS staging, survival
2. **follow_up.tsv** - Longitudinal follow-up data
3. **RNA-seq counts** - Gene expression data (HTSeq counts format)

### Download Instructions

**Option 1: GDC Data Portal (Web Interface)**
1. Visit: https://portal.gdc.cancer.gov/projects/MMRF-COMMPASS
2. Navigate to "Cases" → "Files"
3. Filter: Data Category = "Clinical" or "Transcriptome Profiling"
4. Download manifest file
5. Use GDC Data Transfer Tool

**Option 2: GDC Data Transfer Tool (Command Line)**
```bash
# Install GDC Client
# Download from: https://gdc.cancer.gov/access-data/gdc-data-transfer-tool

# Download using manifest
gdc-client download -m gdc_manifest.txt -d data/raw/
```

**Option 3: Python API**
```python
import requests
import json

# GDC API endpoint
endpoint = "https://api.gdc.cancer.gov/files"

# Query for MMRF files
params = {
    "filters": json.dumps({
        "op": "and",
        "content": [
            {"op": "=", "content": {"field": "cases.project.project_id", "value": "MMRF-COMMPASS"}},
            {"op": "=", "content": {"field": "data_category", "value": "Clinical"}}
        ]
    }),
    "size": "1000"
}

response = requests.get(endpoint, params=params)
files = response.json()["data"]["hits"]
```

---

## Processed Data (Tracked in Git)

### patient_level_clean.csv

**Description:** Clean, analysis-ready dataset with patient-level data

**Dimensions:** 859 patients × 112 columns

**Columns:**
- `case_id` - Unique patient identifier
- `age_years` - Age at diagnosis (years)
- `iss_stage` - ISS stage (I, II, III)
- `gender` - Male/Female
- `survival_months` - Overall survival time (months)
- `event` - Event indicator (1=death, 0=censored)
- `gene_1` to `gene_100` - Expression values for top 100 prognostic genes

**Data Processing:**
1. Merged clinical and RNA-seq data
2. Quality control (removed low-quality samples)
3. Normalization: log2(CPM + 1)
4. Feature selection: Top 100 genes by Random Forest importance
5. Patient-level aggregation (one row per patient)

**Usage:**
```python
import pandas as pd

# Load processed data
df = pd.read_csv('data/processed/patient_level_clean.csv')

# Check shape
print(f"Patients: {df.shape[0]}, Features: {df.shape[1]}")

# Split features and labels
X = df[[col for col in df.columns if col.startswith('gene_')]]
y = df['iss_stage']
```

---

## Data Statistics

### Cohort Characteristics

| Characteristic | Value |
|----------------|-------|
| Total Patients | 859 |
| ISS Stage I | 308 (35.9%) |
| ISS Stage II | 335 (39.0%) |
| ISS Stage III | 216 (25.1%) |
| Median Age | 63.4 years (range: 28-90) |
| Male | 517 (60.2%) |
| Female | 342 (39.8%) |
| Deaths | 191 (22.2%) |
| Median Follow-up | 2.8 years |

### Gene Expression Data

| Statistic | Value |
|-----------|-------|
| Total Genes (Raw) | 30,018 |
| Genes After QC | 30,018 |
| Genes in Analysis | 100 (feature selection) |
| Normalization | log2(CPM + 1) |
| Expression Range | 0 to ~15 (log2 scale) |

---

## Data Quality Control

### Sample QC Metrics
- **Minimum read count:** >10 million reads
- **Mapping rate:** >80%
- **Ribosomal RNA:** <20%
- **Duplicate rate:** <50%

### Exclusions
- Low read count: 12 samples
- Failed QC: 8 samples
- Missing clinical data: 23 samples

**Final cohort:** 859 patients with complete data

---

## Data Usage Notes

### Privacy & Ethics
- Data from consented research participants
- De-identified patient information
- Comply with MMRF data usage agreements
- Cite CoMMpass study in publications

### Recommended Citation
```
Data were obtained from the Multiple Myeloma Research Foundation (MMRF)
Relating Clinical Outcomes in MM to Personal Assessment of Genetic Profile
(CoMMpass) study (ClinicalTrials.gov identifier: NCT01454297), accessed via
the NCI Genomic Data Commons (https://portal.gdc.cancer.gov/).
```

### Data Availability Statement
```
Raw sequencing data are available through controlled access at the NCI Genomic
Data Commons (https://portal.gdc.cancer.gov/, project ID: MMRF-COMMPASS).
Processed data used in this analysis are available in this repository at
data/processed/patient_level_clean.csv.
```

---

## Contact

For questions about data processing or access:

**[Your Name]**  
Email: [your.email@institution.edu]  
GitHub: https://github.com/[your-username]/myeloma-biomarker-project

---

**Last Updated:** January 2026
