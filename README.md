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

## Results at a Glance

| Analysis Type | Key Metric | Result | Significance |
|--------------|------------|--------|--------------|
| **Differential Expression** | Significant genes (FDR < 0.05) | 6,356 genes | 3,187 up, 3,169 down |
| **Pathway Enrichment** | Top pathway (GO) | Cell cycle | p < 1e-20 |
| **GSEA** | Strongest enrichment | G2-M Checkpoint | NES = 2.897, FDR < 0.001 |
| **Machine Learning** | Best model (AUC) | Logistic Regression | 0.874 |
| **SHAP Interpretation** | Top predictor | MYC | Consistent #1 across models |
| **Deep Learning** | Classification accuracy | 93.8% | 100% Stage III sensitivity |
| **Unsupervised Clustering** | Molecular subtypes | 4 clusters | Stage II heterogeneity |

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

## Data Access

**IMPORTANT:** The MMRF CoMMpass dataset requires controlled access authorization.

- **Raw data cannot be shared publicly** due to data usage agreements
- To reproduce this analysis, you must:
  1. Apply for data access at: https://portal.gdc.cancer.gov/ (dbGaP authentication)
  2. Submit MMRF data use application at: https://research.themmrf.org/
  3. Download clinical and RNA-seq data following approval
  4. Place files in `data/raw/` directory as specified in `data/README.md`

The repository includes:
- ✅ All analysis code (notebooks 01-09)
- ✅ Methodology documentation
- ✅ Small summary statistics
- ❌ No raw patient-level data (excluded per data usage agreement)

## Installation

```bash
git clone https://github.com/abhisikhwal/myeloma-biomarker-project.git
cd myeloma-biomarker-project
pip install -r requirements.txt
```

## Usage

### Notebook Execution Order

Execute notebooks sequentially for full reproducibility:

1. **01_explore_clinical_data.ipynb** - Clinical survival analysis, Kaplan-Meier curves
2. **02_download_rnaseq_data.ipynb** - GDC data download (requires MMRF authorization)
3. **03_process_rnaseq_counts.ipynb** - Normalization, QC, gene filtering
4. **04_differential_expression_analysis.ipynb** - 6,356 significant genes (FDR < 0.05)
5. **05_pathway_enrichment_analysis.ipynb** - GO, KEGG, Reactome enrichment
6. **06_gsea_analysis.ipynb** - MSigDB Hallmarks (G2-M checkpoint NES = 2.897)
7. **07_machine_learning_survival.ipynb** - ML models, SHAP interpretability
8. **08_deep_learning_neural_network.ipynb** - PyTorch classifier (93.8% accuracy)
9. **09_unsupervised_learning_clustering.ipynb** - UMAP, K-means, molecular subtypes

**Note:** Notebooks 02-09 require MMRF data access (see Data Access section above)

```bash
cd notebooks
jupyter lab
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
Abhinav Sikhwal (2026). Multiple Myeloma Biomarker Discovery: Integrative 
Computational Analysis. GitHub: https://github.com/abhisikhwal/myeloma-biomarker-project
```

## Contact

**Abhinav Sikhwal**  
Computational Biology Researcher  
GitHub: [@abhisikhwal](https://github.com/abhisikhwal)  
LinkedIn: [linkedin.com/in/abhinav-sikhwal](https://www.linkedin.com/in/abhinav-sikhwal/)

## License

MIT License - See LICENSE file for details

---

**Analysis Completed:** January 2026  
**Purpose:** PhD Application Portfolio (Leibniz-LSB at TUM) - Computational Biology/Bioinformatics
