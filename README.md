# 🧭 Geospatial Machine Learning for Equitable Access to Sports and Active Mobility in Singapore

*A data-driven, AI-enhanced spatial analysis of sports facilities and cycling networks to uncover inequities and support healthier, more inclusive urban planning in Singapore.*

---

## 🌍 Project Overview

This project investigates whether **sports facilities and cycling paths are equitably distributed** across Singapore relative to **demographics (age, sex, ethnicity, income)** and **sports participation rates**.  
By integrating **open government data**, **geospatial analysis**, and **machine learning**, the project quantifies inequity in access to active-living infrastructure and proposes **data-driven recommendations** for future facility planning.

**Core Research Question:**
> Are sports facilities and cycling paths equitably distributed relative to demographics and participation rates (by age, ethnicity, sex, and income)?

---

## 🧠 Key Objectives

1. **Measure spatial access** to sports facilities and cycling paths across all Planning Areas (PAs).  
2. **Assess equity** — whether low-income, minority, or ageing populations experience lower access or participation.  
3. **Model participation behavior** using geospatial machine learning to uncover environmental and social drivers.  
4. **Identify “facility deserts”** and **recommend optimal locations** for new sports hubs or cycling connectors.  
5. **Support Singapore’s policy goals** under Smart Nation, Healthier SG, and the Green Plan 2030.

---

## 🗺️ Data Sources

All raw datasets live in `data/`. Key files and their intended sources/uses:

| File | Description | Likely Source / Notes |
|------|-------------|------------------------|
| `SportSGSportFacilitiesGEOJSON.geojson` | Polygons for SportSG / ActiveSG facilities (stadia, pools, sports halls, gyms) with rich attributes embedded in the `Description` HTML. | Based on Sport Singapore facilities layer published via data.gov.sg (SportSG Sport Facilities). |
| `Top Sports & Exercise – Overall.csv` and other `Top Sports & Exercise – *.csv` | Time series (% of population) for top sports/exercise by year and by demographic slices (age bands, sex, ethnicity). | Derived from SportSG / MCCY sports participation statistics on data.gov.sg. |
| `BarrierstoParticipationinSportPhysicalActivity2022.csv` | 2022 survey results on barriers to sport/physical activity by population segment. | Based on the "Barriers to Participation in Sport Physical Activity" dataset on data.gov.sg. |
| `MotivationstoParticipateinSportPhysicalActivity2022.csv` | 2022 survey results on motivations for sport/physical activity by population segment. | Based on the "Motivations to Participate in Sport Physical Activity" dataset on data.gov.sg. |
| `Master Plan 2019 SDCP Cycling Path layer.geojson` | Indicative cycling path alignments from URA’s Master Plan 2019 Special & Detailed Control Plans (SDCP). | URA Master Plan 2019 SDCP Cycling Path layer (via data.gov.sg). |
| `CyclingPathNetworkKML.kml` | Symbolic line representation of current cycling paths from LTA & Town Councils. | LTA / data.gov.sg cycling path network layer. |
| `NParksParksandNatureReserves.geojson` | Polygons of parks and nature reserves across Singapore. | NParks parks and nature reserves GIS layer (via data.gov.sg). |
| `ParkConnectorLoop.geojson` | Line network for Park Connector Loops and Park Connector Network segments. | NParks / URA active mobility network (park connectors) from data.gov.sg. |
| `LTABicycleRackGEOJSON.geojson` | Point locations of public bicycle racks managed by LTA. | LTA bicycle rack locations (data.gov.sg). |
| `LTAMRTStationExitGEOJSON.geojson` | Point locations of MRT station exits. | LTA MRT/LRT station exits (data.gov.sg). |
| `LTAParkingStandardsZoneGEOJSON.geojson` | Polygons for LTA parking standards zones. | LTA parking standards zones layer (data.gov.sg). |
| `HDBExistingBuilding.kml` | Footprints of existing HDB residential blocks for estimating population-supporting built form. | HDB existing building outlines (likely from data.gov.sg / OneMap planning layers). |
| `PublicTransportUtilisationAveragePublicTransportRidership.csv` | Aggregated ridership indicators for public transport, by year. | LTA / MOT public transport utilisation statistics from data.gov.sg. |
| `ResidentWorkingPersonsAged15YearsandOverbyPlanningAreaandUsualModeofTransporttoWorkGeneralHouseholdSurvey2015.csv` | Mode share to work by planning area (GHS 2015). | SingStat General Household Survey 2015 detailed tables. |
| `ResidentWorkingPersonsAged15YearsandOverbyUsualModeofTransporttoWorkAgeGroupandSexGeneralHouseholdSurvey2015.csv` | Mode share to work by age group and sex (GHS 2015). | SingStat General Household Survey 2015 detailed tables. |
| `BarrierstoParticipationinSportPhysicalActivity2022.csv` / `MotivationstoParticipateinSportPhysicalActivity2022.csv` | Attitudinal survey items on barriers & motivations towards physical activity. | SportSG / data.gov.sg survey datasets. |
| `firstlast.json`, `services.json`, `routes.geojson`, `stops.geojson` | GTFS-derived service, route and stop metadata for bus and rail networks. | Derived locally from LTA Datamall / open transit GTFS feeds (cached here for analysis). |

During analysis, these raw layers are cleaned and spatially joined (typically to URA Planning Areas, Master Plan 2019) before being aggregated to the **Planning Area (PA)** level.

---

## ⚙️ Methods and Workflow

### 1. Spatial Preprocessing
- Standardize coordinate reference (SVY21 EPSG:3414)  
- Point-in-polygon joins (facilities → PA)  
- Line-polygon intersections (cycling paths → PA)  
- Calculate per-capita and per-km² access metrics

### 2. Spatial Analytics
- **Accessibility metrics:** facility-to-population ratio, PCN km/km²  
- **Equity metrics:** Location Quotient (LQ), Gini, Theil  
- **Spatial clustering:** Moran’s I, Getis-Ord Gi* hotspot maps  
- **Needs-adjusted residuals:** access predicted by demographics → identify underserved zones

### 3. Geospatial Machine Learning
- Predict **sports participation rates** using:
  - Random Forest / XGBoost  
  - Causal Forest (for heterogeneous treatment effects)
  - SHAP analysis for feature importance
- Spatial cross-validation to prevent geographic leakage
- Interpret residuals to detect structural inequity

### 4. Visualization
- Choropleth maps of facility & PCN access  
- Lorenz curves of inequality  
- Hotspot maps of “facility deserts”  
- SHAP plots (feature influence)  
- Equity Priority Index map combining low-access + low-income + low-participation

### 5. Spatial Optimization (Future Phase)
- Genetic Algorithm / MCLP to suggest new facility or cycling hub sites  
- Optimize for coverage, equity, and cost

---

## 📈 Expected Outcomes

| Output | Description |
|--------|-------------|
| **Equity Map** | Shows planning areas with low access and participation |
| **Lorenz & Gini Plots** | Quantify spatial inequality of facilities and PCN |
| **SHAP Feature Importance** | Identifies key environmental & social predictors of participation |
| **Priority Index Map** | Combines demographic, access, and participation deficits |
| **Policy Recommendations** | Suggests where to build next sports complexes or cycling hubs |

---

## 🏛️ Policy & Strategic Alignment

This project supports Singapore’s national development goals:

| Policy / Initiative | Alignment |
|----------------------|------------|
| **Smart Nation & AI Strategy 2.0** | Uses AI/ML for urban equity and planning |
| **Healthier SG (MOH)** | Promotes preventive health through equitable active-living environments |
| **Singapore Green Plan 2030** | Encourages cycling and walking as sustainable mobility |
| **URA Long-Term Plan Review (LTPR)** | Advances “15-minute city” vision through access metrics |
| **ActiveSG Vision 2030** | Informs equitable sports facility planning |
| **LTMP 2040** | Supports Active Mobility and last-mile connectivity |
| **Forward Singapore (Empower Pillar)** | Strengthens inclusivity and community wellbeing |

---

## 🧩 Tech Stack

| Category | Tools / Libraries |
|-----------|------------------|
| **Language** | Python 3.11 |
| **Data & Geo** | GeoPandas, Shapely, Fiona, PyProj |
| **Spatial Stats** | PySAL, Esda, libpysal |
| **Machine Learning** | scikit-learn, XGBoost, SHAP |
| **Visualization** | Matplotlib, Seaborn, Folium, Kepler.gl |
| **Optimization** | OR-Tools, Pyomo, DEAP |
| **Dashboard** | Streamlit or Dash for interactive equity maps |

---

## 📂 Repository Structure

sg-sports-equity-ml/
├── data/
│ ├── data_raw/ # Raw GeoJSON, KML, CSV
│ ├── data_processed/ # Cleaned, spatially joined datasets
├── notebooks/
│ ├── 01_data_cleaning.ipynb
│ ├── 02_spatial_equity_analysis.ipynb
│ ├── 03_ml_participation_model.ipynb
│ └── 04_visualization_dashboard.ipynb
├── src/
│ ├── features/ # buffer, 2SFCA, distance metrics
│ ├── models/ # OLS, spatial regression, ML models
│ └── viz/ # mapping and plotting utilities
├── reports/ # charts, maps, and policy briefs
├── .gitignore
├── LICENSE
└── README.md


---

## 📊 Key Indicators to Compute

| Indicator | Formula | Insight |
|------------|----------|----------|
| Facility-per-capita | Facilities / Population | Service accessibility |
| PCN Density | PCN length / Land area | Active mobility infrastructure |
| Facility Location Quotient | (Area’s access / City avg access) | Relative advantage |
| Gini Coefficient | Gini(facilities per capita) | Inequality in access |
| Participation Model Coefficients | ML output | Drivers of sports participation |
| Equity Priority Index | Weighted composite | Site selection for interventions |

---

## 🚀 Expected Impact

- **For Policy:** Evidence-based infrastructure planning for SportSG, LTA, and URA  
- **For Public Health:** Identifies communities at risk of inactivity  
- **For Urban Design:** Supports 15-minute city and Active Mobility policies  
- **For Academia:** Demonstrates how AI and GIS integrate to quantify *spatial justice*  
