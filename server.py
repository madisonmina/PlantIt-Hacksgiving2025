import sys
import json
import traceback
import pandas as pd
import networkx as nx

def main():
    try:
        # 1. Parse input JSON from command-line argument
        raw = sys.argv[1] if len(sys.argv) > 1 else ""
        payload = json.loads(raw) if raw else {}
        selected_plants = payload.get("plants", [])
        
        if not selected_plants:
            raise ValueError("No plants provided in the input.")
        
        # 2. Load your dataset
        df = pd.read_csv("groupable_data.csv")
        
        # 3. Build link_targets dictionary
        help_df = df[df["Predicted Link"] == 0]  # only "helps"
        link_targets_dict = help_df.groupby("Species")["Destination Scientific"].apply(list).to_dict()
        
        # 4. Build graph
        G = nx.Graph()
        for plant in selected_plants:
            targets = link_targets_dict.get(plant, [])
            for t in targets:
                if t in selected_plants:  # only connect selected plants
                    G.add_edge(plant, t)
        
        # 5. Find mutually connected groups
        groups = [list(g) for g in nx.connected_components(G)]
        
        # 6. Throw error if no plant is part of a group
        if not groups:
            raise ValueError("No mutually helping groups found among the selected plants.")
        
        # 7. Return JSON
        result = {"ok": True, "groups": groups}
        print(json.dumps(result))
        
    except Exception as e:
        tb = traceback.format_exc()
        print(tb, file=sys.stderr)
        print(json.dumps({"ok": False, "error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
