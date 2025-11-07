from flask import Flask, render_template, jsonify
from flask_cors import CORS
import json
import os
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

def load_baseline():
    """Load baseline data"""
    baseline_path = Path("../baseline.json")
    if baseline_path.exists():
        with open(baseline_path) as f:
            return json.load(f)
    return {}

def load_integrity_report():
    """Load latest integrity report"""
    report_path = Path("../integrity_report.json")
    if report_path.exists():
        with open(report_path) as f:
            return json.load(f)
    return {"MODIFIED": [], "CREATED": [], "DELETED": []}

def get_system_stats():
    """Get system statistics"""
    baseline = load_baseline()
    report = load_integrity_report()
    
    total_files = len(baseline)
    modified = len(report.get('MODIFIED', []))
    created = len(report.get('CREATED', []))
    deleted = len(report.get('DELETED', []))
    total_changes = modified + created + deleted
    
    status = "SECURE" if total_changes == 0 else "BREACH"
    
    return {
        'total_files': total_files,
        'modified': modified,
        'created': created,
        'deleted': deleted,
        'total_changes': total_changes,
        'status': status,
        'last_scan': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    return jsonify(get_system_stats())

@app.route('/api/integrity')
def api_integrity():
    return jsonify(load_integrity_report())

@app.route('/api/baseline')
def api_baseline():
    baseline = load_baseline()
    # Return first 100 entries for performance
    limited = dict(list(baseline.items())[:100])
    return jsonify(limited)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
