#!/usr/bin/env python3
"""
🌐🧠 BROSKI NATURAL LANGUAGE WEB API 🧠🌐
🚀 REST API for Natural Language Agent Control 🚀
👑 "Deploy 3 money bots" → HTTP POST → IT HAPPENS! 👑
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Add the chaosgenius path
sys.path.append("/root/chaosgenius")

try:
    from broski_natural_language_commander import NaturalLanguageCommander
except ImportError as e:
    print(f"⚠️ Import warning: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="🧠 BROSKI Natural Language Agent API",
    description="Control your agent army with natural language commands!",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Natural Language Commander
nl_commander = None


@app.on_event("startup")
async def startup_event():
    """🚀 Initialize the Natural Language Commander on startup"""
    global nl_commander
    try:
        nl_commander = NaturalLanguageCommander()
        nl_commander.command_portal.start_command_monitoring()
        print("🧠💬 Natural Language API ready!")
    except Exception as e:
        print(f"❌ Startup error: {e}")


# Pydantic models for API
class CommandRequest(BaseModel):
    command: str
    priority: Optional[int] = 3
    user_id: Optional[str] = "api_user"


class CommandResponse(BaseModel):
    success: bool
    message: str
    command_id: Optional[str] = None
    results: Optional[List[Dict]] = None
    suggestions: Optional[List[str]] = None
    execution_time: Optional[float] = None


class AgentStatusResponse(BaseModel):
    agent_count: int
    active_agents: int
    pending_commands: int
    dashboard: Dict


class SuggestionsResponse(BaseModel):
    suggestions: List[str]
    partial_input: Optional[str] = None


# API Routes
@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """🏠 Natural Language Command Dashboard"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧠 BROSKI Agent Army Commander</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                margin: 0;
                padding: 20px;
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 {
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 30px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .command-input {
                width: 100%;
                padding: 15px;
                font-size: 18px;
                border: none;
                border-radius: 10px;
                margin-bottom: 20px;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
            }
            .execute-btn {
                width: 100%;
                padding: 15px;
                font-size: 18px;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .execute-btn:hover {
                transform: translateY(-2px);
            }
            .suggestions {
                margin: 20px 0;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 10px;
            }
            .suggestion {
                padding: 10px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.2s;
            }
            .suggestion:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            .results {
                margin-top: 20px;
                padding: 20px;
                background: rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                min-height: 100px;
            }
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .status-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            .status-value {
                font-size: 2em;
                font-weight: bold;
                display: block;
            }
            .loading {
                display: none;
                text-align: center;
                margin: 20px 0;
            }
            .spinner {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-top: 4px solid #fff;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠💜 BROSKI AGENT ARMY COMMANDER 💜🧠</h1>

            <div class="command-section">
                <input type="text" id="commandInput" class="command-input"
                       placeholder="Type your command... e.g., 'deploy 3 money bots' or 'run NFT campaign overnight'"
                       onkeypress="handleKeyPress(event)">
                <button class="execute-btn" onclick="executeCommand()">🚀 EXECUTE COMMAND</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>🧠 Processing your command...</p>
            </div>

            <div class="suggestions" id="suggestions">
                <h3>💡 Quick Commands:</h3>
                <div class="suggestion" onclick="setCommand('deploy 3 money bots')">🤖 Deploy 3 Money Bots</div>
                <div class="suggestion" onclick="setCommand('run NFT campaign overnight')">🎨 Run NFT Campaign Overnight</div>
                <div class="suggestion" onclick="setCommand('check agent status')">📊 Check Agent Status</div>
                <div class="suggestion" onclick="setCommand('boost neural performance')">⚡ Boost Neural Performance</div>
                <div class="suggestion" onclick="setCommand('start crypto campaign')">₿ Start Crypto Campaign</div>
                <div class="suggestion" onclick="setCommand('create mission system optimization')">🎯 Create Optimization Mission</div>
            </div>

            <div class="status-grid" id="statusGrid">
                <!-- Status cards will be populated here -->
            </div>

            <div class="results" id="results">
                <h3>📊 Command Results</h3>
                <p>Enter a command above to see results here...</p>
            </div>
        </div>

        <script>
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    executeCommand();
                }
            }

            function setCommand(command) {
                document.getElementById('commandInput').value = command;
            }

            async function executeCommand() {
                const command = document.getElementById('commandInput').value.trim();
                if (!command) return;

                const loading = document.getElementById('loading');
                const results = document.getElementById('results');

                loading.style.display = 'block';
                results.innerHTML = '<h3>📊 Command Results</h3><p>🧠 Processing...</p>';

                try {
                    const response = await fetch('/api/execute', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            command: command,
                            priority: 3
                        })
                    });

                    const data = await response.json();

                    let html = '<h3>📊 Command Results</h3>';

                    if (data.success) {
                        html += `<div style="color: #4ecdc4; font-weight: bold;">✅ ${data.message}</div>`;

                        if (data.results && data.results.length > 0) {
                            html += '<div style="margin-top: 15px;">';
                            data.results.forEach(result => {
                                if (result.success) {
                                    html += `<div style="margin: 5px 0; color: #90EE90;">🎯 ${result.message}</div>`;
                                }
                            });
                            html += '</div>';
                        }
                    } else {
                        html += `<div style="color: #ff6b6b; font-weight: bold;">❌ ${data.message}</div>`;

                        if (data.suggestions && data.suggestions.length > 0) {
                            html += '<div style="margin-top: 15px;"><strong>💡 Try these instead:</strong>';
                            data.suggestions.forEach(suggestion => {
                                html += `<div style="margin: 5px 0; cursor: pointer; color: #87CEEB;" onclick="setCommand('${suggestion}')">• ${suggestion}</div>`;
                            });
                            html += '</div>';
                        }
                    }

                    results.innerHTML = html;

                } catch (error) {
                    results.innerHTML = `<h3>📊 Command Results</h3><div style="color: #ff6b6b;">❌ Error: ${error.message}</div>`;
                } finally {
                    loading.style.display = 'none';
                }

                // Refresh status after command
                updateStatus();
            }

            async function updateStatus() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();

                    const statusGrid = document.getElementById('statusGrid');
                    statusGrid.innerHTML = '';

                    Object.entries(data.dashboard).forEach(([key, value]) => {
                        const card = document.createElement('div');
                        card.className = 'status-card';
                        card.innerHTML = `
                            <div>${key}</div>
                            <span class="status-value">${value}</span>
                        `;
                        statusGrid.appendChild(card);
                    });

                } catch (error) {
                    console.error('Status update error:', error);
                }
            }

            // Update status on page load and every 30 seconds
            updateStatus();
            setInterval(updateStatus, 30000);
        </script>
    </body>
    </html>
    """


@app.post("/api/execute", response_model=CommandResponse)
async def execute_command(request: CommandRequest, background_tasks: BackgroundTasks):
    """🚀 Execute natural language command"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    start_time = time.time()

    try:
        # Execute the command
        result = nl_commander.execute_natural_command(request.command)

        execution_time = time.time() - start_time

        return CommandResponse(
            success=result["success"],
            message=result["message"],
            command_id=result.get("parsed", {}).get("command_id"),
            results=result.get("results", []),
            suggestions=result.get("suggestions", []),
            execution_time=execution_time,
        )

    except Exception as e:
        execution_time = time.time() - start_time
        return CommandResponse(
            success=False,
            message=f"Command execution error: {str(e)}",
            execution_time=execution_time,
        )


@app.get("/api/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """📊 Get current agent status"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    try:
        dashboard = nl_commander.command_portal.get_command_dashboard()
        active_agents = len(
            [
                a
                for a in nl_commander.command_portal.active_agents.values()
                if a["status"] == "ACTIVE"
            ]
        )

        return AgentStatusResponse(
            agent_count=len(nl_commander.command_portal.active_agents),
            active_agents=active_agents,
            pending_commands=len(
                [
                    c
                    for c in nl_commander.command_portal.command_queue
                    if c["status"] == "PENDING"
                ]
            ),
            dashboard=dashboard,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status retrieval error: {str(e)}")


@app.get("/api/suggestions", response_model=SuggestionsResponse)
async def get_command_suggestions(partial_input: str = ""):
    """💡 Get command suggestions"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    try:
        suggestions = nl_commander.get_command_suggestions(partial_input)
        return SuggestionsResponse(suggestions=suggestions, partial_input=partial_input)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestions error: {str(e)}")


@app.get("/api/agents")
async def get_agents():
    """🤖 Get all available agents"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    try:
        agents = {}
        for agent_id, agent_data in nl_commander.command_portal.active_agents.items():
            agents[agent_id] = nl_commander.command_portal.get_agent_status(agent_id)

        return {"agents": agents}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agents retrieval error: {str(e)}")


@app.post("/api/agents/{agent_id}/command")
async def send_agent_command(
    agent_id: str, command_type: str, command_data: Dict = None, priority: int = 3
):
    """📡 Send direct command to specific agent"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    try:
        if agent_id not in nl_commander.command_portal.active_agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

        command_id = nl_commander.command_portal.issue_command(
            agent_id, command_type, command_data or {}, priority
        )

        return {
            "success": True,
            "command_id": command_id,
            "message": f"Command sent to {agent_id}",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Command error: {str(e)}")


@app.post("/api/missions")
async def create_mission(
    mission_name: str, agent_ids: List[str], objective: str, mission_type: str = "API"
):
    """🎯 Create new mission"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    try:
        mission_id = nl_commander.command_portal.create_mission(
            mission_name, agent_ids, objective, mission_type
        )

        return {
            "success": True,
            "mission_id": mission_id,
            "message": f"Mission '{mission_name}' created successfully",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mission creation error: {str(e)}")


@app.post("/api/missions/{mission_id}/execute")
async def execute_mission(mission_id: str):
    """🚀 Execute mission"""
    if not nl_commander:
        raise HTTPException(
            status_code=500, detail="Natural Language Commander not initialized"
        )

    try:
        if mission_id not in nl_commander.command_portal.agent_missions:
            raise HTTPException(
                status_code=404, detail=f"Mission {mission_id} not found"
            )

        nl_commander.command_portal.execute_mission(mission_id)

        return {"success": True, "message": f"Mission {mission_id} execution started"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Mission execution error: {str(e)}"
        )


@app.get("/api/health")
async def health_check():
    """🏥 API Health Check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "nl_commander": nl_commander is not None,
        "version": "2.0.0",
    }


if __name__ == "__main__":
    import uvicorn

    print("🌐🧠 LAUNCHING BROSKI NATURAL LANGUAGE WEB API! 🧠🌐")

    uvicorn.run(
        "broski_nl_web_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
