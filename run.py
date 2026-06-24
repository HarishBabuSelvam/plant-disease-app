# run.py
# Run this file to start the app!
# Usage: python run.py

from flask_app.app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n🌿 Plant Disease Detection App")
    print("🚀 Starting server...")
    print("🌐 Open: http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)