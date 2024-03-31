import pandas as pd
data = pd.read_csv("fifa.csv")
print(data.head()) 
print(data.shape) 
print(data.info())
data = data.drop(["Photo", "Flag", "Club Logo"], axis=1) 
def convert_currency(value):
  """Converts currency strings to float, handling suffixes (M, K)."""
  if value[-1] == "M":
    return float(value[:-1]) * 1000000
  elif value[-1] == "K":
    return float(value[:-1]) * 1000
  else:
    return float(value)
data["Value"] = data["Value"].apply(convert_currency)
data["Wage"] = data["Wage"].apply(convert_currency)
data["Release Clause"] = data["Release Clause"].apply(convert_currency)
data["Value"] = data["Value"].astype(float)
data["Wage"] = data["Wage"].astype(float)
data["Release Clause"] = data["Release Clause"].astype(float)
data["Joined"] = pd.to_datetime(data["Joined"], format="%y").dt.year
data["Contract Valid Until"] = pd.to_datetime(data["Contract Valid Until"])
data["Height"] = data["Height"].str.replace('"','').astype(float)
data["Weight"] = data["Weight"].str.replace('lbs','').astype(float)
print(data.isnull().sum())
data['Potential'] = data['Potential'].fillna(data['Potential'].median())
data["Overall"].hist()
plt.xlabel("Overall Rating")
plt.ylabel("Number of Players")
plt.title("Distribution of Overall Rating")
plt.show()
top_20 = data.nlargest(20, "Overall")
top_20_players = top_20["Name"]
print(top_20_players)
top_20_df = data[data.index.isin(top_20.index)]
avg_age = top_20_df["Age"].mean()
avg_wage = top_20_df["Wage"].mean()
print(f"Average Age of Top 20 Players: {avg_age:.2f}")
print(f"Average Wage of Top 20 Players: {avg_wage:.2f}")
highest_wage_player = top_20_df.loc[top_20_df["Wage"].idxmax(), "Name"]
highest_wage = top_20_df["Wage"].max()
print(f"Player with Highest Wage: {highest_wage_player} (Wage: {highest_wage:.2f})")
player_info_df = data[["Name", "Club", "Wage", "Overall"]]
avg_overall_rating_club = player_info_df.groupby("Club")["Overall"].mean()
top_10_clubs = avg_overall_rating_club.nlargest(10).index
plt.figure(figsize=(10, 6))
avg_overall_rating_club.loc[top_10_clubs].plot(kind="bar")
plt.xlabel("Club")
plt.ylabel("Average Overall Rating")
plt.title("Average Overall Rating of Top 10 Clubs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.scatter(data["Age"], data["Potential"])
plt.xlabel("Age")
plt.ylabel("Potential")
plt.title("Relationship Between Age and Potential")
plt.show()
corr = data[["Overall", "Potential", "Value", "International Reputation", "Release Clause"]].corr()
print(corr)
wage_features = corr["Wage"].sort_values(ascending=False)[1:].index
plt.scatter(data["Overall"], data["Wage"])
plt.xlabel("Overall Rating")
plt.ylabel("Wage")
plt.title("Relationship Between Overall Rating and Wage")
plt.show()
player_position_counts = data["Preferred Position"].value_counts().sort_values(ascending=False)
max_position = player_position_counts.index[0]
min_position = player_position_counts.index[-1]
max_count = player_position_counts.iloc[0]
min_count = player_position_counts.iloc[-1]
print(f"Position with Most Players: {max_position} ({max_count} players)")
print(f"Position with Least Players: {min_position} ({min_count} players)")
player_position_counts.plot(kind="bar")
plt.xlabel("Preferred Position")
plt.ylabel("Number of Players")
plt.title("Distribution of Players by Preferred Position")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
high_wage_juventus_players = data[(data["Club"] == "Juventus") & (data["Wage"] > 200000)]
print(high_wage_juventus_players)
top_5_per_position = (
    data.groupby("Preferred Position")["Overall"]
    .sort_values(ascending=False)
    .reset_index()
    .head(5) 
)
print(top_5_per_position)
avg_wage_top_per_position = (
    top_5_per_position.groupby("Preferred Position")["Wage"]
    .mean()
    .reset_index()
)
print(avg_wage_top_per_position)