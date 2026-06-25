# run.py
# ============================================
# APPLICATION ENTRY POINT
# Works for both local and production
# ============================================

import os
from flask_app.app import create_app

app = create_app()

if __name__ == '__main__':
    port  = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'

    print("\n🌿 Plant Disease Detection App")
    print(f"🚀 Starting on port {port}...")
    print(f"🌐 Open: http://localhost:{port}\n")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )