# Genomics Portfolio
**Milena Campos** | Computational Quantitative Geneticist

Researcher specializing in quantitative genetics, genomic prediction, and 
GWAS in Nellore beef cattle. Building reproducible computational pipelines 
for large-scale phenotypic and genomic data.

---

## Project P1 — Phenotype Preprocessing Pipeline

**What it does:** Loads, validates, and cleans a large Nellore cattle
phenotype dataset (1.19M records, 44 traits) for downstream genetic analysis.
Includes morphological defect frequency analysis across evaluation stages
(weaning, yearling, revision).

**Dataset:** Nellore beef cattle · Brazil · birth, weaning and yearling weights
+ conformation scores + morphological defects + pedigree

**Scripts:**
- `clean_phenotypes.py` — data loading, biological outlier removal, logging
- `defect_frequency.py` — defect frequency analysis (translated from R)

**Results:**
- 385,978 animals retained after pedigree filtering
- 210 biological outliers removed across 3 weight traits
- ODE (despigmentation) most frequent defect at weaning and yearling stages
- Clean dataset ready for GWAS and genomic prediction

**Skills demonstrated:** Python · pandas · data cleaning · 
reproducible pipelines · R→Python translation · logging

---

## Skills
**Expert:** Quantitative genetics · GWAS · genomic prediction · 
statistical modeling · R · HPC · scientific writing

**Proficient:** Python · pandas · matplotlib · Git · SQL