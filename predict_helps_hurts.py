import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

'''
NOTE: This does NOT actually predict what plants help others or vise versa.
The model was trained on predicting the LABELS, not the recipient.
This will need further experimentation to use recipient as labels instead
'''

class helps_hurts_classifier():
    def __init__(self, depth=3, feature_columns=['PFT_Exeter_SEv', 'Aa_sat', 'Biome_TrRF_lw'], target_column=['Link']):
        self.load_data() # initializes class data variables
        self.cleaned = self.clean_joined_data(self.joined)
        self.feature_columns = feature_columns
        self.target_column = target_column
        self.X = self.cleaned[feature_columns]
        self.y = self.cleaned[target_column]
        self.best_clf = RandomForestClassifier(max_depth=depth, random_state=79)
        self.best_clf.fit(self.X, self.y)

    def _predict(self, X):
        return self.best_clf.predict(X)
    
    def _get_filtered_full_feature_matrix(self, names : list, common=False) -> pd.DataFrame:
        ### returns calculated X feature matrix from given list of names
        ### by searching joined for name and then cleaning the row
        ### common flags whether to search by scientific (false) or common (true) name
        if common:
            scientific_names = [] # calculate all scientific for each given common name
            for name in names:
                scientific_names += self.to_scientific_species([name])[name]
            names = scientific_names

        full_feature_matrix = self.joined[self.joined['Source Scientific'].isin(names)]
        return full_feature_matrix

    def _map_prediction_to_hurts_helps(self, prediction, original_features) -> list:
        ### Maps the predicted integer values to the scientific names in the given original features list
        ### Assumes ordering is the same for predictions and features
        pred_map = {0 : 'helps', 1 : 'helped by', 2: 'avoid'}
        mapped = [pred_map[p] for p in prediction]
        df = pd.DataFrame({
            "name": original_features['Destination Scientific'],
            "result": mapped
        })
        return df
        
    
    def predict_from_name(self, names : list, is_common) -> pd.DataFrame:
        ### returns all predicted good plant pairs for a given list of names
        ### uses _get_feature_matrix and _predict
        ### is_common flags whether to search by scientific (false) or common (true) name for ALL names
        filtered_features = self._get_filtered_full_feature_matrix(names, common=is_common)
        cleaned_matrix = self.clean_joined_data(filtered_features)
        X_pred = cleaned_matrix[self.feature_columns]
        y_pred = self._predict(X_pred)
        hurts_helps = self._map_prediction_to_hurts_helps(y_pred, filtered_features)
        return hurts_helps
    
    def to_common_species(self, name : list) -> list: # keep formatting of EcoNameTranslator API, though this will always be 1-1
        name = name[0]
        filtered = self.plants_common_to_scientific[self.plants_common_to_scientific['Scientific Name with Author'].str.lower().str.contains(name.lower())]
        return {name : filtered['Common Name'].tolist()} # keep formatting of EcoNameTranslator API
        
    def to_scientific_species(self, name : list) -> list: # keep formatting of EcoNameTranslator API
        name = name[0]
        filtered = self.plants_common_to_scientific[self.plants_common_to_scientific['Common Name'].str.lower().str.contains(name.lower())]
        return {name : filtered['Scientific Name with Author'].tolist()} # keep formatting of EcoNameTranslator API
    
    def load_data(self):
        self.pairs_df_full = pd.read_csv('datasets/companion_plants.csv')
        self.plants_common_to_scientific = pd.read_csv('datasets/plantlst.txt', delimiter=',')
        self.plant_feature_data_df = pd.read_csv('datasets/GlobResp database_Atkin et al 2015_New Phytologist.csv')

        self.plants_common_to_scientific = self.plants_common_to_scientific[['Scientific Name with Author', 'Common Name']]
        self.plants_common_to_scientific['Scientific Name with Author'] = self.plants_common_to_scientific['Scientific Name with Author'].str.split().str[:2].str.join(sep=" ") # take first 2 words
        self.plants_common_to_scientific = self.plants_common_to_scientific.dropna(ignore_index=True)
        
        # this uses the above function to query plantlst.txt instead of any API, making it much faster (but less accurate, in theory)
        scientific_names_source_helps_or_hurts_destination = []
        already_looked_up_names = {} # store calculations to avoid repeating them
        unique_common_names = self.pairs_df_full['Source Node'].unique()
        for name in tqdm(unique_common_names, position=0, desc='Source common names'):
            # check if name is already looked up
            if name not in already_looked_up_names:
                source_scientific_names = self.to_scientific_species([name])[name] # add all scientific names linked to source's common name
                already_looked_up_names[name] = source_scientific_names # store to avoid recalculating
            else:
                source_scientific_names = already_looked_up_names[name] # get already calculated result

            target_source_rows = self.pairs_df_full[self.pairs_df_full['Source Node'] == name] # get all rows with this name
            for row in target_source_rows.itertuples(): # iterate over all destinations as tuple list (needs indexing) 
                link = row[2] # Link; helps, hurts, or helped by
                destination_node = row[3] # Destination Node; what the other plant is
                # check if name is already looked up
                if destination_node not in already_looked_up_names:
                    destination_scientific_names = self.to_scientific_species([destination_node])[destination_node] # get all scientific names of the other plant
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
        hurts_help_df = pd.DataFrame(scientific_names_source_helps_or_hurts_destination)
        self.joined = pd.merge(left=hurts_help_df, right=self.plant_feature_data_df, left_on='Source Scientific', right_on='Species')
        return None # stored as class variables instead

    def clean_joined_data(self, joined_data : pd.DataFrame):
        cleaned = joined_data.copy()
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

if __name__ == '__main__':
    predictor = helps_hurts_classifier()
    prediction = predictor.predict_from_name('tomato', is_common=True)
    json = prediction.to_json(orient='index')
    print(json)

    # scientific_results = predictor.to_scientific_species(['tomato'])['tomato']
    # common_result = predictor.to_common_species([scientific_results[0]])
    # print('scientific results:', scientific_results)
    # print('common result:', common_result)
