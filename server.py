import spider
from flask import Flask, jsonify, request

app = Flask(__name__)


def prepare_reponse(message, songs):
  return {
    "session": {
      "id": "session_id",
      "params": {},
      "languageCode": ""
    },
    "prompt": {
      "override": False,
      "content": {
        "media": {
          "mediaObjects": songs,
          "mediaType": "AUDIO",
        }
      },
      "firstSimple": {
        "speech": message
      }
    }
  }


@app.route('/google-action', methods=['POST'])
def google_action():
    query = request.json['intent']['query']
    query = query.replace("Play", "").replace("play", "")
    songs = spider.search(query)

    if len(songs) > 0:
        message = f"Playing {query} from MusicSpider"
    else:
        message = "No song found"

    return jsonify(prepare_reponse(message, songs[:1]))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
