# %%
import os
import pandas as pd
from functions import *
# %%
os.chdir(f"{pathlib.Path(__file__).parent.resolve()}")
print(f"Your current working directory is: {os.getcwd()}")
# %%
years = load_object("years")
all_seasons_dict = load_object("all_seasons_dict")
# %%
# initialise a df object with a "Driver Name" column
df = pd.DataFrame(columns=["Driver Name"])
# %%
for year in years:
    for gp in all_seasons_dict[f"{year}"].keys():
        x = pd.DataFrame(all_seasons_dict[f"{year}"][f"{gp}"])
        df = df.merge(x, on = "Driver Name", how = "outer")
# %%
# reorder columns such that "Driver Name" is first
df = df[["Driver Name"] + [col for col in df.columns if col != "Driver Name"]]
# %%
df.to_csv(f"{os.path.abspath(os.getcwd())}/data.csv", index = False)

# Were I to continue, I would clean the data in this .csv and go onto conduct analyses etc.