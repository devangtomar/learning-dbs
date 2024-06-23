from flask import Flask, request, jsonify
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns

app = Flask(__name__)

# Connect to Cassandra
connection.setup(["localhost"], "mykeyspace", protocol_version=3)


# Define the ORM model
class User(Model):
    __keyspace__ = "mykeyspace"
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    name = columns.Text(required=True)
    email = columns.Text(required=True)


# Sync your model with the database
sync_table(User)


@app.route("/users", methods=["POST"])
def create_user():
    user = User.create(name=request.json["name"], email=request.json["email"])
    return jsonify({"message": "User created", "id": str(user.id)}), 201


@app.route("/users", methods=["GET"])
def read_users():
    users = User.objects().all()
    return jsonify(
        [{"id": str(user.id), "name": user.name, "email": user.email} for user in users]
    )


@app.route("/users/<id>", methods=["GET"])
def read_user(id):
    user = User.objects(id=id).first()
    if user:
        return jsonify({"id": str(user.id), "name": user.name, "email": user.email})
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    user = User.objects(id=id).update(
        name=request.json["name"], email=request.json["email"]
    )
    return jsonify({"message": "User updated"})


@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    User.objects(id=id).delete()
    return jsonify({"message": "User deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
