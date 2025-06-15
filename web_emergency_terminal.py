#!/usr/bin/env python3
"""
🌐💻 WEB TERMINAL EMERGENCY ACCESS 💻🌐
Browser-based terminal when SSH fails!
"""

from flask import Flask, render_template_string, request, jsonify
import subprocess
import threading

app = Flask(__name__)

TERMINAL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🆘 Emergency Web Terminal</title>
    <style>
        body {
            background: #000;
            color: #00ff00;
            font-family: monospace;
            margin: 0;
            padding: 20px;
        }
        .terminal {
            background: #111;
            border: 2px solid #00ff00;
            padding: 20px;
            border-radius: 10px;
            min-height: 500px;
        }
        input[type="text"] {
            background: #000;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 10px;
            width: 80%;
            font-family: monospace;
        }
        button {
            background: #00ff00;
            color: #000;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
        }
        .output {
            white-space: pre-wrap;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="terminal">
        <h1>🆘 CHAOSGENIUS EMERGENCY TERMINAL 🆘</h1>
        <p>Emergency web-based access when SSH fails!</p>

        <div class="output" id="output"></div>

        <input type="text" id="command" placeholder="Enter command..." onkeypress="if(event.key==='Enter') executeCommand()">
        <button onclick="executeCommand()">Execute</button>
        <button onclick="emergencyRecovery()">🆘 Emergency Recovery</button>
    </div>

    <script>
        function executeCommand() {
            const command = document.getElementById('command').value;
            const output = document.getElementById('output');

            output.innerHTML += '$ ' + command + '\n';

            fetch('/execute', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: command})
            })
            .then(response => response.json())
            .then(data => {
                output.innerHTML += data.output + '\n';
                output.scrollTop = output.scrollHeight;
            });

            document.getElementById('command').value = '';
        }

        function emergencyRecovery() {
            fetch('/emergency_recovery', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                document.getElementById('output').innerHTML += data.output + '\n';
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def terminal():
    return render_template_string(TERMINAL_HTML)

@app.route('/execute', methods=['POST'])
def execute_command():
    try:
        command = request.json.get('command', '')

        # Security: Only allow safe commands
        safe_commands = ['ls', 'pwd', 'whoami', 'date', 'ps', 'top', 'df', 'free', 'systemctl status']

        if any(cmd in command for cmd in safe_commands):
            result = subprocess.run(command.split(), capture_output=True, text=True, timeout=10)
            output = result.stdout + result.stderr
        else:
            output = "❌ Command not allowed for security reasons"

        return jsonify({'output': output})

    except Exception as e:
        return jsonify({'output': f'Error: {e}'})

@app.route('/emergency_recovery', methods=['POST'])
def emergency_recovery():
    try:
        result = subprocess.run(['/root/ultimate_emergency_recovery.sh'],
                              capture_output=True, text=True)

        return jsonify({'output': '🆘 Emergency recovery executed!\n' + result.stdout})

    except Exception as e:
        return jsonify({'output': f'❌ Recovery failed: {e}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
