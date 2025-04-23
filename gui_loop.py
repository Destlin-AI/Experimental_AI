from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from MemoryPanel import list_fragment_summary
from LLMPanel import get_llm_status
from AgentPanel import list_agents
from SystemMonitor import get_system_info

app = FastAPI()

# Allow local web UI / Electron to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "🧠 Symbolic Memory GUI Online"}

@app.get("/memory")
def get_memory():
    return list_fragment_summary()

@app.get("/llm")
def get_llm():
    return get_llm_status()

@app.get("/agents")
def get_agents():
    return list_agents()

@app.get("/system")
def get_system_stats():
    return get_system_info()

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard_html():
    try:
        with open("frontend/dashboard.html", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return HTMLResponse(content="<h1>🧠 GUI not built yet</h1>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gui_loop:app", host="127.0.0.1", port=8000, reload=True)
