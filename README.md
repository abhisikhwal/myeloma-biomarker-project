# 🔬 Biomarker Discovery in Multiple Myeloma Progression
## Clinical Analysis of MMRF CoMMpass Study (N=995 patients)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **PhD Application Portfolio Project**  
> Comprehensive survival analysis demonstrating clinical bioinformatics expertise

---

## 🎯 Project Overview

This project performs comprehensive survival analysis on 995 newly diagnosed multiple myeloma (MM) patients from the MMRF CoMMpass study, demonstrating:

- ✅ Advanced statistical analysis (Kaplan-Meier, Cox regression)
- ✅ Publication-quality data visualization
- ✅ Clinical interpretation of genomic data
- ✅ Reproducible bioinformatics workflow
- ✅ Professional documentation standards

**Author:** [Your Name] | MSc in Data Science, AI & Digital Business  
**Date:** January 2026

---

## 🔑 Key Findings

### 1️⃣ ISS Staging is the Dominant Prognostic Factor

**Multivariate Cox Regression Results:**
- **Stage II vs I:** HR = 1.74 (95% CI: 1.10-2.76), **p = 0.018** ✅
- **Stage III vs I:** HR = 1.75 (95% CI: 1.13-2.72), **p = 0.013** ✅

→ *Stage II/III patients have ~75% increased mortality risk*

### 2️⃣ Median Survival by ISS Stage

| ISS Stage | Patients (Deaths) | Median Survival | Prognosis |
|-----------|-------------------|-----------------|-----------|
| **Stage I** | 348 (28) | 22.3 months | Best |
| **Stage II** | 353 (64) | 15.4 months | Intermediate |
| **Stage III** | 266 (92) | 14.9 months | Worst |

**Statistical validation:** Log-rank test p = 0.023 (Stage I vs III)

### 3️⃣ Age and Gender Are Not Independent Predictors

When adjusted for ISS stage in multivariate analysis:
- **Age:** HR = 0.998, p = 0.772 ❌
- **Gender:** HR = 1.08, p = 0.621 ❌

→ *ISS staging alone provides sufficient prognostic information*

---

## 📊 Visualizations

### Publication-Quality Figures Generated:

1. **Kaplan-Meier Survival Curves by ISS Stage**
   - Clear separation between stages
   - 95% confidence intervals
   - Statistical significance (p=0.023)

2. **Patient Characteristics Panel (4 subplots)**
   - Age distribution (median: 63.4 years)
   - ISS stage breakdown (35% / 36% / 27%)
   - Gender and vital status
   - Survival box plots

3. **Age-Stratified Survival Analysis**
   - Survival curves by age group
   - ISS × Age interaction heatmap

4. **Cox Regression Hazard Ratios**
   - Forest plot with confidence intervals
   - Independent risk factors

5. **Gender-Specific Survival**
   - Male vs Female comparison
   - Gender × ISS interaction

6. **Summary Statistics Table**
   - Complete cohort characterization

---

## 📁 Repository Structure

```
myeloma-biomarker-project/
├── README.md                          # This file
├── METHODS_AND_RESULTS.md             # Detailed documentation
├── requirements.txt                   # Python dependencies
├── notebooks/
│   ├── 01_explore_clinical_data.ipynb # Main analysis notebook
│   └── [Future: RNA-seq analysis]
├── data/
│   ├── raw/                           # Original TSV files (gitignored)
│   └── processed/
│       └── patient_level_clean.csv    # Clean dataset (995 rows)
├── results/
│   ├── figures/                       # All 6 publication figures
│   └── tables/
│       └── patient_characteristics.csv
└── src/
    └── data_loader.py                 # Reusable functions
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/myeloma-biomarker-project.git
cd myeloma-biomarker-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Analysis

```bash
# Launch Jupyter
jupyter lab

# Open and run: notebooks/01_explore_clinical_data.ipynb
```

---

## 📚 Methodology

### Data Source
- **Study:** MMRF CoMMpass (NCT01454297)
- **Patients:** 995 newly diagnosed MM
- **Access:** NCI GDC Data Portal (public)
- **Follow-up:** Longitudinal (8 years)

### Statistical Methods
- **Survival Analysis:** Kaplan-Meier estimator
- **Hypothesis Testing:** Log-rank test
- **Multivariate Analysis:** Cox proportional hazards regression
- **Software:** Python (pandas, lifelines, matplotlib, seaborn)

### Quality Control
- ✅ Data cleaning (7,185 → 995 rows)
- ✅ Missing data handling
- ✅ Statistical assumptions verified
- ✅ Multiple testing correction
- ✅ Reproducible workflow

---

## 🎓 Skills Demonstrated

### Bioinformatics
- [x] Public database queries (GDC API)
- [x] Clinical data processing
- [x] Survival analysis
- [x] Statistical testing

### Data Science
- [x] Python programming
- [x] Pandas data manipulation
- [x] Statistical modeling
- [x] Data visualization

### Research
- [x] Study design understanding
- [x] Clinical interpretation
- [x] Scientific writing
- [x] Reproducible research

---

## 📈 Results Summary

> **Bottom Line:** This analysis validates ISS staging as the gold standard prognostic tool for multiple myeloma. Stage II/III patients show 74-75% increased mortality risk independent of age and gender. These findings support ISS-based risk stratification for treatment planning.

**Clinical Impact:**
- Stage III patients need aggressive early intervention
- Age should not exclude patients from intensive therapy
- Simple staging system provides robust prognostication

---

## 🔮 Future Directions

### Phase 2: Genomic Integration (Next Steps)
- [ ] Download RNA-seq data (787 patients)
- [ ] Differential expression analysis
- [ ] Gene-survival correlations
- [ ] Machine learning biomarker discovery
- [ ] Pathway enrichment analysis

### Phase 3: Advanced Modeling
- [ ] MGUS → MM progression analysis
- [ ] Treatment response prediction
- [ ] Multi-omics integration
- [ ] External validation cohort

---

## 📖 Documentation

**Detailed Methods:** See [METHODS_AND_RESULTS.md](METHODS_AND_RESULTS.md)

**Key Sections:**
- Study population & data collection
- Statistical analysis methodology
- Complete results with interpretation
- Discussion & clinical implications
- Limitations & future directions

---

## 🏆 Why This Project Matters for PhD Applications

### Demonstrates:
1. **Clinical Research Skills** - Real patient data analysis
2. **Statistical Rigor** - Proper methodology, p-values, confidence intervals
3. **Translational Thinking** - Bench to bedside interpretation
4. **Technical Proficiency** - Python, statistical software, visualization
5. **Scientific Communication** - Clear figures, professional documentation
6. **Independent Learning** - Self-directed project from concept to completion

### Portfolio Quality:
- ✅ Publication-ready figures
- ✅ Reproducible analysis
- ✅ Professional documentation
- ✅ GitHub-ready codebase
- ✅ Real-world clinical data

---

## 📧 Contact

**[Your Name]**  
MSc in Data Science, AI & Digital Business  
📧 [your.email@example.com]  
🔗 [LinkedIn Profile URL]  
💻 [GitHub Profile URL]

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Data Source:** Multiple Myeloma Research Foundation (MMRF)
- **Database:** NCI Genomic Data Commons (GDC)
- **Study:** CoMMpass (NCT01454297)

---

## 📚 References

1. Greipp PR, et al. (2005). International staging system for multiple myeloma. *J Clin Oncol* 23(15):3412-20.
2. Kumar SK, et al. (2017). Multiple myeloma. *Nat Rev Dis Primers* 3:17046.
3. Palumbo A, Anderson K. (2011). Multiple myeloma. *N Engl J Med* 364(11):1046-60.

---

*Last Updated: January 30, 2026*  
*Status: Phase 1 Complete (Clinical Analysis) | Phase 2 Pending (RNA-seq Integration)*
