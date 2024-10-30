from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for url in data:
        if url["id"] == id:
            return jsonify(url), 200

    return {"message": "Image not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    img = request.get_json()

    existing_img = next((item for item in data if item["id"] == img["id"]), None)

    if existing_img:
        return jsonify({"Message": f"picture with id {img['id']} already present"}), 302
    
    data.append(img)
    
    return jsonify(img), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    img = request.get_json()

    existing_img = next((item for item in data if item["id"] == img["id"]), None)

    if existing_img:
        existing_img.update(img)
        return jsonify(existing_img), 200
    
    return jsonify({"Message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    existing_img = next((item for item in data if item["id"] == id), None)

    if existing_img:
        data.remove(existing_img)
        return jsonify(""), 204
    
    return jsonify({"Message": "picture not found"}), 404
