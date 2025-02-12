## **1. Motivation and Purpose**

**Role:** Data Science Consultancy for the Entertainment Industry  
**Target Audience:** Movie Enthusiasts, Reviewers, and Industry Analysts  

Movie ratings significantly impact audience decisions, yet predicting a movie’s success before its release remains a challenge. Our dashboard will provide an **interactive exploration** of movie statistics, allowing users to analyze factors affecting movie ratings. Additionally, it will enable users to **predict ratings** based on key features such as **actors, genres, directors, and writers**, helping them assess a movie’s potential success even before release.  

The dashboard serves two main purposes:
1. **Movie Statistics Exploration** – Users can search for movies, view their ratings, and analyze trends in the industry.
2. **Rating Prediction Model** – Users can input key movie features (e.g., stars, directors, genres) to estimate a movie's potential rating before release.

This tool will be useful for **casual users who want to evaluate upcoming films** and **industry professionals who need insights into movie performance** based on historical data.

---

## **2. Description of the Data**

The dataset consists of **33,600 movies** with the following key attributes:

- **Movie Details:** `Title`, `Year`, `Duration`, `MPA rating`
- **Ratings & Popularity:** `Rating`, `Votes`, `Wins`, `Nominations`, `Oscars`
- **Financials:** `Budget`, `Gross Worldwide`, `Gross US/Canada`, `Opening Weekend Gross`
- **Creators & Cast:** `Directors`, `Writers`, `Stars`, `Genres`, `Production Companies`
- **Other:** `Filming Locations`, `Languages`, `Countries of Origin`

### **Planned Features for Visualization & Prediction**
- **Statistical analysis** of ratings based on different attributes (e.g., rating distribution by genre, director, or star).
- **Correlation analysis** of factors affecting ratings (e.g., how budget impacts ratings).
- **Rating prediction model** using `Stars`, `Genres`, `Directors`, and `Writers`.

Since some attributes (e.g., budget and revenue) have missing values, **data cleaning and imputation** will be necessary before analysis.

---

## **3. Research Questions & Usage Scenarios**

### **Research Questions**
1. **Which features contribute the most to a movie’s rating?**
2. **How do movie genres and budget correlate with ratings and financial success?**
3. **Can we predict a movie’s rating based on its cast, genre, and creators?**

### **Usage Scenario 1: Movie Enthusiast Predicting a Film’s Rating**  
- *Alex is a movie fan who watches trailers before deciding which films to see. He wants to know if an upcoming movie will be worth watching, even before reviews are available.*  
- *He uses the dashboard to enter key details (actors, director, and genre) into the prediction tool, which estimates the movie’s rating.*  
- *Alex also explores past trends to see how similar movies have performed in terms of ratings and revenue.*  
- *This helps him make an informed decision about whether to watch the film on release.*  

### **Usage Scenario 2: Industry Analyst Reviewing Movie Trends**  
- *Sarah, a film analyst, wants to understand what makes a movie successful.*  
- *She explores trends in ratings based on genres, directors, and budgets.*  
- *She filters the dataset by country and production company to analyze regional performance.*  
- *Sarah uses the dashboard to build insights into industry trends and make predictions for upcoming films.*

