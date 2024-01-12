# pyfootballdata

A Python client for [football-data.org](football-data.org) API.

# Installation
```bash
pip install pyfootballdata
```
# Usage
```python
# Step 1: import the package
from pyfootballdata import FootballData

# Step 2: initialize the client (can be `async`)
fd = FootballData('YOUR_API_KEY') 

# Step 3: query the data 
# (e.g. standings for EPL circa 2021)
epl_standings = fd.standings(competition=2021, season=2021)
sorted_by_goals_conceded = epl_standings.overall.sort_by(
    key="goals_against", direction="desc"
)
worst_defense = sorted_by_goals_conceded[0]

print(worst_defense.team.name, worst_defense.goals_against) # Norwich City FC 84
```
# Documentation
TBA
# Examples
TBA
