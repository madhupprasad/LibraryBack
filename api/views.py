from flask import Blueprint, jsonify, request
from libgen_api import LibgenSearch

main = Blueprint('main', __name__)

@main.route('/search/bybook', methods=['GET'])
def bybook():
    name = request.args.get('bookname')
    if name:
        s = LibgenSearch()
        books = s.search_title(name)
        return jsonify({"books":books})
    
@main.route('/search/byauthor', methods=['GET'])
def byauthor():
    name = request.args.get('authorname')
    if name:
        s = LibgenSearch()
        books = s.search_author(name)
        return jsonify({"books":books})
    