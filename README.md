#  IMDB Movie Analysis Dashboard  

## **Overview**
This Dash-powered web application provides interactive visualizations and predictive analytics for movie profitability using IMDB data. The dashboard allows users to explore key movie attributes, compare trends, and predict the profitability of a movie based on its genre, lead star, director, and budget.  

Using dataset: https://www.kaggle.com/datasets/raedaddala/top-500-600-movies-of-each-year-from-1960-to-2024

**Heroku Link:** https://data551-dash-live-b51d7a902ddb.herokuapp.com/

##  Features  

### 1️⃣ **Data Exploration & Visualization**  
- **Scatter Plot** – Compare relationships between different numerical features (e.g., Rating vs. Gross Worldwide).  
- **Line Plot** – Visualize trends over time.  
- **Histogram** – Show the distribution of a selected movie feature.  
- **Bar Chart** – Compare average values of different genres.  
- **Box Plot** – Display the spread of movie attributes by genre.  
- **Pie Chart** – Show aggregate metrics such as total or average gross earnings per genre.  

### 2️⃣ **Statistics & Insights**  
- **Top 10 by Average Rating** – Identify the best-performing writers, directors, and stars within a selected genre.  
- **Data Table Preview** – Browse the processed movie dataset.  

### 3️⃣ **Movie Profitability Prediction**  
- Enter a **movie genre, lead star, director, and budget** to predict:  
  - **Profitability category** (e.g., `1.6+`, `2.0+` gross-to-budget ratio).  
  - **Estimated gross-to-budget ratio** based on historical data and a trained Random Forest model.  

##  Technologies Used  
- **Dash & Dash Bootstrap Components** – Interactive web UI  
- **Altair** – Data visualization  
- **Pandas & NumPy** – Data manipulation  
- **Scikit-Learn** – Machine learning models (Random Forest for classification & regression)  
- **Regex & AST** – Data cleaning and transformation  

##  Data Preprocessing  
- Converted duration from `hh:mm` format to minutes.  
- Mapped detailed movie genres into broader categories.  
- Encoded categorical variables (`genres`, `directors`, `stars`).  
- Created new features: **profit**, **gross-to-budget ratio**, and **profitability category**.  
- Removed extreme outliers and missing values.  

##  Machine Learning Models  
- **Profitability Category Prediction**: Random Forest Classifier  
- **Gross/Budget Ratio Prediction**: Random Forest Regressor  
- Model trained on `genres`, `lead star`, `director`, and `budget` features.  

##  Deployment  
To deploy on **Heroku**

## **Sketch**
A dashboard sketch will be linked below showing the interface layout and key visualization elements.

![Dashboard Sketch](img/AppSketch.PNG)