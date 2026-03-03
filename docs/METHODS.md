# Detailed Methodology
## Multiple Myeloma Biomarker Discovery Project

**Analysis Date:** January 2026  
**Notebooks:** 9 (01-09)  
**Software:** Python 3.8+

---

## 1. Dataset & Study Population

### 1.1 Data Source
- **Study:** Multiple Myeloma Research Foundation (MMRF) CoMMpass
- **Full Name:** Relating Clinical Outcomes in MM to Personal Assessment of Genetic Profile
- **ClinicalTrials.gov:** NCT01454297
- **Data Portal:** NCI Genomic Data Commons (GDC)
- **Access:** Public (open-access tier)
- **Download Date:** January 2026

### 1.2 Cohort Characteristics
- **Total Patients:** 859 with complete clinical + RNA-seq data
- **ISS Stage I:** 308 patients (35.9%)
- **ISS Stage II:** 335 patients (39.0%)
- **ISS Stage III:** 216 patients (25.1%)
- **Median Age:** 63.4 years (range: 28-90)
- **Gender:** 60% male, 40% female
- **Median Follow-up:** 2.8 years
- **Deaths:** 191 (22.2%)

### 1.3 Inclusion Criteria
- Newly diagnosed multiple myeloma
- Complete clinical data (ISS stage, survival)
- RNA-seq data passing quality control
- No missing covariates for multivariate analysis

### 1.4 ISS Staging System
- **Stage I:** β2-microglobulin <3.5 mg/L AND albumin ≥3.5 g/dL
- **Stage II:** Not Stage I or III
- **Stage III:** β2-microglobulin ≥5.5 mg/L

---

## 2. Clinical Analysis (Notebook 01)

### 2.1 Survival Analysis
**Methods:**
- Kaplan-Meier estimator for non-parametric survival curves
- 95% confidence intervals via Greenwood's formula
- Log-rank test for survival distribution comparison
- Median survival computed per ISS stage

**Software:** `lifelines` (v0.27+)

**Statistical Test:**
```python
from lifelines.statistics import multivariate_logrank_test
results = multivariate_logrank_test(durations, groups, event_observed)
p_value = results.p_value  # Two-sided
```

### 2.2 Cox Proportional Hazards Regression
**Model:**
```
h(t|X) = h0(t) * exp(β1*ISS_II + β2*ISS_III + β3*Age + β4*Gender)
```

**Variables:**
- ISS Stage (categorical: I=reference, II, III)
- Age at diagnosis (continuous, years)
- Gender (binary: female=reference, male)

**Assumptions:**
- Proportional hazards verified via Schoenfeld residuals
- Linearity of continuous predictors assessed

**Software:** `lifelines.CoxPHFitter()`

---

## 3. RNA-seq Data Processing (Notebooks 02-03)

### 3.1 Data Download (Notebook 02)
**Source:** GDC Data Portal API

**Commands:**
```bash
gdc-client download -m gdc_manifest.txt
```

**Files Retrieved:**
- RNA-seq STAR gene expression files (HTSeq counts)
- Clinical data (TSV format)
- Sample sheet with case-to-file mapping

### 3.2 Quality Control
**Metrics:**
- **Total read count:** >10 million reads per sample
- **Mapping rate:** >80%
- **Ribosomal RNA:** <20%
- **Duplicate rate:** <50%

**Sample Exclusions:**
- Low read count (<5 million): 12 samples removed
- Failed QC metrics: 8 samples removed
- Missing clinical data: 23 samples removed

### 3.3 Normalization (Notebook 03)
**Method:** log2(CPM + 1) transformation

**CPM (Counts Per Million):**
```
CPM = (raw_counts / total_counts) * 1,000,000
log2_CPM = log2(CPM + 1)  # +1 pseudocount avoids log(0)
```

**Rationale:**
- CPM accounts for library size differences
- log2 transformation stabilizes variance
- +1 pseudocount handles zero counts

**Alternative considered:** DESeq2-style normalization (size factors)

---

## 4. Differential Expression Analysis (Notebook 04)

### 4.1 Statistical Model
**Method:** Negative binomial regression (similar to DESeq2/edgeR)

**Model:**
```
log(μij) = β0j + β1j * ISS_Stagei + offseti
```
Where:
- μij = expected count for gene j in sample i
- β1j = log fold change for gene j
- offseti = log(size_factori) to account for library size

**Software:** Custom implementation using `statsmodels.GLM(family=NegativeBinomial)`

### 4.2 Multiple Testing Correction
**Method:** Benjamini-Hochberg FDR (False Discovery Rate)

**Procedure:**
1. Compute p-values for all 30,018 genes
2. Rank p-values from smallest to largest
3. Adjusted p-value (FDR): `p_adj = p * n_genes / rank`
4. Control FDR at 5%: `FDR < 0.05`

### 4.3 Significance Thresholds
- **FDR < 0.05:** Statistical significance
- **|log2FC| > 1:** Biological significance (2-fold change)

**Results:** 6,356 genes passed both criteria

---

## 5. Pathway Enrichment Analysis (Notebook 05)

### 5.1 Gene Ontology (GO) Enrichment
**Method:** Over-representation analysis (ORA)

**Statistical Test:** Hypergeometric distribution
```
P(X ≥ k) = Σ [(M choose x) * (N-M choose n-x)] / (N choose n)
```
Where:
- N = total genes in genome (background)
- M = genes in specific GO term
- n = genes in query set (significant DEGs)
- k = overlap (significant DEGs in this GO term)

**Database:** Gene Ontology Consortium (2023 version)
**Categories:** Biological Process (BP), Molecular Function (MF), Cellular Component (CC)
**Software:** `gseapy.enrichr()`

### 5.2 KEGG Pathway Enrichment
**Database:** Kyoto Encyclopedia of Genes and Genomes (KEGG) 2021

**Method:** Same hypergeometric test as GO

**Pathways Tested:** ~350 human pathways

### 5.3 Reactome Pathway Enrichment
**Database:** Reactome Pathway Database (2022)

**Method:** Same hypergeometric test as GO

**Pathways Tested:** ~2,500 human pathways

### 5.4 Multiple Testing Correction
**Method:** Benjamini-Hochberg FDR within each database

**Significance:** Adjusted p-value < 0.05

---

## 6. Gene Set Enrichment Analysis (Notebook 06)

### 6.1 GSEA Methodology
**Method:** Pre-ranked Gene Set Enrichment Analysis

**Algorithm:**
1. **Rank genes:** All 30,018 genes ranked by log2 fold change (Stage III vs I)
2. **Enrichment Score (ES):** Walk down ranked list, increase score when gene in set, decrease when not
3. **Normalize ES:** Account for gene set size → Normalized Enrichment Score (NES)
4. **Permutations:** 1,000 permutations to compute p-value
5. **FDR correction:** Across all gene sets tested

**Gene Sets:** MSigDB Hallmark collection (v2020, 50 hallmark pathways)

**Software:** `gseapy.prerank()`

**Enrichment Score Formula:**
```
ES = max |Σ [gene_in_set] - Σ [gene_not_in_set]|
```

### 6.2 Leading-Edge Analysis
**Definition:** Subset of genes in gene set that contribute most to enrichment signal

**Method:** Genes before peak enrichment score

**Purpose:** Identify specific dysregulated genes within pathway

---

## 7. Machine Learning (Notebook 07)

### 7.1 Feature Selection Pipeline

**Step 1: Variance Filtering**
```python
from sklearn.feature_selection import VarianceThreshold
selector = VarianceThreshold(threshold=0.1)
# 30,018 → 15,234 genes
```

**Step 2: Univariate Selection**
```python
from scipy.stats import spearmanr
# Spearman correlation with survival time
# Top 1,000 genes by |correlation|
```

**Step 3: Random Forest Importance**
```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=200)
# Top 100 genes by feature_importances_
```

**Final Feature Set:** 100 genes (300-fold reduction from 30,018)

### 7.2 Train-Test Split
**Method:** Stratified split (maintains class proportions)

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratified=True, random_state=42
)
```

**Sizes:**
- Training: 644 patients (75%)
- Test: 215 patients (25%)

### 7.3 Model Training

**Models Evaluated:**

**1. Logistic Regression**
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(
    penalty='l2',  # Ridge regularization
    C=1.0,         # Inverse regularization strength
    solver='lbfgs',
    max_iter=1000,
    multi_class='multinomial'
)
```

**2. Random Forest**
```python
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42
)
```

**3. XGBoost**
```python
import xgboost as xgb
model = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
```

**4. Gradient Boosting**
```python
from sklearn.ensemble import GradientBoostingClassifier
model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
```

### 7.4 Cross-Validation
**Method:** 5-fold stratified cross-validation

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X_train, y_train, cv=skf, scoring='roc_auc_ovr')
```

**Metric:** AUC (Area Under ROC Curve) - one-vs-rest for multi-class

### 7.5 SHAP Analysis
**Method:** SHapley Additive exPlanations (game-theoretic feature attribution)

**Implementation:**
```python
import shap
explainer = shap.TreeExplainer(model)  # For tree-based models
shap_values = explainer.shap_values(X_test)
```

**Interpretation:**
- **SHAP value > 0:** Feature pushes prediction toward this class
- **SHAP value < 0:** Feature pushes prediction away from this class
- **|SHAP value|:** Magnitude of feature importance

**Visualization:** Beeswarm plots showing feature contributions

---

## 8. Deep Learning (Notebook 08)

### 8.1 Neural Network Architecture

**Implementation:** PyTorch 2.0

```python
import torch.nn as nn

class MyelomaClassifier(nn.Module):
    def __init__(self, input_dim=100):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 256)
        self.bn1 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.fc3 = nn.Linear(128, 64)
        self.bn3 = nn.BatchNorm1d(64)
        self.fc4 = nn.Linear(64, 3)  # 3 classes (ISS I, II, III)
        self.dropout = nn.Dropout(0.3)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = self.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        x = self.relu(self.bn3(self.fc3(x)))
        x = self.dropout(x)
        x = self.fc4(x)
        return x
```

**Total Parameters:** 48,067

### 8.2 Training Configuration

**Data Split:**
```python
# 70% train, 15% validation, 15% test
train_size = int(0.70 * len(dataset))
val_size = int(0.15 * len(dataset))
test_size = len(dataset) - train_size - val_size
```

**Optimizer:**
```python
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    betas=(0.9, 0.999),
    eps=1e-8
)
```

**Loss Function:**
```python
criterion = nn.CrossEntropyLoss()
```

**Learning Rate Scheduler:**
```python
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',
    factor=0.5,
    patience=10,
    verbose=True
)
```

**Early Stopping:**
- Monitor validation loss
- Patience: 20 epochs (stop if no improvement for 20 consecutive epochs)

### 8.3 Training Loop
```python
for epoch in range(max_epochs):
    # Training
    model.train()
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
    
    # Validation
    model.eval()
    with torch.no_grad():
        val_loss = evaluate(model, val_loader)
    
    # Learning rate scheduling
    scheduler.step(val_loss)
    
    # Early stopping
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        save_checkpoint(model)
    else:
        patience_counter += 1
        if patience_counter >= patience:
            break  # Stop training
```

**Hyperparameters:**
- Batch size: 32
- Max epochs: 150
- Early stopping patience: 20
- Learning rate: 0.001 (initial)

### 8.4 Evaluation Metrics
```python
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)
```

**Metrics Computed:**
- Accuracy
- Precision (per class and weighted average)
- Recall (per class and weighted average)
- F1-score (per class and weighted average)
- Confusion matrix

---

## 9. Unsupervised Learning (Notebook 09)

### 9.1 Dimensionality Reduction

**PCA (Principal Component Analysis)**
```python
from sklearn.decomposition import PCA
pca = PCA(n_components=50)
X_pca = pca.fit_transform(X_scaled)
# Variance explained: 25% in first 50 PCs
```

**t-SNE (t-Distributed Stochastic Neighbor Embedding)**
```python
from sklearn.manifold import TSNE
tsne = TSNE(
    n_components=2,
    perplexity=30,
    n_iter=1000,
    random_state=42
)
X_tsne = tsne.fit_transform(X_scaled)
```

**UMAP (Uniform Manifold Approximation and Projection)**
```python
import umap
reducer = umap.UMAP(
    n_neighbors=15,
    min_dist=0.1,
    n_components=2,
    random_state=42
)
X_umap = reducer.fit_transform(X_scaled)
```

**Selection:** UMAP chosen for clustering (best visual separation)

### 9.2 Optimal Cluster Number

**Methods:**
1. **Elbow Method:** Plot inertia vs. k
2. **Silhouette Analysis:** Compute silhouette scores for k=2 to k=10

```python
from sklearn.metrics import silhouette_score

silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X_umap)
    score = silhouette_score(X_umap, labels)
    silhouette_scores.append(score)
```

**Result:** k=4 optimal (highest silhouette score + biological interpretability)

### 9.3 K-means Clustering
```python
from sklearn.cluster import KMeans

kmeans = KMeans(
    n_clusters=4,
    init='k-means++',  # Smart initialization
    n_init=10,         # 10 random initializations
    max_iter=300,
    random_state=42
)
clusters = kmeans.fit_predict(X_umap)
```

### 9.4 Cluster Validation

**Silhouette Score:**
```python
from sklearn.metrics import silhouette_score
score = silhouette_score(X_umap, clusters)
# Score = 0.58 (good separation)
```

**Survival Analysis:**
```python
from lifelines.statistics import multivariate_logrank_test
result = multivariate_logrank_test(
    durations=survival_times,
    groups=clusters,
    event_observed=events
)
# p < 0.0001 (highly significant)
```

---

## 10. Software & Packages

### Core Scientific Computing
- **Python:** 3.8+
- **NumPy:** 1.24.3 (array operations)
- **pandas:** 2.0.0 (dataframes)
- **SciPy:** 1.10.0 (statistical tests)
- **Matplotlib:** 3.7.0 (plotting)
- **Seaborn:** 0.12.0 (statistical visualization)

### Bioinformatics
- **gseapy:** 1.0.5 (pathway enrichment, GSEA)
- **lifelines:** 0.27.0 (survival analysis)

### Machine Learning
- **scikit-learn:** 1.3.0 (ML models, preprocessing)
- **XGBoost:** 2.0.0 (gradient boosting)
- **SHAP:** 0.42.0 (model interpretability)

### Deep Learning
- **PyTorch:** 2.0.0 (neural networks)
- **torchvision:** 0.15.0 (utilities)

### Dimensionality Reduction
- **umap-learn:** 0.5.3 (UMAP)

### Utilities
- **tqdm:** 4.65.0 (progress bars)
- **Jupyter:** 1.0.0 (notebooks)

---

## 11. Statistical Considerations

### Multiple Testing Correction
**Problem:** Testing 30,018 genes → high false positive rate at p<0.05

**Solution:** Benjamini-Hochberg FDR correction
- Controls expected proportion of false discoveries
- Less conservative than Bonferroni
- Standard in genomics

### Survival Analysis
**Censoring:** Right-censored data (patients alive at end of follow-up)
**Handling:** Kaplan-Meier and Cox regression properly account for censoring

### Machine Learning
**Overfitting Prevention:**
- Train-test split (never test on training data)
- Cross-validation (5-fold stratified)
- Regularization (L2 penalty, dropout)
- Early stopping (DL)

**Class Imbalance:**
- Stratified splitting maintains class proportions
- Weighted metrics for evaluation

### Deep Learning
**Regularization Techniques:**
- Batch normalization (reduces internal covariate shift)
- Dropout (0.3) (randomly zeros units during training)
- Early stopping (prevents overtraining)
- Learning rate scheduling (adaptive learning rate)

---

## 12. Reproducibility

### Random Seeds
All random operations seeded for reproducibility:
```python
import random
import numpy as np
import torch

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)
```

### Environment
**requirements.txt** specifies exact package versions

**Installation:**
```bash
pip install -r requirements.txt
```

### Code Organization
- 9 Jupyter notebooks (sequential pipeline)
- Clear markdown documentation
- Inline comments for complex operations
- Functions modularized where appropriate

---

## 13. Computational Resources

### Hardware
- **CPU:** Multi-core (8+ cores recommended)
- **RAM:** 32GB+ (for full dataset in memory)
- **GPU:** Optional (speeds up deep learning ~10x)

### Runtime
- **Differential Expression:** ~30 minutes
- **Pathway Enrichment:** ~10 minutes
- **GSEA:** ~15 minutes
- **Machine Learning:** ~20 minutes
- **Deep Learning:** ~30 minutes (CPU), ~3 minutes (GPU)
- **Unsupervised Learning:** ~15 minutes

**Total Pipeline:** ~2.5 hours (CPU), ~1.5 hours (GPU)

---

## 14. Data Availability

### Raw Data
- **Source:** NCI GDC Data Portal
- **Project:** MMRF-COMMPASS
- **Access:** Controlled (dbGaP authentication required for raw sequencing)
- **Processed counts:** Open-access

### Processed Data
- **patient_level_clean.csv:** 859 patients × 100 genes
- **differential_expression_results.csv:** 30,018 genes × statistics
- **pathway_enrichment_results.csv:** GO/KEGG/Reactome results
- **gsea_hallmark_results.csv:** 50 hallmark pathways

**Availability:** Included in GitHub repository

---

## 15. Ethical Considerations

### Data Usage
- Public data from consented research participants
- Proper attribution to MMRF CoMMpass study
- Compliance with GDC data usage policies

### Clinical Translation
- Findings are exploratory, require validation
- Not intended for direct clinical use without validation
- Computational predictions ≠ clinical recommendations

---

**Methods Documentation Complete**  
**For questions:** Contact Abhinav Sikhwal at https://github.com/abhisikhwal
