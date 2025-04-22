import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup
from flask_cors import CORS
import time  # Import the time module for timing

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/get-tide-data', methods=['GET'])
def get_tide_data():
    try:
        start_time = time.time()  # Start timing the request
        
        url = 'https://www.tide-forecast.com/locations/Saibai-Island-Torres-Strait/tides/latest'  # Replace with the actual URL for tide data
        
        # Set timeout to avoid hanging requests
        response = requests.get(url, timeout=10)  # 10-second timeout
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')

        tide_data = []  # Create a list to hold tide data

        # Iterate through all the <tr> rows, starting from index 26
        for tide_row in soup.find_all('tr')[26:100]:  # Check all <tr> tags
            row_data = tide_row.text.strip()  # Get the full text of the row
            
            # Filter out rows that do not contain tide data
            if "AM" in row_data or "PM" in row_data:  # Assuming times are in AM/PM format
                if "m" in row_data or "ft" in row_data:  # Looking for data that includes height
                    tide_data.append(row_data)  # Add valid tide row data to the list

        end_time = time.time()  # End timing the request
        duration = end_time - start_time
        print(f"Request completed in {duration} seconds.")
        
        # Return the tide data in the response
        return jsonify({'tide_data': tide_data}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f"Failed to fetch tide data: {str(e)}"}), 500

    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
