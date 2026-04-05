# ==========================================
# VELIONX BLOOD STRIKE PANEL
# Dark Modern Professional Edition
# Coded By VELIONX
# ==========================================

from flask import Flask, request, jsonify, render_template_string, session
import os, time, hashlib, subprocess, threading, uuid, json, zipfile

app = Flask(__name__)
app.secret_key = "VELIONX_SUPER_SECRET_KEY_2026"

# Konfigurasi Path
USERS_FILE = os.path.expanduser("~/velionx_users.json")
HWID_FILE = os.path.expanduser("~/.velionx_hwid")
MODS_DIR = os.path.expanduser("~/velionx_mods")
BLOOD_STRIKE_PATH = "/storage/emulated/0/Android/data/com.netease.newspike/files"

# Buat folder
os.makedirs(MODS_DIR, exist_ok=True)

# ==========================================
# FUNGSI HWID & USER
# ==========================================
def get_hwid():
    if os.path.exists(HWID_FILE):
        with open(HWID_FILE, 'r') as f:
            return f.read().strip()
    else:
        new_hwid = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()
        with open(HWID_FILE, 'w') as f:
            f.write(new_hwid)
        return new_hwid

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# ==========================================
# EKSEKUSI COMMAND (Anti-Freeze)
# ==========================================
def run_commands(cmd_list):
    full_output = ""
    for cmd in cmd_list:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if result.stdout:
                full_output += result.stdout + "\n"
            if result.stderr:
                full_output += result.stderr + "\n"
        except subprocess.TimeoutExpired:
            full_output += f"\n[!] TIMEOUT 5 DETIK: '{cmd}' nyangkut!\n"
        except Exception as e:
            full_output += f"Error: {str(e)}\n"
    return full_output.strip()

# ==========================================
# HTML PAGE (Dark Modern Theme)
# ==========================================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>VELIONX • Blood Strike Panel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            padding: 20px;
            position: relative;
        }

        /* Grid background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(79, 70, 229, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(79, 70, 229, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        /* Card Modern */
        .card {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            border: 1px solid rgba(79, 70, 229, 0.3);
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        .card:hover {
            border-color: rgba(79, 70, 229, 0.6);
            box-shadow: 0 0 30px rgba(79, 70, 229, 0.2);
        }

        /* Header */
        .header {
            text-align: center;
            margin-bottom: 24px;
        }

        .logo {
            font-size: 48px;
            background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        h1 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-top: 8px;
        }

        .subtitle {
            color: #94A3B8;
            font-size: 12px;
            margin-top: 4px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }

        .stat-card {
            background: rgba(30, 41, 59, 0.6);
            border-radius: 20px;
            padding: 12px;
            text-align: center;
            border: 1px solid rgba(79, 70, 229, 0.2);
        }

        .stat-icon {
            font-size: 24px;
            margin-bottom: 4px;
        }

        .stat-value {
            font-size: 20px;
            font-weight: 700;
            color: #F1F5F9;
        }

        .stat-label {
            font-size: 10px;
            color: #94A3B8;
            margin-top: 4px;
        }

        /* Buttons */
        .btn {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 16px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-bottom: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4);
        }

        .btn-danger {
            background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
            color: white;
        }

        .btn-warning {
            background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%);
            color: white;
        }

        .btn-secondary {
            background: rgba(51, 65, 85, 0.8);
            color: #E2E8F0;
            border: 1px solid rgba(79, 70, 229, 0.3);
        }

        .btn-secondary:hover {
            background: rgba(79, 70, 229, 0.3);
        }

        .btn:active {
            transform: scale(0.98);
        }

        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        /* Grid 2 kolom */
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .span-2 {
            grid-column: span 2;
        }

        /* Input */
        .input-group {
            margin-bottom: 16px;
        }

        input, select {
            width: 100%;
            padding: 14px;
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid rgba(79, 70, 229, 0.3);
            border-radius: 16px;
            color: #F1F5F9;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            outline: none;
            transition: all 0.2s;
        }

        input:focus, select:focus {
            border-color: #818CF8;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        }

        /* Terminal */
        .terminal {
            background: #0A0F1A;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(79, 70, 229, 0.3);
            margin-top: 20px;
        }

        .terminal-header {
            background: #1E293B;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid rgba(79, 70, 229, 0.3);
        }

        .terminal-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .terminal-dot.red { background: #EF4444; }
        .terminal-dot.yellow { background: #F59E0B; }
        .terminal-dot.green { background: #10B981; }

        .terminal-title {
            color: #64748B;
            font-size: 11px;
            margin-left: 8px;
            font-family: 'JetBrains Mono', monospace;
        }

        .terminal-content {
            height: 150px;
            overflow-y: auto;
            padding: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #A5B4FC;
            line-height: 1.6;
        }

        .terminal-content::-webkit-scrollbar {
            width: 4px;
        }

        .terminal-content::-webkit-scrollbar-track {
            background: #1E293B;
        }

        .terminal-content::-webkit-scrollbar-thumb {
            background: #4F46E5;
            border-radius: 10px;
        }

        /* Hide/Show */
        .view {
            display: none;
        }

        .view.active {
            display: block;
        }

        /* Badge */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(79, 70, 229, 0.2);
            border: 1px solid rgba(79, 70, 229, 0.5);
            border-radius: 20px;
            font-size: 10px;
            color: #A78BFA;
            margin-bottom: 16px;
        }

        /* Upload area */
        .upload-area {
            border: 2px dashed rgba(79, 70, 229, 0.4);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 16px;
        }

        .upload-area:hover {
            border-color: #818CF8;
            background: rgba(79, 70, 229, 0.05);
        }

        .upload-area i {
            font-size: 48px;
            color: #818CF8;
            margin-bottom: 12px;
        }

        /* Animations */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        /* Toast */
        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #1E293B;
            border: 1px solid #4F46E5;
            border-radius: 40px;
            padding: 12px 24px;
            font-size: 13px;
            font-weight: 500;
            z-index: 1000;
            animation: slideUp 0.3s ease;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
    </style>
</head>
<body>

<div class="container" id="app">
    <!-- LOGIN VIEW -->
    <div id="view-login" class="view active">
        <div class="card">
            <div class="header">
                <div class="logo">⚡</div>
                <h1>VELIONX</h1>
                <div class="subtitle">Blood Strike Optimizer</div>
            </div>
            <div class="badge" style="display: block; text-align: center;">🔐 HWID SECURE</div>
            <div class="input-group">
                <input type="text" id="username" placeholder="Username" autocomplete="off">
            </div>
            <div class="input-group">
                <input type="password" id="password" placeholder="Password">
            </div>
            <button class="btn btn-primary" onclick="login()">
                <i class="fas fa-arrow-right-to-bracket"></i> LOGIN
            </button>
            <p id="loginMsg" style="margin-top: 16px; font-size: 12px; text-align: center; color: #EF4444;"></p>
        </div>
    </div>

    <!-- MAIN MENU VIEW -->
    <div id="view-main" class="view">
        <div class="card">
            <div class="header">
                <div class="logo">🎮</div>
                <h1>VELIONX</h1>
                <div class="subtitle">Blood Strike • Pro Optimizer</div>
            </div>

            <!-- Stats -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">📱</div>
                    <div class="stat-value" id="stat-device">---</div>
                    <div class="stat-label">Device</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🔋</div>
                    <div class="stat-value" id="stat-battery">--%</div>
                    <div class="stat-label">Battery</div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon">🌡️</div>
                    <div class="stat-value" id="stat-temp">--°C</div>
                    <div class="stat-label">Temp</div>
                </div>
            </div>

            <!-- Main Menu -->
            <button class="btn btn-primary" onclick="switchView('view-adb')">
                <i class="fas fa-mobile-alt"></i> NON-ROOT MODE (ADB)
            </button>
            <button class="btn btn-danger" onclick="switchView('view-root')">
                <i class="fas fa-skull"></i> ROOT MODE (ULTRA)
            </button>
            <button class="btn btn-secondary" onclick="switchView('view-inject')">
                <i class="fas fa-file-archive"></i> 📦 INJECT MOD ZIP
            </button>

            <!-- Terminal -->
            <div class="terminal">
                <div class="terminal-header">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                    <span class="terminal-title">VELIONX_CONSOLE</span>
                </div>
                <div class="terminal-content" id="terminal-main">
                    <span style="color:#64748B;">[sys] System ready...</span><br>
                    <span style="color:#A78BFA;">[+] Welcome to VELIONX Panel</span><br>
                </div>
            </div>
        </div>
    </div>

    <!-- ADB MODE VIEW -->
    <div id="view-adb" class="view">
        <div class="card">
            <h1 style="font-size: 20px; text-align: center;">🎮 NON-ROOT MODE</h1>
            <div class="subtitle" style="text-align: center;">ADB Tweaks for Blood Strike</div>
            
            <div class="grid-2" style="margin-top: 20px;">
                <button class="btn btn-primary" onclick="execCmd('nr', '1', 'terminal-adb', this)">1. Aim Head Max</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '2', 'terminal-adb', this)">2. Ultra Respon</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '3', 'terminal-adb', this)">3. Fix Touch</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '4', 'terminal-adb', this)">4. Perf Mode</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '5', 'terminal-adb', this)">5. Net Stabil</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '6', 'terminal-adb', this)">6. Touch Smp</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '7', 'terminal-adb', this)">7. Batt Throt</button>
                <button class="btn btn-primary" onclick="execCmd('nr', '8', 'terminal-adb', this)">8. Game Turbo</button>
                <button class="btn btn-primary span-2" onclick="execCmd('nr', '9', 'terminal-adb', this)">⚡ APPLY ALL TWEAKS</button>
                <button class="btn btn-warning span-2" onclick="execCmd('reset', 'adb', 'terminal-adb', this)">⟲ RESTORE ADB</button>
            </div>

            <button class="btn btn-secondary" onclick="switchView('view-main')" style="margin-top: 16px;">
                <i class="fas fa-arrow-left"></i> Back to Menu
            </button>

            <div class="terminal" style="margin-top: 16px;">
                <div class="terminal-header">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                    <span class="terminal-title">ADB_CONSOLE</span>
                </div>
                <div class="terminal-content" id="terminal-adb"></div>
            </div>
        </div>
    </div>

    <!-- ROOT MODE VIEW -->
    <div id="view-root" class="view">
        <div class="card">
            <h1 style="font-size: 20px; text-align: center;">☠ ROOT ULTRA MODE</h1>
            <div class="subtitle" style="text-align: center;">Root Access Required</div>
            
            <div class="grid-2" style="margin-top: 20px;">
                <button class="btn btn-danger" onclick="execCmd('r', '1', 'terminal-root', this)">1. Aim Max</button>
                <button class="btn btn-danger" onclick="execCmd('r', '2', 'terminal-root', this)">2. CPU OC</button>
                <button class="btn btn-danger" onclick="execCmd('r', '3', 'terminal-root', this)">3. GPU Boost</button>
                <button class="btn btn-danger" onclick="execCmd('r', '4', 'terminal-root', this)">4. Zero Therm</button>
                <button class="btn btn-danger" onclick="execCmd('r', '5', 'terminal-root', this)">5. Kill Bkg</button>
                <button class="btn btn-danger" onclick="execCmd('r', '6', 'terminal-root', this)">6. RAM Mgt</button>
                <button class="btn btn-danger" onclick="execCmd('r', '7', 'terminal-root', this)">7. I/O Sched</button>
                <button class="btn btn-danger" onclick="execCmd('r', '8', 'terminal-root', this)">8. Storage UP</button>
                <button class="btn btn-danger span-2" onclick="execCmd('r', '9', 'terminal-root', this)">9. Ultra Net BBR</button>
                <button class="btn btn-danger span-2" onclick="execCmd('r', '10', 'terminal-root', this)">☠ APPLY EXTREME ROOT</button>
                <button class="btn btn-warning span-2" onclick="execCmd('reset', 'root', 'terminal-root', this)">⟲ RESTORE ROOT</button>
            </div>

            <button class="btn btn-secondary" onclick="switchView('view-main')" style="margin-top: 16px;">
                <i class="fas fa-arrow-left"></i> Back to Menu
            </button>

            <div class="terminal" style="margin-top: 16px;">
                <div class="terminal-header">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                    <span class="terminal-title">ROOT_CONSOLE</span>
                </div>
                <div class="terminal-content" id="terminal-root"></div>
            </div>
        </div>
    </div>

    <!-- INJECT MOD VIEW -->
    <div id="view-inject" class="view">
        <div class="card">
            <h1 style="font-size: 20px; text-align: center;">📦 MOD INJECTOR</h1>
            <div class="subtitle" style="text-align: center;">Upload ZIP to Blood Strike</div>
            
            <div class="upload-area" onclick="document.getElementById('zipFile').click()">
                <i class="fas fa-cloud-upload-alt"></i>
                <p>Click to select ZIP file</p>
                <p style="font-size: 11px; color:#64748B; margin-top: 8px;">Support: .zip</p>
            </div>
            <input type="file" id="zipFile" accept=".zip" style="display: none;" onchange="uploadZip()">
            
            <button class="btn btn-secondary" onclick="switchView('view-main')">
                <i class="fas fa-arrow-left"></i> Back to Menu
            </button>

            <div class="terminal" style="margin-top: 16px;">
                <div class="terminal-header">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                    <span class="terminal-title">INJECT_CONSOLE</span>
                </div>
                <div class="terminal-content" id="terminal-inject"></div>
            </div>
        </div>
    </div>
</div>

<script>
    function showToast(msg, isError = false) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `<i class="fas ${isError ? 'fa-exclamation-triangle' : 'fa-check-circle'}"></i> ${msg}`;
        toast.style.background = isError ? '#7F1D1D' : '#1E293B';
        toast.style.borderColor = isError ? '#EF4444' : '#4F46E5';
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    function log(msg, terminalId = 'terminal-main', type = 'info') {
        const term = document.getElementById(terminalId);
        if (!term) return;
        const time = new Date().toLocaleTimeString('id-ID');
        const colors = { info: '#A78BFA', error: '#EF4444', warn: '#F59E0B', sys: '#64748B' };
        const color = colors[type] || '#A78BFA';
        term.innerHTML += `<span style="color:#334155;">[${time}]</span> <span style="color:${color}">${msg}</span><br>`;
        term.scrollTop = term.scrollHeight;
    }

    function switchView(viewId) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.getElementById(viewId).classList.add('active');
    }

    function fetchSysInfo() {
        fetch('/api/sysinfo')
            .then(res => res.json())
            .then(data => {
                document.getElementById('stat-device').innerText = data.device;
                document.getElementById('stat-battery').innerText = data.battery;
                document.getElementById('stat-temp').innerText = data.temp;
            }).catch(() => {
                document.getElementById('stat-device').innerText = 'Unknown';
            });
    }

    function login() {
        const user = document.getElementById('username').value;
        const pass = document.getElementById('password').value;
        const msgEl = document.getElementById('loginMsg');

        if (!user || !pass) {
            msgEl.innerText = 'Isi username & password!';
            return;
        }

        fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user: user, pass: pass })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                switchView('view-main');
                fetchSysInfo();
                log(`Welcome back, ${user}!`, 'terminal-main', 'info');
                showToast('Login successful!');
            } else {
                msgEl.innerText = data.msg;
                showToast(data.msg, true);
            }
        })
        .catch(() => {
            msgEl.innerText = 'Server offline!';
            showToast('Server offline!', true);
        });
    }

    function execCmd(mode, id, terminalId, btn) {
        if (btn.disabled) return;
        const oldText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> WAIT...';
        btn.disabled = true;

        log(`Executing ${mode}:${id}...`, terminalId, 'sys');

        fetch('/api/exec', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mode: mode, id: id })
        })
        .then(res => res.json())
        .then(data => {
            log(data.msg, terminalId, data.status === 'success' ? 'info' : 'error');
        })
        .catch(() => {
            log('[X] Server error!', terminalId, 'error');
        })
        .finally(() => {
            btn.innerHTML = oldText;
            btn.disabled = false;
        });
    }

    function uploadZip() {
        const fileInput = document.getElementById('zipFile');
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('zipfile', file);

        log(`Uploading ${file.name}...`, 'terminal-inject', 'sys');

        fetch('/api/inject', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            log(data.msg, 'terminal-inject', data.status === 'success' ? 'info' : 'error');
            if (data.status === 'success') showToast('Mod injected!');
            else showToast(data.msg, true);
        })
        .catch(() => {
            log('[X] Upload failed!', 'terminal-inject', 'error');
            showToast('Upload failed!', true);
        });

        fileInput.value = '';
    }

    // Auto refresh sysinfo every 10 sec
    setInterval(() => {
        if (document.getElementById('view-main').classList.contains('active')) {
            fetchSysInfo();
        }
    }, 10000);
</script>
</body>
</html>
"""

# ==========================================
# API ROUTES
# ==========================================
@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/sysinfo', methods=['GET'])
def api_sysinfo():
    if not session.get('logged_in'):
        return jsonify({"device": "Locked", "battery": "--", "temp": "--"})
    
    try:
        model = subprocess.run("getprop ro.product.model", shell=True, capture_output=True, text=True, timeout=2)
        model_out = model.stdout.strip() or "Unknown"
        
        battery = subprocess.run("dumpsys battery | grep level", shell=True, capture_output=True, text=True, timeout=2)
        bat_out = battery.stdout.strip()
        bat_percent = bat_out.split(":")[-1].strip() + "%" if ":" in bat_out else "100%"
        
        temp = subprocess.run("dumpsys battery | grep temperature", shell=True, capture_output=True, text=True, timeout=2)
        temp_out = temp.stdout.strip()
        temp_c = str(round(int(temp_out.split(":")[-1].strip()) / 10, 1)) + "°C" if ":" in temp_out else "--"
        
        return jsonify({"device": model_out, "battery": bat_percent, "temp": temp_c})
    except:
        return jsonify({"device": "Error", "battery": "--", "temp": "--"})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('user')
    password = data.get('pass')
    hwid = get_hwid()
    
    users = load_users()
    
    if username not in users:
        return jsonify({"status": "fail", "msg": "Username not found!"})
    
    if users[username]['password'] != password:
        return jsonify({"status": "fail", "msg": "Wrong password!"})
    
    if users[username].get('banned', False):
        return jsonify({"status": "fail", "msg": "Account banned!"})
    
    db_hwid = users[username].get('hwid', '')
    
    if not db_hwid:
        users[username]['hwid'] = hwid
        save_users(users)
        session['logged_in'] = True
        session['username'] = username
        return jsonify({"status": "success", "msg": "Login & Device locked!"})
    elif db_hwid == hwid:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({"status": "success", "msg": "Login success!"})
    else:
        return jsonify({"status": "fail", "msg": "HWID mismatch! Device locked."})

@app.route('/api/inject', methods=['POST'])
def api_inject():
    if not session.get('logged_in'):
        return jsonify({"status": "fail", "msg": "Unauthorized!"})
    
    if 'zipfile' not in request.files:
        return jsonify({"status": "fail", "msg": "No file uploaded!"})
    
    file = request.files['zipfile']
    if file.filename == '':
        return jsonify({"status": "fail", "msg": "Empty filename!"})
    
    if not file.filename.endswith('.zip'):
        return jsonify({"status": "fail", "msg": "Only ZIP files!"})
    
    try:
        # Backup existing files if any
        backup_dir = f"{MODS_DIR}/backup_{int(time.time())}"
        if os.path.exists(BLOOD_STRIKE_PATH):
            os.makedirs(backup_dir, exist_ok=True)
            subprocess.run(f"cp -r {BLOOD_STRIKE_PATH}/* {backup_dir}/", shell=True)
        
        # Save and extract
        save_path = f"{MODS_DIR}/{file.filename}"
        file.save(save_path)
        
        with zipfile.ZipFile(save_path, 'r') as zip_ref:
            zip_ref.extractall(BLOOD_STRIKE_PATH)
        
        return jsonify({"status": "success", "msg": f"Injected {file.filename} to Blood Strike!"})
    except Exception as e:
        return jsonify({"status": "fail", "msg": f"Inject failed: {str(e)}"})

def format_response(base_msg, system_output):
    if system_output:
        return f"{base_msg}<br><span style='color:#64748B;font-size:10px;'>[out] {system_output.replace(chr(10), '<br>')}</span>"
    return base_msg

@app.route('/api/exec', methods=['POST'])
def api_exec():
    if not session.get('logged_in'):
        return jsonify({"status": "fail", "msg": "Unauthorized!"})
    
    req = request.json
    mode = req.get('mode')
    cmd_id = req.get('id')
    msg = ""
    
    try:
        if mode == 'nr':
            if cmd_id == '1':
                out = run_commands(["adb shell wm density 160"])
                msg = format_response("✓ DPI 720 APPLIED!", out)
            elif cmd_id == '2':
                out = run_commands(["adb shell settings put global window_animation_scale 0.0", "adb shell settings put global transition_animation_scale 0.0", "adb shell settings put global animator_duration_scale 0.0"])
                msg = format_response("✓ ANIMATION KILLED!", out)
            elif cmd_id == '3':
                out = run_commands(["adb shell settings put system pointer_speed 7"])
                msg = format_response("✓ TOUCH BOOSTED!", out)
            elif cmd_id == '4':
                out = run_commands(["adb shell cmd power set-fixed-performance-mode-enabled true"])
                msg = format_response("✓ HIGH PERF ON!", out)
            elif cmd_id == '5':
                out = run_commands(["adb shell settings put global tcp_congestion_control cubic"])
                msg = format_response("✓ PING STABILIZED!", out)
            elif cmd_id == '6':
                out = run_commands(["adb shell settings put secure long_press_timeout 250"])
                msg = format_response("✓ SAMPLING OPTIMIZED!", out)
            elif cmd_id == '7':
                out = run_commands(["adb shell cmd deviceidle disable"])
                msg = format_response("✓ DOZE DISABLED!", out)
            elif cmd_id == '8':
                out = run_commands(["adb shell settings put global game_mode_preferred_performance 1"])
                msg = format_response("✓ GAME MODE ON!", out)
            elif cmd_id == '9':
                out = run_commands([
                    "adb shell wm density 160",
                    "adb shell settings put global window_animation_scale 0.0",
                    "adb shell settings put system pointer_speed 7",
                    "adb shell cmd power set-fixed-performance-mode-enabled true"
                ])
                msg = format_response("✓ ALL TWEAKS APPLIED!", out)
        
        elif mode == 'r':
            try:
                check = subprocess.run("su -c 'echo 1'", shell=True, capture_output=True, timeout=3)
                if check.returncode != 0:
                    return jsonify({"status": "fail", "msg": "Device not rooted!"})
            except:
                return jsonify({"status": "fail", "msg": "Root timeout/denied!"})
            
            if cmd_id == '1':
                out = run_commands(["su -c 'wm density 160'"])
                msg = format_response("✓ DPI OK!", out)
            elif cmd_id == '2':
                out = run_commands(["su -c 'for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > $cpu; done'"])
                msg = format_response("✓ CPU PERF!", out)
            elif cmd_id == '3':
                out = run_commands(["su -c 'setprop debug.egl.hw 1'"])
                msg = format_response("✓ GPU BOOST!", out)
            elif cmd_id == '4':
                out = run_commands(["su -c 'stop thermal-engine'"])
                msg = format_response("✓ THERMAL KILLED!", out)
            elif cmd_id == '5':
                out = run_commands(["su -c 'stop logd'"])
                msg = format_response("✓ LOGD STOPPED!", out)
            elif cmd_id == '6':
                out = run_commands(["su -c 'echo 0 > /sys/module/lowmemorykiller/parameters/enable_lmk'"])
                msg = format_response("✓ LMK DISABLED!", out)
            elif cmd_id == '7':
                out = run_commands(["su -c 'for i in /sys/block/*/queue/scheduler; do echo deadline > $i; done'"])
                msg = format_response("✓ I/O DEADLINE!", out)
            elif cmd_id == '8':
                out = run_commands(["su -c 'fstrim -v /data'"])
                msg = format_response("✓ TRIM OK!", out)
            elif cmd_id == '9':
                out = run_commands(["su -c 'sysctl -w net.ipv4.tcp_congestion_control=bbr'"])
                msg = format_response("✓ BBR ACTIVE!", out)
            elif cmd_id == '10':
                out = run_commands([
                    "su -c 'wm density 160'",
                    "su -c 'for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo performance > $cpu; done'",
                    "su -c 'stop logd'"
                ])
                msg = format_response("✓ EXTREME TWEAKS!", out)
        
        elif mode == 'reset':
            if cmd_id == 'adb':
                out = run_commands([
                    "adb shell wm density reset",
                    "adb shell settings put global window_animation_scale 1.0",
                    "adb shell settings put global transition_animation_scale 1.0",
                    "adb shell settings put global animator_duration_scale 1.0"
                ])
                msg = format_response("✓ ADB RESTORED!", out)
            else:
                out = run_commands([
                    "su -c 'wm density reset'",
                    "su -c 'settings put global window_animation_scale 1.0'",
                    "su -c 'for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do echo schedutil > $cpu; done'",
                    "su -c 'start logd'",
                    "su -c 'start thermal-engine'"
                ])
                msg = format_response("✓ ROOT RESTORED!", out)
        
        return jsonify({"status": "success", "msg": msg})
    except Exception as e:
        return jsonify({"status": "fail", "msg": f"Error: {str(e)}"})

# ==========================================
# RUN SERVER
# ==========================================
def start_browser():
    time.sleep(2)
    os.system("termux-open-url http://127.0.0.1:5005")

if __name__ == "__main__":
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    
    # Buat user default kalo belum ada
    users = load_users()
    if not users:
        users["velionx"] = {
            "password": "admin123",
            "hwid": "",
            "banned": False
        }
        save_users(users)
        print("[✓] Default user created: velionx / admin123")
    
    print("\033[1;95m╔═══════════════════════════════════╗\033[0m")
    print("\033[1;95m║     VELIONX BLOOD STRIKE PANEL    ║\033[0m")
    print("\033[1;95m║   Dark Modern Professional Ed     ║\033[0m")
    print("\033[1;95m╚═══════════════════════════════════╝\033[0m")
    print("\n\033[96m[*] Server running at: http://127.0.0.1:5005\033[0m")
    print("\033[93m[*] Default login: velionx / admin123\033[0m")
    
    threading.Thread(target=start_browser).start()
    app.run(host="127.0.0.1", port=5005)