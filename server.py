import spider
from flask import Flask, jsonify, request

app = Flask(__name__)


response = {
  "session": {
    "id": "session_id",
    "params": {},
    "languageCode": ""
  },
  "prompt": {
    "override": False,
    "content": {
      "media": {
        "mediaObjects": [],
        "mediaType": "AUDIO",
      }
    },
    "firstSimple": {
      "speech": ""
    }
  }
}


@app.route('/google-action', methods=['POST'])
def google_action():
    query = request.json['intent']['query']
    query = query.replace("Play", "").replace("play", "")

    songs = spider.search_z1(query)

    media = [{"name": song["name"], "url": song["source"]} for song in songs[:1]]
    response["prompt"]["content"]["media"]["mediaObjects"] = media

    if len(songs) > 0:
        message = f"Playing {query} from MusicSpider"
    else:
        message = "No song found"

    response["prompt"]["firstSimple"]["speech"] = message

    return jsonify(response)

"""
@app.route('/api/music/')
def search_handler():
    query = request.args.get('search')
    songs = spider.search_z1(query)
    return jsonify({
        "next": None,
        "count": len(songs),
        "results": songs
    })
"""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
