from flask import Blueprint, json, jsonify, request
from libgen_api import LibgenSearch

main = Blueprint('main', __name__)

@main.route('/python/search/bookname', methods=['GET'])
def bybook():
    name = request.args.get('bookname')
    if name:
        s = LibgenSearch()
        books = s.search_title(name)
        return jsonify({"books":books})
    
@main.route('/python/search/authorname', methods=['GET'])
def byauthor():
    name = request.args.get('authorname')
    if name:
        s = LibgenSearch()
        books = s.search_author(name)
        return jsonify({"books":books})

@main.route('/python/getlink', methods=['POST'])
def getDlink():
    args = request.get_json()
    if args:
        s = LibgenSearch()
        links = s.resolve_download_links(args)
        print(links)
        return jsonify({"links" : links})