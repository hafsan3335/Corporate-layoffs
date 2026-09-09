# Data Dictionary: Corporate Layoffs Research Dataset

**Source:** Layoffs.fyi / Kaggle (`swaptr/layoffs-2022`, Version 478)  
**Date Range:** 2020-03-11 to 2026-09-03  
**Total Cleaned Events:** 4,589  
**Unique Companies:** 2,975  
**Unique Countries:** 67  

| Column Name | Type | Null Count (%) | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `company` | String | 0 (0.0%) | Legal or operational name of the company | *Amazon, Meta, Stripe* |
| `location` | String | 0 (0.0%) | Headquarters city or metro area | *SF Bay Area, New York City* |
| `total_laid_off` | Float | 1,593 (34.7%) | Count of employees terminated (**Layoff Magnitude**) | *500, 11000* |
| `percentage_laid_off` | Float | 1,712 (37.3%) | Fraction of workforce terminated (**Layoff Intensity**) | *0.10 (10%), 0.25 (25%)* |
| `date` | Date | 0 (0.0%) | Public announcement date (ISO `YYYY-MM-DD`) | *2023-01-18* |
| `industry` | String | 0 (0.0%) | Granular sector classification | *Finance, Retail, Healthcare* |
| `industry_group` | String | 0 (0.0%) | Consolidated macro industry cohort | *Fintech & Financial Services* |
| `stage` | String | 0 (0.0%) | Financing maturity stage at announcement | *Series B, Post-IPO, Seed* |
| `stage_group` | String | 0 (0.0%) | Consolidated maturity cohort | *Late Stage (Series C-D)* |
| `funds_raised` | Float | 544 (11.9%) | Total historical funding raised (USD Millions) | *257.0 ($257M)* |
| `country` | String | 0 (0.0%) | Country of corporate headquarters | *United States, India, Germany* |
| `source` | String | 3 (0.1%) | Primary verification URL / press release | *https://techcrunch.com/...* |
| `date_added` | Date | 0 (0.0%) | Date the event was logged into Layoffs.fyi | *2023-01-19* |
