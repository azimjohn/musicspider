from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def healthz():
    return jsonify({'healthy': True})


@app.route('/api/music/')
def search():
    search = request.args.get('search') 
    return jsonify({"search": search,"results": []})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
