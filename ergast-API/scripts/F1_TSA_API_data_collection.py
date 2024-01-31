# %%
import requests
import fastf1
import pandas as pd
import time
import os
import pathlib
from functions import * # functions I created, contained in functions.py
# %%
os.chdir(f"{pathlib.Path(__file__).parent.resolve()}")
print(f"Your current working directory is: {os.getcwd()}")
# %%
baseurl = "https://ergast.com/api/f1/{year}/{gp}/results.json" # the template url to be used
urls = [] # initialise an empty list for the urls
years = list(range(1958, 2024)) # list of seasons to be sampled, starts 1958 as this is start of shared cars ban (/driverStandings.json has key-value pairs for each driver, but not each car number)
maxgps = [] # initialise an empty list for the number of GPs in each season
all_seasons_dict = {} # initialise dictionary for all the seasons
dfs = [] # initialise list for GP data frames

save_object(years, "years") # save the years object as a .pkl
# %%
# get the number of GPs in each season
for year in years:
    maxgp = max(fastf1.get_event_schedule(year)["RoundNumber"])
    maxgps.append(maxgp)

# for each year, loop through each GP and grab the url for that GP and add it to the `urls` list
for year, maxgp in zip(years, maxgps):      
    gps = range(1, maxgp + 1)
    for gp in gps:
        url = baseurl.format(year = year, gp = gp)
        urls.append(url)
# %%
for url in urls:
    
    print(f"Starting: {url}")
    
    r = requests.get(url, params={"limit": "1000"}).json()
    total_drivers = int(r["MRData"]["total"])
    season_key = str(r["MRData"]["RaceTable"]["season"])
    
    if total_drivers > 0:
        
        if season_key not in all_seasons_dict:
            all_seasons_dict[season_key] = {}
        
        race_name = str(r["MRData"]["RaceTable"]["Races"][0]["raceName"])
        drivers = r["MRData"]["RaceTable"]["Races"][0]["Results"]
        
        position_list = [] # initialise list for each position for each GP
        driverId_list = [] # initialise list for each of the driver's last names for each GP
        
        for driver in drivers:
            
            position_list.append(int(driver["position"]))
            driverId_list.append(str(driver["Driver"]["driverId"]))
            
            race_info = {f"{season_key} {race_name} Position": position_list, "Driver Name": driverId_list}
        
        all_seasons_dict[season_key].update({race_name: race_info})
        
    else:
        continue
    
    save_object(all_seasons_dict, "all_seasons_dict.pkl")
    print(f"Finished: {url}")
    print("-" * 50)
    time.sleep(18) # API has max 200 requests per hour. 3600 seconds in 1 hour. therefore, 3600 / 200 = 18 seconds delay between each iteration will ensure rate limit is not hit.