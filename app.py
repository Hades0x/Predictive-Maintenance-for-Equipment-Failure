from flask import Flask, request, jsonify
import joblib
import traceback
import logging


app = Flask(__name__)

# Set up logging to a file
logging.basicConfig(filename='flask_errors.log', level=logging.ERROR)
# Load the trained model
model = joblib.load('/Users/prateek/Desktop/mantanence/your_model.pkl')  # Replace 'your_model.pkl' with the actual model file

@app.route('/')
def home():
    return "Welcome to the Predictive Maintenance API!"
# Add a route for serving a favicon
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('/Users/prateek/Desktop/mantanence/favicon.ico')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        # Check if the required keys are present in the JSON data
        required_keys = ['Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
        for key in required_keys:
            if key not in data:
                return jsonify({"error": f"Missing key: {key}"}), 400

        features = [data['Air temperature [K]'], data['Process temperature [K]'], data['Rotational speed [rpm]'], data['Torque [Nm]'], data['Tool wear [min]']]
        print("Features:", features)
        app.logger.info("Features: %s", features)
        prediction = model.predict([features])[0]
        print("Prediction:", prediction)
        app.logger.info("Prediction: %s", prediction)

        return jsonify({"prediction": prediction})
    except Exception as e:
        app.logger.error("Error: %s", str(e))
        app.logger.error(traceback.format_exc())  # Log the traceback
        return jsonify({"error": "An error occurred during prediction"}), 500

#def predict():
    #data = request.get_json(force=True)
    #features = [data['Air temperature [K]'], data['Process temperature [K]'], data['Rotational speed [rpm]'], data['Torque [Nm]'], data['Tool wear [min]']]
    #prediction = model.predict([features])[0]
    #return jsonify(prediction)

if __name__ == '__main__':
    app.run(port=8765)


