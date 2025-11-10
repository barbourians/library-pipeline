# In Jupyter notebook
import sys
sys.path.append('C:\\Users\\Admin\\Documents\\GitHub\\library-pipeline\\src')

from data_processing.ingestion import load_csv, load_json

# Test CSV loading
df_circ = load_csv('../data/circulation_data.csv')
print(f"Loaded {len(df_circ)} circulation records")
print(df_circ.head())

# Test JSON loading
df_events = load_json('../data/events_data.json')
print(f"Loaded {len(df_events)} events")
print(df_events.head())
