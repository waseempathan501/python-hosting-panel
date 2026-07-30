from flask import Flask, render_template_string, request, send_from_directory
import os
import subprocess
import sys
import threading

app = Flask(__name__)

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(UPLOAD_DIR, "hosted_python_scripts")

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# Dictionary to keep track of background running projects
running_processes = {}

@app.route('/image')
def profile_image():
    possible_names = ["1768110605494.jpg", "profile.jpg", "avatar.jpg"]
    for name in possible_names:
        if os.path.exists(os.path.join(UPLOAD_DIR, name)):
            return send_from_directory(UPLOAD_DIR, name)
    for file in os.listdir(UPLOAD_DIR):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            return send_from_directory(UPLOAD_DIR, file)
    return "Image not found", 404

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WASEEM PRO HACKER - Python Cloud Portal</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #05050a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .neon-box {
            position: relative;
            width: 100%;
            max-width: 420px;
            background: #0b0f19;
            border-radius: 25px;
            padding: 30px 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.9);
            overflow: hidden;
            z-index: 1;
        }
        .neon-box::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: conic-gradient(from 0deg, #ff0055, #00ffcc, #ff0055, #00ffcc, #ff0055);
            animation: rotateBorder 4s linear infinite;
            z-index: -2;
        }
        .neon-box::after {
            content: '';
            position: absolute;
            inset: 3px;
            background: #0b0f19;
            border-radius: 23px;
            z-index: -1;
        }
        @keyframes rotateBorder {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .content-container { position: relative; z-index: 2; width: 100%; text-align: center; }
        .creator-banner {
            background: linear-gradient(90deg, #ff0055, #7000ff, #00ffcc);
            background-size: 200% auto;
            color: white; font-size: 13px; font-weight: bold;
            padding: 8px; border-radius: 8px; margin-bottom: 15px;
            text-transform: uppercase; letter-spacing: 1px;
        }
        h1 { font-size: 22px; margin-bottom: 5px; color: #ffffff; }
        p.subtitle { font-size: 12px; color: #00ffcc; margin-bottom: 20px; font-weight: 600; }
        .status-box {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(0, 255, 204, 0.3);
            padding: 12px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; color: #cbd5e1;
        }
        .status-box span { color: #22c55e; font-weight: bold; }
        .link-group { display: flex; flex-direction: column; gap: 12px; width: 100%; margin-bottom: 20px; }
        .custom-btn {
            display: flex; align-items: center; justify-content: center; gap: 10px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(0, 255, 204, 0.4);
            padding: 12px 15px; border-radius: 12px;
            color: #f1f5f9; text-decoration: none; font-weight: 600; font-size: 14px;
        }
        .custom-btn:hover { background: #00ffcc; color: #05050a; }
        .host-btn { background: linear-gradient(135deg, #22c55e, #16a34a); border: none; color: white; }
    </style>
</head>
<body>
    <div class="neon-box">
        <div class="content-container">
            <div class="creator-banner">✨ WASEEM CLOUD HOSTING ✨</div>
            <h1>🔥 ╰‿╯𝕎𝔸𝕊𝔼𝔼𝕄 𝕂ℍ𝔸ℕ 👑 🔥</h1>
            <p class="subtitle">🔥 ⚡ ★24/7 CLOUD PYTHON PAAS★ 🔥</p>
            <div class="status-box">
                Status: <span>Active & Permanent Running</span>
            </div>
            <div class="link-group">
                <a href="/hosting" class="custom-btn host-btn">🐍 Open Cloud Hosting Panel</a>
                <a href="https://tiktok.com/@waseempathan902" target="_blank" class="custom-btn">🔥 Follow TikTok Account</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

HOSTING_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Waseem Cloud - Python Deployment Panel</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #05050a;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .neon-box {
            position: relative; width: 100%; max-width: 440px;
            background: #0b0f19; border-radius: 25px; padding: 35px 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.9);
        }
        h2 { color: #00ffcc; margin-bottom: 20px; font-size: 22px; text-align: center; }
        .form-group { margin-bottom: 18px; text-align: left; }
        label { display: block; font-size: 11px; color: #94a3b8; margin-bottom: 6px; font-weight: bold; }
        input[type="text"], input[type="file"] {
            width: 100%; background: #05050a; border: 1px solid #1e293b;
            padding: 12px; border-radius: 12px; color: white; font-size: 14px;
        }
        button {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: #05050a; border: none; width: 100%; padding: 14px;
            border-radius: 12px; font-weight: 900; font-size: 15px; cursor: pointer;
            margin-top: 10px; text-transform: uppercase;
        }
        .alert {
            background: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e;
            color: #4ade80; padding: 12px; border-radius: 12px; font-size: 13px;
            margin-top: 15px; word-break: break-all;
        }
        .alert a { color: #00ffcc; font-weight: bold; text-decoration: underline; }
        .back-link { display: inline-block; margin-top: 20px; color: #94a3b8; text-decoration: none; font-size: 13px; }
    </style>
</head>
<body>
    <div class="neon-box">
        <h2>⚡ 24/7 Python Cloud Deployer</h2>
        <form method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label>PROJECT NAME (SLUG)</label>
                <input type="text" name="project_name" placeholder="e.g. tradingbot" required>
            </div>
            <div class="form-group">
                <label>UPLOAD PYTHON (.PY) FILE</label>
                <input type="file" name="py_file" accept=".py" required>
            </div>
            <button type="submit">Deploy & Run 24/7</button>
        </form>

        {% if success_url %}
        <div class="alert">
            🚀 Project Live Successfully!<br>Live Endpoint: <a href="{{ success_url }}" target="_blank">{{ request.host_url[:-1] }}{{ success_url }}</a>
        </div>
        {% endif %}

        <a href="/" class="back-link">← Back to Home</a>
    </div>
</body>
</html>
"""

def background_runner(file_path):
    """Background thread mein script ko hamesha ke liye run rakhta hai"""
    try:
        subprocess.run([sys.executable, file_path])
    except Exception as e:
        print(f"Background execution error: {e}")

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/hosting', methods=['GET', 'POST'])
def hosting():
    success_url = None
    if request.method == 'POST':
        project_name = request.form.get('project_name').strip().lower()
        py_file = request.files.get('py_file')
        
        if project_name and py_file:
            project_path = os.path.join(PROJECTS_DIR, project_name)
            if not os.path.exists(project_path):
                os.makedirs(project_path)
            
            file_path = os.path.join(project_path, "main.py")
            py_file.save(file_path)
            
            # Agar pehle se koi process chal raha hai to usay avoid karein
            if project_name not in running_processes:
                t = threading.Thread(target=background_runner, args=(file_path,), daemon=True)
                t.start()
                running_processes[project_name] = t
            
            success_url = f"/live/{project_name}"

    return render_template_string(HOSTING_TEMPLATE, success_url=success_url)

@app.route('/live/<project_name>')
def live_project(project_name):
    project_path = os.path.join(PROJECTS_DIR, project_name, "main.py")
    if os.path.exists(project_path):
        return f"""
        <body style="background:#05050a; color:#00ffcc; font-family:sans-serif; text-align:center; padding-top:50px;">
            <h2>🚀 Project '{project_name}' is Live & Running 24/7!</h2>
            <p style="color:#22c55e;">Your background worker/bot script is active on the cloud server.</p>
            <br><a href="/hosting" style="color:white; background:#22c55e; padding:10px 20px; text-decoration:none; border-radius:8px;">Back to Panel</a>
        </body>
        """
    return "Project not found", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
