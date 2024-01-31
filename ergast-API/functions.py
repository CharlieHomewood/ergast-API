# %%
import os
import pickle
import pathlib
# %%
os.chdir(f"{pathlib.Path(__file__).parent.resolve()}")
print(f"Your current working directory is: {os.getcwd()}")
# %%
# function to save objects as .pkl files
def save_object(object, filename):
    
    # make sure the filename ends with ".pkl"
    if not filename.endswith('.pkl'):
        filename += '.pkl'
    
    # append the pkl directory to the beginning of the filename
    filename = os.path.join(os.getcwd(), "pkl", filename)
    
    # using the filename, create a new .pkl file and store the object inside it
    with open(filename, 'wb') as f:
        pickle.dump(object, f)

# function to load created .pkl files
def load_object(filename):
    
    # make sure the filename ends with ".pkl"
    if not filename.endswith('.pkl'):
        filename += '.pkl'
    
    # append the pkl directory to the beginning of the filename
    filename = os.path.join(os.getcwd(), "pkl", filename)
    
    # if the filename exists, open that file and load the object
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    
    # else, return an error saying the file does not exist
    else:
        raise FileNotFoundError(f"File '{filename}' does not exist.")
# %%
