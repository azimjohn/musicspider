from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def healthz():
    return jsonify({'healthy': True})


@app.route('/api/music/')
def search():
    search = request.args.get('search') 
    return jsonify({
        "next": None,
        "count": 1,
        "search": search, "results": [{
            "id": 1,
            "image": "",
            "name": "Good For You",
            "artist": "Selena Gomez"
        }]
    })


@app.route('/api/music/<int:id>/')
def get_song(id):
    return jsonify({
        "id": 1,
        "source": "https://z1.fm/download/14508776",
        "image": "",
        "name": "Good For You",
        "artist": "Selena Gomez"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
