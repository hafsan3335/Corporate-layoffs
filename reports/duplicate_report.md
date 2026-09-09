# Duplicate Analysis & Disambiguation Report

## 1. Overview
Public layoff event tracking often records multiple media dispatches for a single corporate announcement or records simultaneous downsizing actions across disparate operating facilities.

## 2. Duplicate Audit Findings
- **Raw Input Rows:** 4,594
- **Identical Event Duplicates Removed:** 5
- **Cleaned Event Rows Retained:** 4,589

## 3. Disambiguation Taxonomy
1. **True Redundant Scrapes:** Identical company, announcement date, city, headcounts, and percentage, differing only in news wire URL or scrape timestamp (e.g., Beyond Meat on 2022-10-14 recorded via CNBC and FoodDive). These were deduplicated to prevent double-counting.
2. **Multi-Site Corporate Actions:** Identical announcement date and company, but different operating locations or distinct business divisions (e.g., Amazon on 2026-07-22 announcing Florida warehouse reallocations alongside Seattle AGI corporate restructuring). These reflect distinct operational restructuring decisions and were preserved.
