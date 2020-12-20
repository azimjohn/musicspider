import spider
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def healthz():
    return jsonify({'healthy': True})


@app.route('/api/music/')
def search_handler():
    query = request.args.get('search')
    songs = spider.search_z1(query)
    return jsonify({
        "next": None,
        "count": len(songs),
        "results": songs
    })


@app.route('/api/music/<int:id>/')
def get_song_handler(id):
    song = es.get(index="songs", id=id)
    song['_source']['id'] = int(song['_id'])
    return jsonify(song['_source'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
