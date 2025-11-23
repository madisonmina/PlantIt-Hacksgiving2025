import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import StandardScaler
import random

class helps_hurts_classifier():
    def __init__(self, X, y, depth=3):
        self.X = X
        self.y = y
        self.best_clf = RandomForestClassifier(max_depth=depth, random_state=79)
        self.best_clf.fit(X, y)
    def predict(self, X):
        return self.best_clf.predict(X)
    
def load_data():
    pairs_df_full = pd.read_csv('datasets/companion_plants.csv')
    plants_common_to_scientific = pd.read_csv('datasets/plantlst.txt', delimiter=',')
    plants_common_to_scientific = plants_common_to_scientific[['Scientific Name with Author', 'Common Name']]
    plants_common_to_scientific['Scientific Name with Author'] = plants_common_to_scientific['Scientific Name with Author'].str.split().str[:2].str.join(sep=" ") # take first 2 words
    plants_common_to_scientific = plants_common_to_scientific.dropna(ignore_index=True)
    def to_species(name : list) -> list: # keep formatting of EcoNameTranslator API
        name = name[0]
        filtered = plants_common_to_scientific[plants_common_to_scientific['Common Name'].str.lower().str.contains(name.lower())]
        return {name : filtered['Scientific Name with Author'].tolist()} # keep formatting of EcoNameTranslator API
    
    # this uses the above function to query plantlst.txt instead of any API, making it much faster (but less accurate, in theory)
    scientific_names_source_helps_or_hurts_destination = []
    already_looked_up_names = {} # store calculations to avoid repeating them
    unique_common_names = pairs_df_full['Source Node'].unique()
    for name in tqdm(unique_common_names, position=0, desc='Source common names'):
        # check if name is already looked up
        if name not in already_looked_up_names:
            source_scientific_names = to_species([name])[name] # add all scientific names linked to source's common name
            already_looked_up_names[name] = source_scientific_names # store to avoid recalculating
        else:
            source_scientific_names = already_looked_up_names[name] # get already calculated result

        target_source_rows = pairs_df_full[pairs_df_full['Source Node'] == name] # get all rows with this name
        for row in target_source_rows.itertuples(): # iterate over all destinations as tuple list (needs indexing) 
            link = row[2] # Link; helps, hurts, or helped by
            destination_node = row[3] # Destination Node; what the other plant is
            # check if name is already looked up
            if destination_node not in already_looked_up_names:
                destination_scientific_names = to_species([destination_node])[destination_node] # get all scientific names of the other plant
                already_looked_up_names[destination_node] = destination_scientific_names
            else: 
                destination_scientific_names = already_looked_up_names[destination_node]
            # we want to add all pairs of source and destination scientific names to the new dataframe
            for source_name in source_scientific_names:
                for destination_name in destination_scientific_names:
                    scientific_names_source_helps_or_hurts_destination.append({
                        'Source Common' : name,
                        'Source Scientific' : source_name,
                        'Destination Common' : destination_node,
                        'Destination Scientific' : destination_name,
                        'Link' : link
                    })
    plant_feature_data_df = pd.read_csv('datasets/GlobResp database_Atkin et al 2015_New Phytologist.csv')
    hurts_help_df = pd.DataFrame(scientific_names_source_helps_or_hurts_destination)
    joined = pd.merge(left=hurts_help_df, right=plant_feature_data_df, left_on='Source Scientific', right_on='Species')
    return joined

def clean_data(data : pd.DataFrame):
    cleaned = data.copy()
    # NaN's
    cleaned = cleaned.dropna(how='all')
    cleaned = cleaned.fillna(0.0)
    # convert target 'Link' feature to int
    link_categories = cleaned['Link'].unique()
    cat_to_int = {cat: i for i, cat in enumerate(link_categories)}
    cleaned['Link'] = [cat_to_int[val] for val in cleaned['Link']]
    cleaned['Link'] = cleaned['Link'].astype(int)
    # filter columns
    categorical_columns = ['Country', 'Biome', 'Site', 'Latitude', 'Longitude',
                        'PFT_LPJ', 'PFT_Sheffield', 'PFT_JULES', 'PFT_Wright', 'PFT_JULES2', 'PFT_Exeter' # plant functional type
    ]
    cleaned[categorical_columns] = cleaned[categorical_columns].astype('category')
    numeric_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
    columns_to_keep = categorical_columns + numeric_cols
    cleaned = cleaned[columns_to_keep] # filter
    # convert categorical to one-hot-encoded dummy ints (0 = helps, 1 = helped_by, 2 = avoid)
    cleaned = pd.get_dummies(cleaned, columns=categorical_columns)
    scaler = StandardScaler()
    for col in numeric_cols:
        if col != 'Link': # don't scale target int column!
            cleaned[col] = scaler.fit_transform(cleaned[col].to_numpy().reshape(-1, 1))
    return cleaned

data = load_data()
cleaned = clean_data(data)
X = cleaned[['PFT_Exeter_SEv', 'Aa_sat', 'Biome_TrRF_lw']]
y = cleaned['Link']
predictor = helps_hurts_classifier(X, y)
predictor.predict(X)

# TODO: add functions to predict from common and scientific name