# Biomarker Discovery in Multiple Myeloma Progression

## Overview

This project analyzes clinical and genomic data from the Multiple Myeloma Research Foundation (MMRF) CoMMpass study to identify potential biomarkers associated with disease progression from Monoclonal Gammopathy of Undetermined Significance (MGUS) to Multiple Myeloma (MM). The goal is to develop predictive models that can identify high-risk patients and inform treatment strategies.

> **Note:** This project is part of my PhD application portfolio in cancer research, demonstrating proficiency in bioinformatics analysis, statistical methods, and reproducible research practices.

## Project Structure

```
myeloma-biomarker-project/
│
├── data/
│   ├── raw/              # Original data files (not tracked in git)
│   └── processed/        # Cleaned and processed data
│
├── notebooks/
│   └── 01_explore_clinical_data.ipynb    # Initial exploratory analysis
│
├── src/
│   └── data_loader.py    # Data loading and preprocessing utilities
│
├── results/
│   ├── figures/          # Generated plots and visualizations
│   ├── tables/           # Summary statistics and results tables
│   └── models/           # Trained models and model outputs
│
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository:**
```bash
git clone <repository-url>
cd myeloma-biomarker-project
```

2. **Create a virtual environment (recommended):**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required packages:**
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Prepare Your Data

Place your MMRF CoMMpass data files in the `data/raw/` directory:
- `clinical.tsv`
- `exposure.tsv`
- `family_history.tsv`
- `follow_up.tsv`
- `pathology_detail.tsv`

### 2. Launch Jupyter

```bash
jupyter lab
```

### 3. Start with Exploratory Analysis

Open and run `notebooks/01_explore_clinical_data.ipynb` to:
- Load and examine clinical data
- Understand data distributions
- Identify missing values
- Create basic visualizations

### 4. Use Data Loading Utilities

```python
from src.data_loader import load_clinical_files, merge_clinical_data

# Load all clinical files
data_dict = load_clinical_files('data/raw/')

# Merge into a single dataframe
merged_df = merge_clinical_data(data_dict)
```

## Data Source

This project uses data from the **MMRF CoMMpass Study** (Relating Clinical Outcomes in Multiple Myeloma to Personal Assessment of Genetic Profile). Data can be accessed through:
- [Database of Genotypes and Phenotypes (dbGaP)](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000748)
- [MMRF Researcher Gateway](https://research.themmrf.org/)

## Analysis Pipeline (In Development)

- [x] Project setup and data loading
- [ ] Clinical data exploration and quality control
- [ ] Survival analysis (Kaplan-Meier, Cox regression)
- [ ] Feature engineering and biomarker selection
- [ ] Machine learning models for progression prediction
- [ ] Results interpretation and visualization

## Contributing

This is an educational project for PhD application purposes. Feedback and suggestions are welcome!

## License

This project is for educational and research purposes. Please ensure you comply with the MMRF data usage agreements and cite the CoMMpass study appropriately in any publications.

## Contact

For questions about this analysis, please contact me through my GitHub profile.

---

**Disclaimer:** This is an independent analysis for educational purposes and is not affiliated with or endorsed by the Multiple Myeloma Research Foundation.
