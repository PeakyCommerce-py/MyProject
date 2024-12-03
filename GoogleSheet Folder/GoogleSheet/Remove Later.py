from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sync', methods=['POST'])
def sync_with_shopify():
    data = request.json
    print("Received data:", data)
    # Placeholder for processing data
    return jsonify({"message": "Data processed successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
