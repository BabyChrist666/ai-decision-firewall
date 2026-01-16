"""Web server for Baby AGI UI."""
import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

from baby_agi.agent import BabyAGI
from baby_agi.models import Task


app = FastAPI(title="Baby AGI Web UI")

# Global state
current_agent: Optional[BabyAGI] = None
active_websockets: List[WebSocket] = []
execution_log: List[Dict[str, Any]] = []


class ObjectiveRequest(BaseModel):
    """Request to set a new objective."""
    objective: str
    workspace_dir: str = "./workspace"
    memory_dir: str = "./memory"
    llm_model: str = "local"
    api_key: Optional[str] = None


class BabyAGIWebWrapper:
    """Wrapper for Baby AGI that sends updates via WebSocket."""

    def __init__(self, agent: BabyAGI):
        self.agent = agent
        self.original_log = agent.log
        agent.log = self.log_with_broadcast

    def log_with_broadcast(self, message: str, level: str = "INFO"):
        """Log and broadcast to all connected WebSockets."""
        self.original_log(message, level)

        # Create log entry
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
        }

        execution_log.append(entry)

        # Broadcast to all websockets
        asyncio.create_task(broadcast_update({
            "type": "log",
            "data": entry,
        }))


async def broadcast_update(message: Dict[str, Any]):
    """Broadcast update to all connected WebSockets."""
    disconnected = []
    for websocket in active_websockets:
        try:
            await websocket.send_json(message)
        except:
            disconnected.append(websocket)

    # Remove disconnected websockets
    for ws in disconnected:
        if ws in active_websockets:
            active_websockets.remove(ws)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the main UI page."""
    html_path = Path(__file__).parent / "ui" / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    return HTMLResponse(content=get_default_html(), status_code=200)


@app.post("/api/objective")
async def set_objective(request: ObjectiveRequest):
    """Set a new objective for Baby AGI."""
    global current_agent

    try:
        # Create new agent
        agent = BabyAGI(
            workspace_dir=request.workspace_dir,
            memory_dir=request.memory_dir,
            llm_model=request.llm_model,
            api_key=request.api_key,
            verbose=True,
        )

        # Wrap agent for web updates
        current_agent = BabyAGIWebWrapper(agent)

        # Set objective
        agent.set_objective(request.objective)

        # Run in background
        asyncio.create_task(run_agent_async(agent))

        return {
            "status": "started",
            "objective": request.objective,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
        }


async def run_agent_async(agent: BabyAGI):
    """Run Baby AGI asynchronously."""
    try:
        await broadcast_update({
            "type": "status",
            "data": {"status": "running"},
        })

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        summary = await loop.run_in_executor(None, agent.run)

        await broadcast_update({
            "type": "completed",
            "data": summary,
        })

        await broadcast_update({
            "type": "status",
            "data": {"status": "idle"},
        })
    except Exception as e:
        await broadcast_update({
            "type": "error",
            "data": {"error": str(e)},
        })


@app.get("/api/status")
async def get_status():
    """Get current Baby AGI status."""
    if current_agent and current_agent.agent:
        return current_agent.agent.get_status()
    return {
        "is_running": False,
        "message": "No active agent",
    }


@app.get("/api/files")
async def get_files():
    """Get list of created files."""
    if current_agent and current_agent.agent:
        return {
            "files": current_agent.agent.get_workspace_files(),
        }
    return {"files": []}


@app.get("/api/logs")
async def get_logs(limit: int = 100):
    """Get execution logs."""
    return {
        "logs": execution_log[-limit:],
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_websockets.append(websocket)

    try:
        # Send initial status
        await websocket.send_json({
            "type": "connected",
            "data": {"message": "Connected to Baby AGI"},
        })

        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            # Handle any incoming messages if needed

    except WebSocketDisconnect:
        if websocket in active_websockets:
            active_websockets.remove(websocket)


def get_default_html() -> str:
    """Get default HTML content."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Baby AGI</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .header {
                background: white;
                border-radius: 15px;
                padding: 30px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 {
                font-size: 2.5em;
                color: #667eea;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                font-size: 1.1em;
            }
            .main-content {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            .card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .card h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            .input-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #333;
                font-weight: 500;
            }
            input, textarea, select {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            input:focus, textarea:focus, select:focus {
                outline: none;
                border-color: #667eea;
            }
            textarea {
                min-height: 100px;
                resize: vertical;
            }
            button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 1.1em;
                cursor: pointer;
                transition: transform 0.2s;
                width: 100%;
            }
            button:hover {
                transform: translateY(-2px);
            }
            button:active {
                transform: translateY(0);
            }
            button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .status {
                padding: 10px 20px;
                border-radius: 8px;
                margin-bottom: 15px;
                font-weight: 500;
            }
            .status.idle { background: #e3f2fd; color: #1976d2; }
            .status.running { background: #fff3e0; color: #f57c00; }
            .status.completed { background: #e8f5e9; color: #388e3c; }
            .status.error { background: #ffebee; color: #d32f2f; }
            .log-container {
                max-height: 400px;
                overflow-y: auto;
                background: #f5f5f5;
                border-radius: 8px;
                padding: 15px;
            }
            .log-entry {
                padding: 8px;
                margin-bottom: 5px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }
            .log-entry.INFO { background: #e3f2fd; }
            .log-entry.SUCCESS { background: #e8f5e9; }
            .log-entry.ERROR { background: #ffebee; }
            .log-entry.WARNING { background: #fff3e0; }
            .file-list {
                list-style: none;
            }
            .file-list li {
                padding: 8px;
                margin: 5px 0;
                background: #f5f5f5;
                border-radius: 4px;
            }
            .full-width {
                grid-column: 1 / -1;
            }
            @media (max-width: 768px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Baby AGI</h1>
                <p class="subtitle">Autonomous Agent for Any Task</p>
            </div>

            <div class="main-content">
                <div class="card">
                    <h2>Set Objective</h2>
                    <div class="status idle" id="status">Status: Idle</div>

                    <div class="input-group">
                        <label>What would you like Baby AGI to do?</label>
                        <textarea id="objective" placeholder="Example: Create a Python calculator"></textarea>
                    </div>

                    <div class="input-group">
                        <label>LLM Model</label>
                        <select id="llm-model">
                            <option value="local">Local (No API required)</option>
                            <option value="openai">OpenAI (GPT-4)</option>
                            <option value="anthropic">Anthropic (Claude)</option>
                        </select>
                    </div>

                    <button id="start-btn" onclick="startObjective()">🚀 Start Baby AGI</button>
                </div>

                <div class="card">
                    <h2>Created Files</h2>
                    <ul class="file-list" id="file-list">
                        <li style="color: #999;">No files yet...</li>
                    </ul>
                </div>

                <div class="card full-width">
                    <h2>Execution Log</h2>
                    <div class="log-container" id="log-container">
                        <div class="log-entry INFO">Waiting for objective...</div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let ws = null;
            let isRunning = false;

            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                ws = new WebSocket(protocol + '//' + window.location.host + '/ws');

                ws.onopen = () => {
                    console.log('Connected to Baby AGI');
                    addLog('INFO', 'Connected to Baby AGI server');
                };

                ws.onmessage = (event) => {
                    const message = JSON.parse(event.data);
                    handleMessage(message);
                };

                ws.onclose = () => {
                    console.log('Disconnected');
                    setTimeout(connectWebSocket, 3000);
                };
            }

            function handleMessage(message) {
                if (message.type === 'log') {
                    addLog(message.data.level, message.data.message);
                } else if (message.type === 'status') {
                    updateStatus(message.data.status);
                } else if (message.type === 'completed') {
                    handleCompletion(message.data);
                } else if (message.type === 'error') {
                    addLog('ERROR', 'Error: ' + message.data.error);
                    updateStatus('error');
                }
            }

            function addLog(level, message) {
                const container = document.getElementById('log-container');
                const entry = document.createElement('div');
                entry.className = 'log-entry ' + level;
                entry.textContent = '[' + new Date().toLocaleTimeString() + '] ' + message;
                container.appendChild(entry);
                container.scrollTop = container.scrollHeight;
            }

            function updateStatus(status) {
                const statusEl = document.getElementById('status');
                statusEl.className = 'status ' + status;
                statusEl.textContent = 'Status: ' + status.charAt(0).toUpperCase() + status.slice(1);

                isRunning = status === 'running';
                document.getElementById('start-btn').disabled = isRunning;

                if (status === 'completed' || status === 'idle') {
                    updateFileList();
                }
            }

            async function updateFileList() {
                try {
                    const response = await fetch('/api/files');
                    const data = await response.json();

                    const fileList = document.getElementById('file-list');
                    fileList.innerHTML = '';

                    if (data.files.length === 0) {
                        fileList.innerHTML = '<li style="color: #999;">No files yet...</li>';
                    } else {
                        data.files.forEach(file => {
                            const li = document.createElement('li');
                            li.textContent = '📄 ' + file;
                            fileList.appendChild(li);
                        });
                    }
                } catch (e) {
                    console.error('Failed to update file list:', e);
                }
            }

            function handleCompletion(data) {
                addLog('SUCCESS', '✓ Objective completed!');
                addLog('INFO', 'Tasks completed: ' + data.tasks.completed);
                addLog('INFO', 'Time: ' + data.elapsed_time.toFixed(2) + 's');
                updateStatus('completed');
            }

            async function startObjective() {
                const objective = document.getElementById('objective').value.trim();
                if (!objective) {
                    alert('Please enter an objective');
                    return;
                }

                const llmModel = document.getElementById('llm-model').value;

                updateStatus('running');
                document.getElementById('log-container').innerHTML = '';
                addLog('INFO', 'Starting objective: ' + objective);

                try {
                    const response = await fetch('/api/objective', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            objective: objective,
                            llm_model: llmModel,
                        }),
                    });

                    const data = await response.json();

                    if (data.status === 'error') {
                        addLog('ERROR', 'Failed to start: ' + data.error);
                        updateStatus('error');
                    }
                } catch (e) {
                    addLog('ERROR', 'Failed to start: ' + e.message);
                    updateStatus('error');
                }
            }

            // Initialize
            connectWebSocket();
            updateFileList();

            // Allow Enter to submit (with Shift+Enter for new line)
            document.getElementById('objective').addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    startObjective();
                }
            });
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 60)
    print("🤖 Baby AGI Web UI")
    print("=" * 60)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:8080")
    print("\nPress Ctrl+C to stop")
    print("=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8080)
