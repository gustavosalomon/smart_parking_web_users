from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Conexión a MongoDB Atlas
client = MongoClient("mongodb+srv://admin:admin123@cluster0.2owahcw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["smart_parking"]
users = db["users"]

@app.route("/api/users/register", methods=["POST"])
def register():
    data = request.get_json()
    data["dni"] = str(data["dni"])  # Forzar DNI como string

    if users.find_one({"dni": data["dni"]}):
        return jsonify({"error": "Ya existe"}), 400

    users.insert_one(data)
    return jsonify({"message": "Registrado correctamente"}), 201

@app.route("/api/users/login", methods=["POST"])
def login():
    data = request.get_json()
    dni = str(data["dni"])  # Forzar DNI como string
    password = data["password"]

    user = users.find_one({"dni": dni, "password": password})
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    user.pop("_id")
    return jsonify({"user": user}), 200

if __name__ == "__main__":
    app.run()
