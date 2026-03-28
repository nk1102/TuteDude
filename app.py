from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates')

# MongoDB setup - with error handling
MONGO_URI = os.getenv("MONGO_URI")
print(f"MONGO_URI loaded: {MONGO_URI[:30]}..." if MONGO_URI else "MONGO_URI not found!")

if not MONGO_URI:
    print("ERROR: MONGO_URI not set in .env file!")
    collection = None
else:
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        # Test the connection
        client.admin.command('ping')
        db = client["crem_db"]
        collection = db["users"]
        print("✓ MongoDB connected successfully")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        collection = None


@app.route('/test')
def test():
    return "Flask is working!"


@app.route('/api')
def get_data():
    with open('data.json') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/', methods=['GET', 'POST'])
def form():
    error = None

    if request.method == 'POST':
        try:
            if collection is None:
                error = "Database connection failed"
            else:
                name = request.form.get('name')
                email = request.form.get('email')
                age = request.form.get('age')

                collection.insert_one({
                    "name": name,
                    "email": email,
                    "age": int(age)
                })

                return redirect(url_for('success'))

        except Exception as e:
            error = str(e)

    return render_template('form.html', error=error)


@app.route('/success')
def success():
    return render_template('succes.html')


if __name__ == '__main__':
    app.run(debug=True)