from flask import request,jsonify
from . import api
from ai.service.trainModel import reviewModel
from ai.service.handleData import prepareData

@api.route('/tests', methods=['GET'])
def review():
    # preparedata = prepareData()
    model = reviewModel()
    res = model.trainModel()
    return jsonify({"data":res})