# Methodology Notes

This repository is a portfolio-style refactor of a labor economics course project on older-worker reemployment.

## Research pipeline

1. **Data collection**
   - Policy documents related to delayed retirement and labor protection
   - Weibo comments discussing retirement reform
   - Bilibili danmaku discussing older-worker reemployment and delayed retirement

2. **Text preprocessing**
   - Merge multi-source text
   - Remove duplicates
   - Normalize punctuation and whitespace
   - Segment Chinese text with `jieba`
   - Remove stopwords and filler expressions

3. **Topic discovery**
   - Train LDA models on the cleaned corpus
   - Compare multiple topic counts
   - Select the best topic number based on perplexity and interpretability

4. **Factor construction**
   - Map topic words into ten analytical factors
   - Build a factor-keyword dictionary

5. **Structural analysis**
   - Use a Word2Vec-based asymmetric similarity matrix
   - Compute DEMATEL prominence and relation scores
   - Generate an ISM reachability matrix
   - Recover multi-level factor structure

## Factor list

- S1: Health and physical capacity
- S2: Reemployment intention
- S3: Skill adaptability
- S4: Digital access capability
- S5: Technology substitution risk
- S6: Age discrimination
- S7: Family responsibility conflict
- S8: Group norm effect
- S9: Policy support strength
- S10: Institutional completeness

## Refactor principles

This GitHub version does **not** directly expose the original classroom scripts.
Instead, it rewrites the workflow into cleaner modules with:
- English comments
- clearer file naming
- reusable functions
- output folders for artifacts
- better separation between raw data, modeling, analysis, and visualization