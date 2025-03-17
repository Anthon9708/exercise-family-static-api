"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/add' , methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        # print(data)
        if data:
            jackson_family.add_member(data)
            return jsonify( data ) , 200
        return jsonify({ "error" : "Invalid data"}), 400
    except Exception :
        return jsonify({"error": str(Exception)}), 500
    
@app.route('/member/<int:id>' , methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200 
    else:
        return jsonify({ "error": "Member not found"}), 404
    
@app.route('/delete/<int:id>' , methods=['DELETE'])
def delete_member(id):
    try:
        member_delete = jackson_family.delete_member(id)
        if member_delete:
            return jsonify({ "done" : True}), 200
        return jsonify({ "error" : "invalid data"})
    except Exception:
        return jsonify({ "error" : str(Exception)}), 500
    
@app.route('/update/<int:id>' , methods=['PUT'])
def update_member(id):
    try:
        data = request.get_json()
        data_update = jackson_family.update_member(id , data)
        if data_update:
            return jsonify(data_update), 200
        return jsonify({ "error" : "invalid data"})
    except Exception:
        return jsonify({ "error" : str(Exception)}), 500


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
