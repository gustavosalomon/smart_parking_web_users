from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://admin:admin123@cluster0.2owahcw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["smart_parking"]
users = db["users"]

@app.route("/api/users/register", methods=["POST"])
def register():
    data = request.get_json()
    if users.find_one({"dni": data["dni"]}):
        return jsonify({"error": "Ya existe"}), 400
    users.insert_one(data)
    return jsonify({"message": "Registrado correctamente"}), 201

@app.route("/api/users/login", methods=["POST"])
def login():
    data = request.get_json()
    user = users.find_one({"dni": data["dni"], "password": data["password"]})
    if not user:
        return jsonify({"error": "Credenciales incorrectas"}), 401
    user.pop("_id")
    return jsonify({"user": user}), 200

@app.route("/api/users/<dni>", methods=["PUT"])
def update_user(dni):
    data = request.get_json()
    data.pop("dni", None)  # No permitir cambiar DNI
    result = users.update_one({"dni": dni}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"message": "Perfil actualizado correctamente"}), 200

@app.route("/api/users/perfil/<dni>", methods=["GET"])
def get_user_profile(dni):
    user = users.find_one({"dni": dni})
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    user.pop("_id")
    return jsonify({"user": user})

if __name__ == "__main__":
    app.run()
