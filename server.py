from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

es = Elasticsearch()
app = Flask(__name__)


def search(text):
    songs = []
    result = es.search(index='songs', body={
        "from": 0, "size": 100, "query": {
            "match": {"name": text}
        }
    })

    for song in result['hits']['hits']:
        song['_source']['id'] = song['_id']
        songs.append(song['_source'])

    return songs


@app.route('/')
def healthz():
    return jsonify({'healthy': True})


@app.route('/api/music/')
def search_handler():
    query = request.args.get('search')
    songs = search(query)
    return jsonify({
        "next": None,
        "count": len(songs),
        "results": songs
    })


@app.route('/api/music/<int:id>/')
def get_song_handler(id):
    song = es.get(index="songs", id=id)
    song['_source']['id'] = song['_id']
    return jsonify(song['_source'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
