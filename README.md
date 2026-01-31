# Multiple Myeloma Biomarker Discovery

Comprehensive computational analysis of multiple myeloma progression using integrated bioinformatics and machine learning approaches on the MMRF CoMMpass dataset (859 patients, 30,018 genes).

## Overview

This project identifies molecular biomarkers of disease progression through multi-modal analysis combining differential expression, pathway enrichment, gene set enrichment analysis (GSEA), machine learning, deep learning, and unsupervised clustering.

**Key Discovery:** MYC-driven cell cycle dysregulation (G2-M checkpoint, E2F targets) and metabolic reprogramming (MTHFD2, glycolysis) characterize Stage III disease progression.

## Dataset

- **Source:** MMRF CoMMpass Study
- **Patients:** 859 (Stage I: 308, Stage II: 335, Stage III: 216)
- **Data:** RNA-seq (30,018 genes), clinical outcomes
- **Follow-up:** Median 2.8 years

## Key Results

### Differential Expression
- 6,356 significantly dysregulated genes (FDR < 0.05)
- Top upregulated: MYC, MTHFD2, CKS2, CCNB1, CDK1
- Pattern: Hyperproliferative, biosynthetic state in Stage III

### Pathway Enrichment
- 417 GO Biological Process terms enriched
- 72 KEGG pathways significant
- Top pathways: Cell cycle, ribosome, glycolysis, one-carbon metabolism

### Gene Set Enrichment Analysis (GSEA)
- G2-M Checkpoint: NES = 2.897, FDR < 0.001
- E2F Targets: NES = 2.628, FDR < 0.001
- Coordinated upregulation of entire pathways, not just individual genes

### Machine Learning
- Logistic Regression: AUC = 0.874 (best model)
- SHAP analysis top predictors: MYC (#1), MTHFD2 (#2), CKS2, CDK1, CCNB1
- Risk stratification: 3 groups with distinct survival outcomes
- ML predictions match pathway enrichment findings

### Deep Learning
- Neural network (PyTorch): 93.8% accuracy
- Perfect Stage III detection: 100% sensitivity (32/32 patients)
- Architecture: 256→128→64 neurons with batch norm and dropout
- Outperforms classical ML, demonstrates nonlinear gene interactions

### Unsupervised Learning
- 4 molecular subtypes identified (K-means clustering)
- Stage II heterogeneity: 173 patients split into 3 molecular groups
- UMAP provides superior visualization vs PCA/t-SNE
- Clusters correlate with survival outcomes (1.55–2.95 years median)

## Cross-Method Validation

All approaches independently converge on same biology:

| Finding | Pathway Enrichment | GSEA | ML (SHAP) | Deep Learning | Clustering |
|---------|-------------------|------|-----------|---------------|------------|
| MYC pathway | ✓ | E2F targets (NES=2.6) | #1 predictor | Classifies Stage III | Defines subtypes |
| Cell cycle | ✓ | G2-M checkpoint (NES=2.9) | CDK1, CCNB1 top 5 | 100% Stage III recall | Cluster 0 signature |
| Metabolism | ✓ | - | MTHFD2 #2 predictor | - | Cluster separation |

## Repository Structure

```
myeloma-biomarker-project/
├── notebooks/              # Jupyter analysis notebooks (01-09)
│   ├── 01_clinical_analysis.ipynb
│   ├── 04_differential_expression.ipynb
│   ├── 05_pathway_enrichment.ipynb
│   ├── 06_gsea_analysis.ipynb
│   ├── 07_machine_learning_survival.ipynb
│   ├── 08_deep_learning_neural_network.ipynb
│   └── 09_unsupervised_learning_clustering.ipynb
│
├── results/
│   ├── figures/            # Publication-quality figures (300 DPI)
│   └── tables/             # Results tables (CSV)
│
├── docs/
│   ├── SUMMARY.md          # Comprehensive findings
│   ├── METHODS.md          # Detailed methodology
│   └── PORTFOLIO_STATEMENT.md  # PhD application materials
│
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Methods Summary

- **Differential Expression:** Negative binomial regression, FDR correction
- **Pathway Enrichment:** Hypergeometric test (GO, KEGG, Reactome)
- **GSEA:** Pre-ranked analysis, MSigDB Hallmarks, 1000 permutations
- **Machine Learning:** Random Forest, XGBoost, Logistic Regression, SHAP
- **Deep Learning:** PyTorch, 256→128→64 architecture, Adam optimizer
- **Clustering:** K-means, UMAP/t-SNE, silhouette analysis

## Technologies

- **Bioinformatics:** Python, Pandas, NumPy, SciPy, gseapy, lifelines
- **Machine Learning:** Scikit-learn, XGBoost, SHAP
- **Deep Learning:** PyTorch
- **Visualization:** Matplotlib, Seaborn, UMAP

## Clinical Implications

- 100-gene prognostic signature for risk stratification
- Stage II molecular subtypes identify high-risk patients needing aggressive treatment
- Therapeutic targets: MYC inhibitors (BET), MTHFD2 (metabolic), CDK inhibitors
- Perfect Stage III detection (100% sensitivity) enables early intervention

## Installation

```bash
git clone https://github.com/[username]/myeloma-biomarker-project.git
cd myeloma-biomarker-project
pip install -r requirements.txt
```

## Usage

Analysis notebooks are numbered sequentially (01-09). Start with:

```bash
jupyter notebook notebooks/01_clinical_analysis.ipynb
```

## Key Files

- `docs/SUMMARY.md` - Comprehensive analysis summary
- `docs/METHODS.md` - Detailed methodology
- `docs/PORTFOLIO_STATEMENT.md` - Research statement for PhD applications
- `results/figures/` - All publication figures
- `results/tables/` - Results data tables

## Citation

If you use this analysis or methodology:

```
[Your Name] (2025). Multiple Myeloma Biomarker Discovery: Integrative 
Computational Analysis. GitHub repository.
```

## Contact

**[Your Name]**  
[University/Institution]  
Email: [your.email@domain.com]  
GitHub: [@your-username](https://github.com/your-username)  
LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

## License

MIT License - See LICENSE file for details

---

**Analysis Completed:** January 2025  
**Purpose:** PhD Application Portfolio - Computational Biology/Bioinformatics
