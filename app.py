from flask import Flask, request, jsonify
from pymongo import MongoClient, ReadPreference

app = Flask(__name__)

MONGO_URI = "mongodb+srv://hussainrazvi1524_db_user:lZ6TP81q8YrA3foI@cluster0.dvyiafp.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['ev_db']
collection = db['vehicles']

@app.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle(vin):
    result = collection.with_options(
        read_preference=ReadPreference.SECONDARY
    ).find_one({"VIN_(1-10)": vin})

    if result:
        result['_id'] = str(result['_id'])
        return jsonify(result)
    return jsonify({"error": "not found"})

@app.route('/vehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    res = collection.with_options(
        write_concern={"w": "majority"}
    ).insert_one(data)
    return jsonify({"id": str(res.inserted_id)})

@app.route('/count-tesla-primary', methods=['GET'])
def count_tesla_primary():
    total = collection.count_documents({"Make": "TESLA"})
    return jsonify({"count": total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
