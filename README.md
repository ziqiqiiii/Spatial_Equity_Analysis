# Equitable Access to Sports & Active Mobility in Singapore

A Spatial Data Science project auditing the fairness of public sports facility distribution (Gyms, Pools, Stadiums) across Singapore's HDB towns.

---

## Project Goal

To answer a critical urban planning question: Does the location of sports facilities match the population density of the residents who need them?

---

## Assumptions
***Behavioral (Human Factors)***

| Assumption | Details |
|---|---|
| Active mobility mode | Residents access facilities by walking only; public transit and private vehicles are excluded to model a conservative accessibility scenario (15-minute city). |
| Trip origin | All trips originate from the resident’s home address (census residence); trips from workplaces, schools, or transit nodes are not considered. |
| Willingness to walk (distance decay) | Walk time capped at 20 minutes (~1.6 km); facilities beyond this range contribute 0 to accessibility. |
| Walking speed | A constant walking speed of 4.8 km/h is used to convert network distance to travel time. |
| Cross-boundary movement | Residents can use facilities across administrative boundaries; nearest facility is assumed regardless of town borders. |
| Rational agent behavior | Residents choose the shortest network path, ignoring preferences like scenery, shade (unless modeled), or perceived safety. |

***Operational (Supply Side)***

| Assumption | Details |
|---|---|
| Public equity scope | Only public facilities (SportSG gyms/pools, parks, PCNs) included; private condos, country clubs, and commercial gyms are excluded. |
| Facility availability | All mapped facilities assumed operational and open; temporary closures or booking limits are not modeled. |

***Methodological (Data Constraints)***

| Assumption | Details |
|---|---|
| Population distribution | With confidential address-level data, population is assumed uniformly distributed within each Planning Area (PA). |
| Network topology | OSM pedestrian network assumed complete and traversable; major barriers (expressways, rivers) require mapped crossings (bridges). |


---


## Methodology (The 5-Step Approach)

**1. 2SFCA (Two-Step Floating Catchment Area):**
  - Measured accessibility based on Network Distance (walking paths), not straight lines.
  - Accounted for "crowding" (Capacity vs. Population size).

**2. KDE (Kernel Density Estimation):**
  - Created "Human Heatmaps" to visualize where demand actually lives versus where facilities are built.

**3. LQ (Location Quotient):**
  - Compared each town against the National Average to identify which estates are "Overserved" vs "Underserved."

**4. Gini Coefficient:**
  - Calculated a single "Inequality Score" (0-1) to quantify the gap between Mature and Non-Mature estates.

**5. Hotspot Analysis (Getis-Ord Gi):**
  - Statistically identified "Fitness Deserts" (Cold Spots) to recommend optimal locations for new infrastructure.

---

## Data Sources

| Source | Details |
|---|---|
| Population | Resident Households (General Household Survey 2015). |
| Infrastructure | SportSG, Parks, PCN (Park Connector Network), CPN (Cycling Path Network). |
| Planning Area | Master Plan 2019 Planning Area, Master Plan 2019 Subzone. |
| Street Network | OpenStreetMap (via OSMnx) for walkable routes. |

---

## Tech Stack

**Python**: Pandas, NumPy
**Geospatial**: GeoPandas, OSMnx, PySAL
**Viz**: Folium, Streamlit

---

## 📂 Repository Structure

```text
├── data/
│   ├── data_raw/                 # Shapefiles, Census CSVs
│   └── data_cleaned/           # Cleaned GeoJSONs with computed scores
├── notebooks/
│   ├── 01_Data_Prep.ipynb   # Cleaning & Demographic Weighting
│   ├── 02_Network_Analysis.ipynb # 2SFCA & OSMnx Routing
│   ├── 03_Inequality_Metrics.ipynb # LQ & Gini Calculation
│   └── 04_Hotspot_Modeling.ipynb # Getis-Ord Gi*
├── RESOURCES.md
└── README.md
```

---
### Resources 
[Resources readme](./RESOURCES.md)

