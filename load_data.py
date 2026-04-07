import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://hussainrazvi1524_db_user:lZ6TP81q8YrA3foI@cluster0.dvyiafp.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['ev_db']
collection = db['vehicles']

def load_and_upload():
    df = pd.read_csv('ev_data.csv')
    df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]

    records = df.to_dict('records')
    batch_size = 5000

    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        collection.insert_many(batch)
        print(f"{i} -> {i + len(batch)}")

if __name__ == "__main__":
    load_and_upload()
