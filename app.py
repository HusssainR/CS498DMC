from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference
from pymongo.write_concern import WriteConcern

app = Flask(__name__)

MONGO_URI = "mongodb+srv://hussainrazvi1524_db_user:lZ6TP81q8YrA3foI@cluster0.dvyiafp.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['ev_db']
collection = db['vehicles']

@app.route('/insert-fast', methods=['POST'])
def insert_fast():
    data = request.json
    coll = collection.with_options(write_concern=WriteConcern(w=1))
    res = coll.insert_one(data)
    return jsonify({"inserted_id": str(res.inserted_id)}), 201

@app.route('/insert-safe', methods=['POST'])
def insert_safe():
    data = request.json
    coll = collection.with_options(write_concern=WriteConcern(w="majority"))
    res = coll.insert_one(data)
    return jsonify({"inserted_id": str(res.inserted_id)}), 201

@app.route('/count-tesla-primary', methods=['GET'])
def count_tesla_primary():
    coll = collection.with_options(read_preference=ReadPreference.PRIMARY)
    total = coll.count_documents({"Make": "TESLA"})
    return jsonify({"count": total}), 200

@app.route('/count-bmw-secondary', methods=['GET'])
def count_bmw_secondary():
    coll = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    total = coll.count_documents({"Make": "BMW"})
    return jsonify({"count": total}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
