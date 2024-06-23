from flask import Flask, request, jsonify
import cassandra.cluster

app = Flask(__name__)

# Connect to Cassandra
cluster = cassandra.cluster.Cluster(["localhost"], port=9042)
session = cluster.connect("mykeyspace")


@app.route("/users", methods=["POST"])
def create_user():
    user = request.json
    query = "INSERT INTO users (id, name, email) VALUES (uuid(), %s, %s)"
    session.execute(query, (user["name"], user["email"]))
    return jsonify({"message": "User created"}), 201


@app.route("/users", methods=["GET"])
def read_users():
    rows = session.execute("SELECT * FROM users")
    users = [{"id": str(row.id), "name": row.name, "email": row.email} for row in rows]
    return jsonify(users)


@app.route("/users/<id>", methods=["GET"])
def read_user(id):
    row = session.execute("SELECT * FROM users WHERE id = %s", [id]).one()
    if row:
        return jsonify({"id": str(row.id), "name": row.name, "email": row.email})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user = request.json
    session.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (user["name"], user["email"], id),
    )
    return jsonify({"message": "User updated"})


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    session.execute("DELETE FROM users WHERE id = %s", [id])
    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
