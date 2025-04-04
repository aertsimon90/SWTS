from flask import Flask, request
import threading
import json
import os
import time

app = Flask(__name__)
terminal_screen_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terminal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            height: 100vh;
            width: 100vw;
            background: linear-gradient(135deg, #1a1a1a, #2a2a5a);
            font-family: 'Courier New', monospace;
            overflow: hidden;
            position: relative;
        }

        .terminal-container {
            height: 100%;
            width: 100%;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            opacity: 0;
            animation: fadeIn 0.5s ease forwards;
        }

        @keyframes fadeIn {
            to { opacity: 1; }
        }

        .command-bar {
            display: flex;
            gap: 10px;
            height: 40px;
            transition: all 0.3s ease;
            transform-origin: top;
        }

        .command-input {
            width: 60%;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid #404080;
            border-radius: 5px;
            color: #ffffff;
            font-size: 16px;
            resize: none;
            height: 100%;
            transition: all 0.3s ease;
        }

        .command-input:focus {
            outline: none;
            box-shadow: 0 0 5px #5050a0;
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 5px #5050a0; }
            50% { box-shadow: 0 0 10px #5050a0; }
            100% { box-shadow: 0 0 5px #5050a0; }
        }

        .toggle-btn {
            width: 10%;
            padding: 10px;
            background: #303060;
            border: none;
            border-radius: 5px;
            color: #ffffff;
            font-size: 16px;
            cursor: pointer;
            height: 100%;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .toggle-btn:hover {
            background: #404080;
            transform: scale(1.05);
        }

        .toggle-btn:active {
            transform: scale(0.95);
        }

        .toggle-btn::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.3s ease, height 0.3s ease;
        }

        .toggle-btn:hover::after {
            width: 100px;
            height: 100px;
        }

        .run-btn {
            width: 30%;
            padding: 10px;
            background: #404080;
            border: none;
            border-radius: 5px;
            color: #ffffff;
            font-size: 16px;
            cursor: pointer;
            height: 100%;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .run-btn:hover {
            background: #5050a0;
            transform: scale(1.05);
        }

        .run-btn:active {
            transform: scale(0.95);
        }

        .run-btn::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            animation: shine 2s infinite;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .run-btn:hover::before {
            opacity: 1;
        }

        @keyframes shine {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }

        .exit-btn {
            width: 100%;
            padding: 10px;
            background: rgba(255, 80, 80, 0.3); /* Soft red */
            border: 1px solid #ff5050;
            border-radius: 5px;
            color: #ffffff;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .exit-btn:hover {
            background: rgba(255, 80, 80, 0.5);
            transform: scale(1.02);
        }

        .exit-btn:active {
            transform: scale(0.98);
        }

        .exit-btn::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.3s ease, height 0.3s ease;
        }

        .exit-btn:hover::after {
            width: 200px;
            height: 200px;
        }

        .output-area {
            flex: 1;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid #404080;
            border-radius: 5px;
            color: #ffffff;
            font-size: 14px;
            overflow-y: auto;
            resize: none;
            transition: all 0.3s ease;
            transform-origin: top;
        }

        .expanded {
            height: 120px;
            animation: expand 0.3s ease forwards;
        }

        @keyframes expand {
            0% { height: 40px; transform: scaleY(1); }
            100% { height: 120px; transform: scaleY(1); }
        }

        .collapsed {
            animation: collapse 0.3s ease forwards;
        }

        @keyframes collapse {
            0% { height: 120px; transform: scaleY(1); }
            100% { height: 40px; transform: scaleY(1); }
        }

        .black-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #000000;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
        }

        .black-overlay.active {
            opacity: 1;
        }
    </style>
</head>
<body>
    <div class="terminal-container">
        <div class="command-bar">
            <input type="text" id="commandInput" class="command-input" placeholder="Enter command...">
            <button class="toggle-btn" id="toggleBtn">+</button>
            <button class="run-btn" id="runBtn">RUN</button>
        </div>
        <button class="exit-btn" id="exitBtn">EXIT</button>
        <textarea class="output-area" id="outputArea" readonly placeholder="Output will appear here..."></textarea>
        <p>Shield Web Terminal System</p>
    </div>
    <div class="black-overlay" id="blackOverlay"></div>

    <script>
        const commandInput = document.getElementById('commandInput');
        const toggleBtn = document.getElementById('toggleBtn');
        const runBtn = document.getElementById('runBtn');
        const exitBtn = document.getElementById('exitBtn');
        const outputArea = document.getElementById('outputArea');
        const commandBar = document.querySelector('.command-bar');
        const blackOverlay = document.getElementById('blackOverlay');

        let isExpanded = false;

        toggleBtn.addEventListener('click', () => {
            if (!isExpanded) {
                // Expand
                commandBar.classList.remove('collapsed');
                commandBar.classList.add('expanded');
                toggleBtn.textContent = '-';
                
                const currentValue = commandInput.value;
                const newTextarea = document.createElement('textarea');
                newTextarea.id = 'commandInput';
                newTextarea.className = 'command-input';
                newTextarea.value = currentValue;
                newTextarea.placeholder = 'Enter command...';
                commandInput.replaceWith(newTextarea);
                
                isExpanded = true;
            } else {
                // Collapse
                commandBar.classList.remove('expanded');
                commandBar.classList.add('collapsed');
                toggleBtn.textContent = '+';
                
                const currentValue = commandInput.value;
                const newInput = document.createElement('input');
                newInput.type = 'text';
                newInput.id = 'commandInput';
                newInput.className = 'command-input';
                newInput.value = currentValue;
                newInput.placeholder = 'Enter command...';
                commandInput.replaceWith(newInput);
                
                setTimeout(() => commandBar.classList.remove('collapsed'), 300);
                isExpanded = false;
            }
        });

        runBtn.addEventListener('click', async () => {
            const command = document.getElementById('commandInput').value;
            outputArea.style.transform = 'scaleY(0.95)';
            outputArea.style.opacity = '0';
            
            try {
                const response = await fetch('/', {
                    method: 'RUN',
                    headers: {
                        'Content-Type': 'application/text'
                    },
                    body: command
                });
                const result = await response.text();
                outputArea.value = result;
                outputArea.style.transform = 'scaleY(1)';
                outputArea.style.opacity = '1';
            } catch (error) {
                outputArea.value = `Error: ${error.message}`;
                outputArea.style.transform = 'scaleY(1)';
                outputArea.style.opacity = '1';
            }
        });

        exitBtn.addEventListener('click', () => {
            blackOverlay.classList.add('active');
            setTimeout(() => {
                window.close();
            }, 300); // Delay to allow fade animation
        });
    </script>
</body>
</html>"""
database = {}
logs = True
lock = threading.Lock()

def encrypt(content, key):
	content = "t/"+str(content)
	keyn = 0
	for h in key:
		keyn += ord(h)**1.26482717
		keyn = keyn/1.2847372738
		keyn = keyn*1.2482627274
	keyn = keyn**2.63826286
	keyn = int(keyn)
	if keyn%2 == 0:
		keyn = -keyn
	new_content = ""
	for h in content:
		h = ord(h)
		new_content += chr((h+keyn)%1114112)
		keyn = int(keyn*1.738262846)
		keyn += int(h**2.272848372)
	return new_content

def decrypt(content, key):
	keyn = 0
	for h in key:
		keyn += ord(h)**1.26482717
		keyn = keyn/1.2847372738
		keyn = keyn*1.2482627274
	keyn = keyn**2.63826286
	keyn = int(keyn)
	if keyn%2 == 0:
		keyn = -keyn
	new_content = ""
	for h in content:
		h = ord(h)
		h = (h-keyn)%1114112
		new_content += chr(h)
		keyn = int(keyn*1.738262846)
		keyn += int(h**2.272848372)
	if new_content.startswith("t/"):
		return new_content[2:]
	else:
		raise ValueError("Error: Incorrect Key for decryption")

def save_database():
	global database
	data = json.dumps(database, default=repr)
	data = encrypt(data, "HmJdi9K20sKwlNxjwHs8eM2")
	data = json.dumps({".": data}, default=repr)
	with open("database", "w") as f:
		f.write(data)

def load_database():
	global database
	if os.path.exists("database"):
		with open("database", "rb") as f:
			data = f.read().decode("utf-8", errors="ignore")
		data = json.loads(data)["."]
		data = decrypt(data, "HmJdi9K20sKwlNxjwHs8eM2")
		data = json.loads(data)
		with lock:
			database = data

load_database()

def terminal_run(command, client):
	global database
	return "Hello, World!\nYour Command: "+command+"\nYour Client Information: "+repr(client)

@app.route("/", methods=["GET", "RUN"])
def root_path():
	global terminal_screen_code, logs
	if "X-Forwarded-For" in request.headers:
		remote_addr = request.headers["X-Forwarded-For"]
		remote_addr = remote_addr[:remote_addr.find(",")].strip()
	else:
		remote_addr = request.remote_addr
	inputdata = request.get_data(as_text=True)
	client = {"time": time.time(), "remote_addr": remote_addr, "headers": dict(request.headers), "environ": dict(request.environ), "data": inputdata}
	if logs:
		with open("logs", "a") as f:
			clientjson = json.dumps(client, default=repr)
			f.write(clientjson+"\n")
			f.flush()
	if request.method == "GET":
		return terminal_screen_code
	else:
		return terminal_run(inputdata, client)

if __name__ == "__main__":
	app.run(debug=True)