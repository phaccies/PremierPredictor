# App that scrapes Premier League Stats [IP]

import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

url = "https://www.skysports.com/premier-league-table"

scrape_page = requests.get(url)
soup = BeautifulSoup(scrape_page.text, "html.parser")

#print(scrape_page.text) to test if website is scrapable 

#TEAM NAMES
teams = soup.find_all("span", attrs={"data-short-name": True})
team_names = [team["data-short-name"] for team in teams]

#MATCHES PLAYED
matches_played = soup.find_all("td", attrs={"data-live-key":"pld"})
#Access the span within the td + strip (take away the \n and whitespace stuff) the text
matches_played_values = [td.find("span").text.strip() for td in matches_played]

#WINS
wins = soup.find_all("td", attrs={"data-live-key":"w"})
wins_values = [td.find("span").text.strip() for td in wins]

#DRAWS
draws = soup.find_all("td", attrs={"data-live-key":"d"})
draws_values = [td.find("span").text.strip() for td in draws]

#LOSSES
losses = soup.find_all("td", attrs={"data-live-key":"l"})
losses_values = [td.find("span").text.strip() for td in losses]

#GF
goals_for = soup.find_all("td", attrs={"data-live-key":"f"})
goals_for_values = [td.find("span").text.strip() for td in goals_for]

#GA
goals_against = soup.find_all("td", attrs={"data-live-key":"a"})
goals_against_values = [td.find("span").text.strip() for td in goals_against]

#GD
goals_diff = soup.find_all("td", attrs={"data-live-key":"gd"})
goals_diff_values = [td.find("span").text.strip() for td in goals_diff]

#PTS
points = soup.find_all("td", attrs={"data-live-key":"pts"})
points_values = [td.find("span").text.strip() for td in points]

team_info = []

for i in range(len(team_names)):
    team_dict = {
        "Team": team_names[i],
        "Matches Played": matches_played_values[i],
        "Wins": wins_values[i],
        "Draws": draws_values[i],
        "Losses": losses_values[i],
        "Goals For": goals_for_values[i],
        "Goals Against": goals_against_values[i],
        "Goal Difference": goals_diff_values[i],
        "Points": points_values[i]
    }
    
    # Add the dictionary to the list
    team_info.append(team_dict)

df = pd.DataFrame(team_info)

#Win Rate
df["Win Rate"] = (df["Wins"].astype(int) / df["Matches Played"].astype(int) * 100).round(2)
df["Win Rate"] = df["Win Rate"].apply(lambda x: f"{x:.0f}%") #Converts to string + adds the % symbol @ end


#Loss Rate
df["Loss Rate"] = (df["Losses"].astype(int) / df["Matches Played"].astype(int) * 100).round(2)
df["Loss Rate"] = df["Loss Rate"].apply(lambda x: f"{x:.0f}%") #Converts to string + adds the % symbol @ end

#Draw Rate
df["Draw Rate"] = (df["Draws"].astype(int) / df["Matches Played"].astype(int) * 100).round(2)
df["Draw Rate"] = df["Draw Rate"].apply(lambda x: f"{x:.0f}%") #Converts to string + adds the % symbol @ end


#Points Per Game
df["PPG"] = round(df["Points"].astype(int) / df["Matches Played"].astype(int))

#Goals Per Game
df["GPG"] = round(df["Goals For"].astype(int) / df["Matches Played"].astype(int))

#Scatter Plot Stuff showing the GF + GA for each team in PL 
goals_scored = df["Goals For"].astype(int)
goals_conceded = df["Goals Against"].astype(int)
team_names = df["Team"]

plt.figure(figsize=(10, 6))
plt.scatter(goals_scored, goals_conceded, color="blue", alpha=0.7, edgecolor="black") 
#color="blue": Sets the color of the points.  (Explanations so ik what's happening when I read this again)
#alpha=0.7: Makes the points slightly transparent.
#edgecolor="black": Adds a border to the points.

plt.xlabel("Goals For (Scored)")
plt.ylabel("Goals Against (Conceded)")
plt.title("Goals Scored vs. Goals Conceded in Premier League")
plt.grid(True)

#Label each point w the corresponding team
for i, team in enumerate(team_names):
    plt.text(goals_scored[i] + 0.2, goals_conceded[i], team, fontsize=8)

#plt.show()  #uncomment me!


#df.to_excel("books.xlsx")
#df.to_csv("books.csv")


##################### MONTE CARLO SIMULATION OF WHO WILL WIN PL + FINAL TABLE PREDICTIONS  ##########################

#Note: Sims don't take vs into account. Ex: Chelsea vs Liverpool will have the same probability as Southampton vs Liverpool
#So the final result is basically if things keep going how they are. Hoping to integrate this in the future ^^

#All PL teams play total 38 games. All teams rn with the exception of Liverpool has played 19.
#So I will be using 19 srry Liverpool lol (they're alr ahead by so much so don't know if it'll matter that much tbh)
games_left = 19 

#Function to simulate remaining matches 
def simulate_matches(win_rate, draw_rate, loss_rate, games_left):
    outcomes = np.random.choice(
    ["win", "draw", "loss"], 
    size=games_left, 
    p=[win_rate, draw_rate, loss_rate] #p is probability for win, draw, loss
)
    points = sum([3 if result == "win" else 1 if result == "draw" else 0 for result in outcomes])
    #remember sum pretty much adds everything in a list/arr. so like sum[1,2,3] is 6
    return points


#Convert rates to decimals
df["Win Prob"] = df["Wins"].astype(int) / df["Matches Played"].astype(int)
df["Draw Prob"] = df["Draws"].astype(int) / df["Matches Played"].astype(int)
df["Loss Prob"] = df["Losses"].astype(int) / df["Matches Played"].astype(int)

#Running 10,000 simulations to predict final table points
num_sims = 10000

#Adding a col to store the avg simulated points
df["Simulated Points"] = 0

# Number of simulations
num_simulations = 10000

# Add a column to store the average simulated points
df["Simulated Points"] = 0

#Loop through each team
for index, row in df.iterrows():
    simulated_points = []
    for _ in range(num_simulations):
        points = simulate_matches(
            row["Win Prob"], 
            row["Draw Prob"], 
            row["Loss Prob"], 
            games_left
        )
        simulated_points.append(points)
    #Store the average points from all simulations
    df.at[index, "Simulated Points"] = int(row["Points"]) + round(sum(simulated_points) / num_simulations)


#df.to_excel("books.xlsx")

#Sort teams by simulated points in descending order
df = df.sort_values(by="Simulated Points", ascending=False)

#Reset index for readability
df.reset_index(drop=True, inplace=True)

print(df[["Team", "Points", "Simulated Points"]])

#Graph for Predicted Final Table 
plt.figure(figsize=(12, 8))
plt.bar(df["Team"], df["Simulated Points"], color="skyblue")
plt.xlabel("Team")
plt.ylabel("Simulated Final Points")
plt.title("Predicted Final Points for Premier League Teams")
plt.xticks(rotation=45, ha="right")
plt.show() #(Will show this graph + scatter plot from b4)


df.to_excel("books.xlsx")


