import json
import requests
from flask import Flask, request, Response
from uvicorn import run

app = Flask(__name__)
app.debug = True

@app.route('/api/data', methods=['GET'])
def get_data():
    json_url = request.args.get('json_url')
    start = request.args.get('start')
    end = request.args.get('end')
    limit = request.args.get('limit')

    try:
        response = requests.get(json_url)
        response.raise_for_status()
        json_data = response.json()

        if start:
            start = int(start)
        else:
            start = 0

        if end:
            end = int(end)
        else:
            end = len(json_data)

        if limit:
            limit = int(limit)
            end = start + limit

        response_data = json_data[start:end]
        response = Response(json.dumps(response_data), mimetype='application/json')
        return response

    except requests.exceptions.RequestException as e:
        error_msg = f"Error retrieving data: {e}"
        return Response(json.dumps({"error": error_msg}), status=500, mimetype='application/json')

    except Exception as e:
        error_msg = f"An error occurred: {e}"
        return Response(json.dumps({"error": error_msg}), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
