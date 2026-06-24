# flask_app/database/db.py
# ============================================
# DATABASE SETUP & OPERATIONS
# ============================================
# We use SQLite — a simple file-based database
# Perfect for beginners — no server needed!
# The entire database is ONE file: predictions.db
# ============================================

import sqlite3
import os
from datetime import datetime

# Database file location
DB_PATH = "flask_app/database/predictions.db"


def get_connection():
    """
    Create and return a database connection.
    
    Why a function? So every part of our app
    can easily get a database connection without
    repeating code.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dictionaries instead of tuples
    # This lets us access data like: row['disease_name']
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """
    Create database tables if they don't exist.
    Called once when Flask app starts.
    
    Our predictions table stores:
    - Every image upload and its prediction result
    - Used for the History page
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Create predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            filename        TEXT NOT NULL,
            original_name   TEXT,
            plant_name      TEXT NOT NULL,
            disease_name    TEXT NOT NULL,
            class_name      TEXT NOT NULL,
            confidence      REAL NOT NULL,
            is_healthy      INTEGER NOT NULL,
            severity        TEXT,
            spread_risk     TEXT,
            recovery_chance INTEGER,
            treatment_time  TEXT,
            created_at      TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")


def save_prediction(data):
    """
    Save a prediction result to the database.
    
    Args:
        data (dict): Prediction data to save
        
    Returns:
        int: ID of the saved record
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO predictions (
            filename, original_name, plant_name,
            disease_name, class_name, confidence,
            is_healthy, severity, spread_risk,
            recovery_chance, treatment_time, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('filename'),
        data.get('original_name'),
        data.get('plant_name'),
        data.get('disease_name'),
        data.get('class_name'),
        data.get('confidence'),
        1 if data.get('is_healthy') else 0,
        data.get('severity'),
        data.get('spread_risk'),
        data.get('recovery_chance'),
        data.get('treatment_time'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

    prediction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return prediction_id


def get_all_predictions(limit=50):
    """
    Get all predictions for the history page.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        list of prediction records
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM predictions
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    # Convert Row objects to regular dictionaries
    return [dict(row) for row in rows]


def get_prediction_by_id(prediction_id):
    """Get a single prediction by its ID"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM predictions WHERE id = ?',
        (prediction_id,)
    )

    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_statistics():
    """
    Get statistics for the dashboard.
    
    Returns counts of total, healthy, diseased predictions
    and most common diseases.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Total predictions
    cursor.execute('SELECT COUNT(*) as count FROM predictions')
    total = cursor.fetchone()['count']

    # Healthy vs diseased
    cursor.execute('''
        SELECT
            SUM(CASE WHEN is_healthy = 1 THEN 1 ELSE 0 END) as healthy,
            SUM(CASE WHEN is_healthy = 0 THEN 1 ELSE 0 END) as diseased
        FROM predictions
    ''')
    health_stats = dict(cursor.fetchone())

    # Most common diseases (top 5)
    cursor.execute('''
        SELECT disease_name, COUNT(*) as count
        FROM predictions
        WHERE is_healthy = 0
        GROUP BY disease_name
        ORDER BY count DESC
        LIMIT 5
    ''')
    top_diseases = [dict(row) for row in cursor.fetchall()]

    # Recent predictions (last 7 days)
    cursor.execute('''
        SELECT COUNT(*) as count FROM predictions
        WHERE created_at >= datetime('now', '-7 days')
    ''')
    recent = cursor.fetchone()['count']

    conn.close()

    return {
        'total':        total,
        'healthy':      health_stats.get('healthy') or 0,
        'diseased':     health_stats.get('diseased') or 0,
        'top_diseases': top_diseases,
        'recent':       recent
    }


def delete_prediction(prediction_id):
    """Delete a prediction record"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM predictions WHERE id = ?',
        (prediction_id,)
    )
    conn.commit()
    conn.close()