from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import os

# Tell Flask where to find frontend files
app = Flask(
    __name__,
    template_folder="../frontend",   # for index.html
    static_folder="../frontend"      # for CSS/JS
)

# ---------------------------
# Route: Serve Frontend
# ---------------------------
@app.route('/')
def home():
    return render_template("index.html")

# ---------------------------
# Route: Register a new user
# ---------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username required"}), 400

    # Run register.py with username
    subprocess.run(["python", "register.py", username])
    return jsonify({"message": f"User {username} registered successfully!"})

# ---------------------------
# Route: Take attendance
# ---------------------------
@app.route('/attendance', methods=['GET'])
def attendance():
    subprocess.run(["python", "attendance.py"])
    return jsonify({"message": "Attendance taken successfully!"})

# ---------------------------
# Route: Get attendance report
# ---------------------------
@app.route('/report', methods=['GET'])
def report():
    if os.path.exists("attendance.csv"):
        return send_file("attendance.csv", mimetype="text/csv")
    else:
        return jsonify({"error": "No report found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
