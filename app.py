from flask import Flask, render_template_string, request, send_from_directory
import os
import subprocess
import sys

app = Flask(__name__)

UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(UPLOAD_DIR, "hosted_python_scripts")

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# Automatic image finder route
@app.route('/image')
def profile_image():
    possible_names = [
        "1768110605494.jpg",
        "profile.jpg",
        "avatar.jpg"
    ]
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
    <title>WASEEM PRO HACKER - Python Portal</title>
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
        .content-container {
            position: relative;
            z-index: 2;
            width: 100%;
            text-align: center;
        }
        .profile-img-container {
            width: 110px; height: 110px;
            margin: 0 auto 15px auto;
            border-radius: 50%;
            padding: 3px;
            background: conic-gradient(#ff0055, #00ffcc, #00ffcc, #ff0055);
            animation: rotateBorder 4s linear infinite;
        }
        .profile-img {
            width: 100%; height: 100%;
            border-radius: 50%;
            object-fit: cover;
            background: #111;
        }
        .creator-banner {
            background: linear-gradient(90deg, #ff0055, #7000ff, #00ffcc);
            background-size: 200% auto;
            color: white; font-size: 13px; font-weight: bold;
            padding: 8px; border-radius: 8px; margin-bottom: 15px;
            animation: textGlow 3s ease infinite; text-transform: uppercase; letter-spacing: 1px;
        }
        @keyframes textGlow {
            0% { background-position: 0% center; }
            50% { background-position: 100% center; }
            100% { background-position: 0% center; }
        }
        h1 { font-size: 22px; margin-bottom: 5px; color: #ffffff; letter-spacing: 1px; }
        p.subtitle { font-size: 12px; color: #00ffcc; margin-bottom: 20px; font-weight: 600; }
        
        .status-box {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(0, 255, 204, 0.3);
            padding: 12px; border-radius: 12px; margin-bottom: 20px; font-size: 13px; color: #cbd5e1;
        }
        .status-box span { color: #22c55e; font-weight: bold; }

        .link-group {
            display: flex; flex-direction: column; gap: 12px; width: 100%; margin-bottom: 20px;
        }
        .custom-btn {
            display: flex; align-items: center; justify-content: center; gap: 10px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(0, 255, 204, 0.4);
            padding: 12px 15px; border-radius: 12px;
            color: #f1f5f9; text-decoration: none; font-weight: 600; font-size: 14px;
            transition: all 0.3s ease;
        }
        .custom-btn:hover {
            background: #00ffcc; color: #05050a; border-color: #00ffcc;
            transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 255, 204, 0.4);
        }
        .host-btn {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            border: none; color: white;
        }
        .host-btn:hover { background: #16a34a; color: white; box-shadow: 0 5px 15px rgba(34, 197, 94, 0.5); }

        .footer-note { font-size: 11px; color: #94a3b8; line-height: 1.4; margin-bottom: 15px; }
        
        .hacker-banner {
            background: linear-gradient(90deg, #00ffcc, #22c55e, #00ffcc);
            background-size: 200% auto;
            color: #05050a; font-size: 12px; font-weight: 900;
            padding: 10px; border-radius: 8px; text-transform: uppercase;
            animation: textGlow 3s ease infinite; letter-spacing: 1px;
        }
    </style>
</head>
<body>
    <div class="neon-box">
        <div class="content-container">
            <div class="creator-banner">✨ WASEEM PRO HACKER ✨</div>
            
            <div class="profile-img-container">
            </div>

            <h1>🔥 ╰‿╯𝕎𝔸𝕊𝔼𝔼𝕄 𝕂ℍ𝔸ℕ 👑 🔥</h1>
            <p class="subtitle">🔥 ⚡ ★𝘃𝗲𝗿𝗶𝗳𝗶𝗲𝗱 𝗰𝗿𝗲𝗮𝘁𝗼𝗿 & 𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿★ 🔥</p>

            <div class="status-box">
                🔥 ⚡ ★𝘀𝘁𝗮𝘁𝘂𝘀: 𝗽𝘆𝘁𝗵𝗼𝗻 𝗲𝗻𝗴𝗶𝗻𝗲 𝗮𝗰𝘁𝗶𝘃𝗲★ 🔥<br>
                       🔥 ⚡ ★𝘀𝗲𝗰𝘂𝗿𝗶𝘁𝘆:★ 🔥 <span>🔥 ⚡ ★𝗮𝗰𝘁𝗶𝘃𝗲 & 𝗲𝗻𝗰𝗿𝘆𝗽𝘁𝗲𝗱★ 🔥</span>
            </div>

            <div class="link-group">
                <a href="/hosting" class="custom-btn host-btn">
                    🐍 Proceed to Python Panel
                </a>
                <a href="https://tiktok.com/@waseempathan902" target="_blank" class="custom-btn">
                    🔥 ⚡𝙁𝙊𝙇𝙇𝙊𝙒 𝙈𝙔 𝙏𝙄𝙆𝙏𝙊𝙆 𝘼𝘾𝘾𝙊𝙐𝙉𝙏⚡
                </a>
                <a href="https://wa.me/923142413307" target="_blank" class="custom-btn">
                    💬 🔥 03142413307  🔥 (1)
                </a>
                <a href="https://wa.me/923293170988" target="_blank" class="custom-btn">
                    💬 🔥 03293170988  🔥 (2)
                </a>
            </div>

            <div class="footer-note">         🔥 ⚡ ★𝗰𝗿𝗮𝗳𝘁𝗲𝗱 𝘄𝗶𝘁𝗵 𝗽𝗿𝗲𝗰𝗶𝘀𝗶𝗼𝗻 𝗯𝘆 𝘄𝗮𝘀𝗲𝗲𝗺 — 𝗯𝘂𝗶𝗹𝘁 𝗳𝗼𝗿 𝗵𝗶𝗴𝗵-𝗲𝗻𝗱 𝘀𝗲𝗰𝘂𝗿𝗶𝘁𝘆 𝘁𝗲𝘀𝘁𝗶𝗻𝗴, 𝗰𝘂𝘀𝘁𝗼𝗺 𝗵𝗼𝘀𝘁𝗶𝗻𝗴, 𝗮𝗻𝗱 𝗻𝗲𝘅𝘁- 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝗼𝗻.★ 🔥
            </div>

            <div class="hacker-banner">
                DEVELOPED BY WASEEM HACKER | CODE ARCHITECT & CYBERSECURITY ENTHUSIAST
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
    <title>Waseem Python Hosting Panel</title>
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
            max-width: 440px;
            background: #0b0f19;
            border-radius: 25px;
            padding: 35px 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.9);
            overflow: hidden;
            z-index: 1;
        }
        .neon-box::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: conic-gradient(from 0deg, #22c55e, #00ffcc, #22c55e, #00ffcc, #22c55e);
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
        .content-container {
            position: relative;
            z-index: 2;
            width: 100%;
            text-align: center;
        }
        .creator-banner {
            background: linear-gradient(90deg, #22c55e, #00ffcc, #22c55e);
            background-size: 200% auto;
            color: #05050a; font-size: 13px; font-weight: 900;
            padding: 8px; border-radius: 8px; margin-bottom: 20px;
            animation: textGlow 3s ease infinite; text-transform: uppercase; letter-spacing: 1px;
        }
        @keyframes textGlow {
            0% { background-position: 0% center; }
            50% { background-position: 100% center; }
            100% { background-position: 0% center; }
        }
        h2 { color: #00ffcc; margin-bottom: 20px; font-size: 22px; font-weight: bold; }
        
        .form-group { margin-bottom: 18px; text-align: left; }
        label { display: block; font-size: 11px; color: #94a3b8; margin-bottom: 6px; font-weight: bold; letter-spacing: 0.5px; }
        input[type="text"] {
            width: 100%; background: #05050a; border: 1px solid #1e293b;
            padding: 12px; border-radius: 12px; color: white; box-sizing: border-box; outline: none; font-size: 14px;
        }
        input[type="text"]:focus { border-color: #00ffcc; }

        input[type="file"] {
            width: 100%;
            background: #05050a;
            border: 1px dashed #22c55e;
            padding: 10px;
            border-radius: 12px;
            color: #22c55e;
            font-size: 13px;
            cursor: pointer;
        }
        input[type="file"]::file-selector-button {
            background: #22c55e;
            color: #05050a;
            border: none;
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            margin-right: 10px;
            transition: 0.2s;
        }
        input[type="file"]::file-selector-button:hover {
            background: #00ffcc;
        }

        button {
            background: linear-gradient(135deg, #22c55e, #16a34a);
            color: #05050a; border: none; width: 100%; padding: 14px;
            border-radius: 12px; font-weight: 900; font-size: 15px; cursor: pointer;
            margin-top: 10px; transition: 0.2s; text-transform: uppercase; letter-spacing: 0.5px;
        }
        button:hover { opacity: 0.9; box-shadow: 0 5px 15px rgba(34, 197, 94, 0.4); }

        .alert {
            background: rgba(34, 197, 94, 0.1); border: 1px solid #22c55e;
            color: #4ade80; padding: 12px; border-radius: 12px; font-size: 13px;
            margin-top: 15px; word-break: break-all; text-align: left;
        }
        .alert a { color: #00ffcc; font-weight: bold; text-decoration: underline; }

        .back-link {
            display: inline-block; margin-top: 20px; color: #94a3b8;
            text-decoration: none; font-size: 13px; font-weight: 600; transition: 0.2s;
        }
        .back-link:hover { color: #00ffcc; }

        .footer-extra {
            margin-top: 20px; font-size: 11px; color: #64748b; border-top: 1px solid #1e293b; padding-top: 15px;
        }
        .hacker-banner {
            background: linear-gradient(90deg, #00ffcc, #22c55e, #00ffcc);
            background-size: 200% auto;
            color: #05050a; font-size: 12px; font-weight: 900;
            padding: 10px; border-radius: 8px; text-transform: uppercase;
            animation: textGlow 3s ease infinite; letter-spacing: 1px; margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="neon-box">
        <div class="content-container">
            <div class="creator-banner">⚡ PYTHON EXECUTION ENGINE ⚡</div>
            <h2>Python Hosting Panel</h2>
            
            <form method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label>PROJECT NAME (SLUG)</label>
                    <input type="text" name="project_name" placeholder="e.g. myscript" required>
                </div>
                <div class="form-group">
                    <label>UPLOAD PYTHON (.PY) FILE</label>
                    <input type="file" name="py_file" accept=".py" required>
                </div>
                <button type="submit">Run & Execute Script</button>
            </form>

            {% if success_url %}
            <div class="alert">
                🚀 Python Script Executed!<br>View Output/Logs: <a href="{{ success_url }}" target="_blank">{{ request.host_url[:-1] }}{{ success_url }}</a>
            </div>
            {% endif %}

            <div class="footer-extra">
                Advanced Python cloud runner powered by custom server background processes. Fast, secure, and automated.
            </div>

            <div class="hacker-banner">
                DEVELOPED BY WASEEM HACKER | CYBERSECURITY ARCHITECT
            </div>

            <a href="/" class="back-link">← Back to Home Profile</a>
        </div>
    </div>
</body>
</html>
"""

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
            
            # Execute the python script using subprocess and capture output
            try:
                result = subprocess.run([sys.executable, file_path], capture_output=True, text=True, timeout=10)
                
                stdout_data = result.stdout.strip()
                stderr_data = result.stderr.strip()
                
                # Permanent Solution: Agar script ka output khali hai, toh default success message dikhao
                if not stdout_data and not stderr_data:
                    output_content = "SUCCESS: Script successfully execute ho gayi hai! (No terminal output generated by script.)"
                else:
                    output_content = f"STDOUT:\n{stdout_data}\n\nSTDERR:\n{stderr_data}"
                    
            except subprocess.TimeoutExpired:
                output_content = "Execution timed out (Script took longer than 10 seconds)."
            except Exception as e:
                output_content = f"Execution Error: {str(e)}"
            
            # Save the execution log/output to a file
            log_path = os.path.join(project_path, "output.txt")
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            success_url = f"/view_output/{project_name}"

    return render_template_string(HOSTING_TEMPLATE, success_url=success_url)

@app.route('/view_output/<project_name>')
def view_output(project_name):
    log_path = os.path.join(PROJECTS_DIR, project_name, "output.txt")
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pretty terminal-style view for python outputs
        terminal_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Execution Output - {project_name}</title>
            <style>
                body {{ background: #05050a; color: #00ffcc; font-family: monospace; padding: 20px; }}
                h2 {{ color: #22c55e; border-bottom: 1px solid #1e293b; padding-bottom: 10px; }}
                pre {{ background: #0b0f19; padding: 20px; border-radius: 12px; border: 1px solid rgba(0,255,204,0.3); white-space: pre-wrap; word-break: break-all; }}
                a {{ display: inline-block; margin-top: 20px; color: #22c55e; text-decoration: none; font-weight: bold; }}
                a:hover {{ color: #00ffcc; }}
            </style>
        </head>
        <body>
            <h2>⚡ Python Execution Logs: {project_name}</h2>
            <pre>{content}</pre>
            <a href="/hosting">← Back to Hosting Panel</a>
        </body>
        </html>
        """
        return terminal_html
    return "<h3 style='font-family:sans-serif; text-align:center; margin-top:50px; color:#ff5722;'>404 - Output Not Found!</h3>", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
