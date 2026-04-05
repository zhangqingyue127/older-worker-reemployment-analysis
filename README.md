# Analysis of Factors Affecting Re-employment of Elderly Workers Based on Text Mining

## Abstract
This repository presents a course-based research project in labor economics that examines the key factors affecting the re-employment of elderly workers in the context of delayed retirement reform in China. The study combines Chinese policy texts and social media discourse with a hybrid **LDA–DEMATEL–ISM** framework to identify latent themes, quantify inter-factor relationships, and reveal the hierarchical structure of the re-employment mechanism. Based on the empirical analysis, the study identifies **10 influencing factors** across four dimensions: **individual**, **technological**, **social**, and **institutional/policy**. The findings suggest that **skill adaptability** functions as the most direct surface-level determinant, while **age discrimination in the workplace** and **group norm effects** act as deeper structural constraints.

**Keywords:** elderly workers; re-employment; text mining; LDA; DEMATEL; ISM; delayed retirement

---

## Research Background
Population aging has become an increasingly prominent structural issue in China. Against this backdrop, delayed retirement reform has gradually moved from policy discussion to institutional implementation. While extending working life may help alleviate labor supply pressure and pension burdens, it also raises a set of labor-market questions concerning re-employment opportunities, intergenerational competition, skill mismatch, health constraints, and social prejudice.

This project focuses on the following research question:

> **What are the key factors affecting the re-employment of elderly workers, and how are these factors structurally related to one another?**

Rather than relying solely on expert scoring, this study uses text mining to extract factor signals from a large corpus of public discussion and policy documents, and then models the interaction and hierarchy among those factors.

---

## Data Sources
The corpus was constructed from both **policy-oriented texts** and **public opinion texts**, in order to capture institutional discourse as well as social responses.

### Policy texts
- Government policy documents
- Official explanatory articles related to delayed retirement and elderly employment

### Social media texts
- Weibo comments
- Bilibili danmu/comments

### Collection window
- **2024-09-10 to 2025-06-01**

### Corpus size
- **155,865 Chinese characters** after collection and integration

The use of multi-source textual data allows the project to capture both macro-level policy framing and micro-level public attitudes toward elderly labor-force re-entry.

---

## Methodological Framework
This project adopts an integrated **LDA–DEMATEL–ISM** framework.

### 1. Text preprocessing
The raw corpus was cleaned through a standard Chinese text processing pipeline, including:
- text aggregation
- deduplication
- stopword removal
- punctuation filtering
- Chinese word segmentation using `jieba`

### 2. LDA topic modeling
Latent Dirichlet Allocation (LDA) was used to identify latent themes in the corpus. Perplexity was used to determine the optimal number of topics, and the final model retained **10 topics**.

These topics were then interpreted and consolidated into **10 influencing factors** under four dimensions:

#### Individual dimension
- Health and physical condition
- Re-employment willingness
- Skill adaptability

#### Technological dimension
- Digital access capability
- Technology substitution risk

#### Social dimension
- Workplace age discrimination
- Family responsibility conflict
- Group norm effect

#### Institutional and policy dimension
- Policy support intensity
- Institutional support completeness

### 3. DEMATEL based on text-derived semantic similarity
To reduce the subjectivity of expert scoring, this project uses a data-driven strategy to construct the influence matrix. Specifically:
- TF-IDF was used to extract representative keywords
- Word2Vec was used to learn semantic representations
- cosine similarity was used to estimate inter-factor relatedness
- a non-linear transformation and Top-3 averaging strategy were applied to improve discrimination and robustness

This process produced a comprehensive influence matrix for subsequent structural analysis.

### 4. ISM hierarchical modeling
Interpretive Structural Modeling (ISM) was employed to transform the influence matrix into a hierarchical structure. After threshold testing, the final threshold was set at:

- **λ = 0.72**

The resulting reachability matrix was then used to divide the 10 factors into multiple structural layers.

---

## Main Findings
The study finds that the re-employment of elderly workers is a **multi-dimensional and hierarchical system** rather than a single-factor issue.

### Surface layer
- **Skill adaptability** is the most direct determining factor.
- It acts as the final manifestation of interactions among deeper factors and directly affects job matching quality.

### Shallow layer
- **Health and physical condition**
- **Re-employment willingness**
- **Digital access capability**

These factors function as the immediate prerequisites for labor-force re-entry.

### Middle layer
- **Technology substitution risk**
- **Family responsibility conflict**
- **Policy support intensity**
- **Institutional support completeness**

These factors connect individual decision-making with the broader labor-market and policy environment.

### Deep layer
- **Workplace age discrimination**
- **Group norm effect**

These are the most fundamental constraint factors. They do not always act directly on job-seeking behavior, but they shape the social environment, perceived legitimacy, and psychological expectations surrounding elderly re-employment.

---

## Key Analytical Figure
The README uses the **original project figure** rather than a redrawn version.

![Centrality-Causality Scatter Plot Analysis](figures/优化版_因素分析结果_图例左下.png)

*Figure. Centrality–causality scatter plot used in the DEMATEL analysis.*

---

## Academic Contribution
This project contributes in three ways at the course-research level:

1. **Interdisciplinary integration**  
   It combines labor economics with natural language processing and structural modeling.

2. **Data-driven factor identification**  
   It replaces conventional expert-scoring dependence with semantic information extracted from large-scale text data.

3. **Hierarchical mechanism interpretation**  
   It goes beyond listing factors and instead explains how factors operate at different structural levels.

---

## Repository Structure
```text
.
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── crawlers/
├── preprocessing/
├── models/
├── analysis/
├── visualization/
├── figures/
└── docs/
```

---

## Reproducibility
This repository is organized as a cleaned and portfolio-oriented academic project version. The workflow follows the sequence below:

1. collect policy and social-media texts  
2. clean and preprocess the corpus  
3. run LDA topic modeling and interpret topics  
4. compute the semantic similarity-based influence matrix  
5. perform DEMATEL centrality/causality analysis  
6. construct the ISM hierarchy  
7. interpret the results from a labor economics perspective

---

## Academic Context
- **University:** Southwestern University of Finance and Economics  
- **Course:** Labor Economics  
- **Semester:** 2024–2025, Semester 2  
- **Author:** Qingyue Zhang  
- **Major:** Artificial Intelligence

This project was completed as a final course paper and later reorganized into a GitHub-friendly research portfolio repository.

---

## Notes
- This repository is intended for **academic presentation and portfolio use**.
- The project reflects a **course research framework**, not a journal-submission version.
- Some source texts originate from public online platforms and official documents; users should handle redistribution carefully and comply with the relevant platform or copyright policies.

---

## Citation
If you would like to reference this repository, please cite it as a course project or GitHub research portfolio entry rather than as a published article.

```bibtex
@misc{zhang2025elderlyreemployment,
  author       = {Qingyue Zhang},
  title        = {Analysis of Factors Affecting Re-employment of Elderly Workers Based on Text Mining},
  year         = {2025},
  note         = {Course project repository, Labor Economics, Southwestern University of Finance and Economics}
}
```
