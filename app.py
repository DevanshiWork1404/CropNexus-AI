from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load dataset
df = pd.read_csv("Crop_recommendation.csv")

def get_crops(temp, top_n=5):
    df['temp_diff'] = abs(df['temperature'] - temp)
    suitable = df.nsmallest(top_n, 'temp_diff')
    return suitable['label'].tolist()

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    temp = data.get("temperature")
    top_n = data.get("top_n", 5)

    if temp is None:
        return jsonify({"error": "Temperature required"}), 400

    crops = get_crops(temp, top_n)
    return jsonify({"crops": crops})

if __name__ == "__main__":
    app.run(debug=True, port=5000)