import subprocess
import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the Terraform binary (in the same folder)
TERRAFORM_PATH = os.path.join(os.getcwd(), "terraform")
# Use the current working directory as the Terraform directory
TERRAFORM_DIR = os.getcwd()

@app.route("/espwd", methods=["GET"])
def generate_password():
    try:
        # Get the password length from the query parameter (default to 18 if not provided)
        length = request.args.get("length", default=18, type=int)

        # Run Terraform commands in the specified directory
        subprocess.run([TERRAFORM_PATH, "init"], check=True, cwd=TERRAFORM_DIR)
        subprocess.run([TERRAFORM_PATH, "apply", "-auto-approve", f"-var=length={length}"], check=True, cwd=TERRAFORM_DIR)

        # Retrieve the generated password from Terraform output
        result = subprocess.run(
            [TERRAFORM_PATH, "output", "-json"],  # Use -json to get the full output as JSON
            capture_output=True,
            text=True,
            check=True,
            cwd=TERRAFORM_DIR
        )

        # Debug: Print the raw Terraform output
        print("Terraform Output (Raw):", result.stdout)

        # Parse the JSON output
        output_json = json.loads(result.stdout)

        # Debug: Print the parsed JSON
        print("Terraform Output (Parsed):", output_json)

        # Extract the password value
        password = output_json["espassword"]["value"]

        # Return the password as a JSON response
        return jsonify({"password": password}), 200

    except subprocess.CalledProcessError as e:
        # Handle errors during Terraform execution
        print("Terraform Error:", e.stderr)
        return jsonify({"error": "Terraform command failed", "details": e.stderr}), 500
    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print("JSON Decode Error:", e)
        return jsonify({"error": "Failed to parse Terraform output", "details": str(e)}), 500
    except KeyError as e:
        # Handle missing keys in the JSON output
        print("Key Error:", e)
        return jsonify({"error": "Invalid Terraform output format", "details": str(e)}), 500
    except Exception as e:
        # Handle any other exceptions
        print("Unexpected Error:", e)
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=200)  
