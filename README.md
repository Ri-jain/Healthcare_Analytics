# Healthcare_Analytics


#  Hospital Inpatient Discharges: Total Hip Replacement

---

##  Overview

This project analyzes **26,594 inpatient discharge records** for Total Hip Replacement surgeries across New York State hospitals. It identifies financial, demographic, and geographic patterns in **cost**, **length of stay**, and **profitability**, supporting smarter decision-making for hospital administrators and public health stakeholders.

---

##  Key Highlights

-  **Top 10 hospitals** generated **over 50% of total charges**, indicating revenue concentration.
-  Identified **5 hospitals** with **negative profit per patient**, exposing inefficiencies.
-  **Women** had **shorter hospital stays** and **higher profitability** per case.
-  **Older age groups (70–89)** saw the **highest length of stay and costs**, straining system resources.
-  **Revenue per day** and **cost per day** were tightly linked (corr = **0.88**).
-  Disparities across **counties** and **health service areas** revealed gaps in service access.

---

## Objectives

- Measure hospital efficiency using cost, revenue, and profit metrics  
- Identify top and underperforming hospitals by financial outcomes  
- Examine demographic impacts (race, gender, age) on patient outcomes  
- Detect regional disparities in healthcare access and economics  
- Visualize insights to support public health policy and operations  

---

##  Project Tasks

| Category             | Description |
|----------------------|-------------|
|  **Data Cleaning**   | Standardized datatypes, handled null ZIPs, removed redundant fields |
|  **Feature Engineering** | Added `cost_per_day`, `profit`, `revenue_per_day`, and `LOS category` |
|  **Demographic Analysis** | Aggregated LOS, cost, and profit by **race**, **gender**, and **age group** |
|  **Financial Benchmarking** | Identified **top 10** hospitals by charges, costs, and profit |
|  **Outlier Detection** | Highlighted underperforming hospitals with high costs and low returns |
|  **Geographic Profiling** | Mapped results by **county** and **health service area** |
|  **Visualization** | Created over **15 visualizations** using Matplotlib and Seaborn |

---
