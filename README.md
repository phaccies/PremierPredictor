# PremierPredictor

## Overview  
PremierPredictor is a Python-based app that scrapes current Premier League data from the Sky Sports website using BeautifulSoup. The app provides visualizations and predictions for the league's outcome at the end of the season based on Monte Carlo simulations.  

## Features  
- Scrapes Premier League data using BeautifulSoup.  
- Visualizes "Goals For" and "Goals Against" statistics in a scatter plot.  
- Predicts final league standings using a Monte Carlo simulation (10,000 iterations, can be changed).  
- Outputs team statistics to an Excel spreadsheet.  

## Technologies  
- **Python**: Core language used.  
- **BeautifulSoup**: For web scraping.  
- **pandas**: For data manipulation and storage.  
- **matplotlib**: For data visualization.  

## Future Plans  
- Deploy the app using Flask to make it interactive.  
- Incorporate match difficulty into simulations (e.g., factoring in the varying difficulty levels of matches like Liverpool vs. Man City compared to Liverpool vs. Wolves).  
