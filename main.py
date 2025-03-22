from flask import Flask, request, jsonify
import os
import csv
import io

app = Flask(__name__)

# Set environment variables for configuration
STORAGE_PATH = os.environ.get('STORAGE_PATH', '/saikat_PV_dir')

@app.route('/calculate-sum', methods=['POST'])
def calculate_sum():
    try:
        # Parse JSON input
        data = request.get_json()
        
        # Validate JSON input
        if 'file' not in data or not data['file']:
            return jsonify({
                "file": None,
                "error": "Invalid JSON input."
            }), 400
            
        if 'product' not in data:
            return jsonify({
                "file": data['file'],
                "error": "Invalid JSON input."
            }), 400
        
        product_name = data['product']
        
        # Check if file exists
        filepath = os.path.join(STORAGE_PATH, data['file'])
        if not os.path.exists(filepath):
            return jsonify({
                "file": data['file'],
                "error": "File not found."
            }), 404
        
        # Read and parse file
        try:
            with open(filepath, 'r') as f:
                # Parse CSV
                try:
                    csv_reader = csv.reader(f)
                    headers = next(csv_reader)
                    
                    # Strip whitespace from headers
                    headers = [h.strip() for h in headers]
                    
                    # Check if CSV has required columns
                    if len(headers) < 2 or 'product' not in headers and 'amount' not in headers:
                        return jsonify({
                            "file": data['file'],
                            "error": "Input file not in CSV format."
                        }), 400
                    
                    # Find column indexes
                    product_idx = headers.index('product')
                    amount_idx = headers.index('amount')
                    
                    # Calculate sum for the specified product
                    total = 0
                    for row in csv_reader:
                        if len(row) > max(product_idx, amount_idx):
                            row_product = row[product_idx].strip()
                            if row_product == product_name:
                                try:
                                    amount = int(row[amount_idx].strip())
                                    total += amount
                                except ValueError:
                                    print(f"Invalid amount value: {row[amount_idx]}")
                    
                    return jsonify({
                        "file": data['file'],
                        "sum": total
                    })
                    
                except Exception as e:
                    print(f"CSV parsing error: {e}")
                    return jsonify({
                        "file": data['file'],
                        "error": "Input file not in CSV format."
                    }), 400
                
        except Exception as e:
            print(f"Error reading file: {e}")
            return jsonify({
                "file": data['file'],
                "error": "Error reading file."
            }), 500
            
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({
            "file": None,
            "error": "Invalid JSON input."
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
#This is a comment
