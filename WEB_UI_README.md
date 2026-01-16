# 🌐 Baby AGI Web UI

Beautiful web interface for Baby AGI - run it on your laptop with a modern, real-time dashboard!

## 🚀 Quick Start

### Start the Web UI

**On Linux/Mac:**
```bash
./start_baby_agi_ui.sh
```

**On Windows:**
```bash
start_baby_agi_ui.bat
```

**Or manually:**
```bash
python -m baby_agi.web_server
```

Then open your browser to: **http://localhost:8080**

---

## ✨ Features

### 📊 Real-Time Dashboard
- Live execution logs
- Task progress updates
- File creation monitoring
- Status indicators

### 🎯 Easy Objective Setting
- Simple text input for objectives
- Choose LLM model (Local, OpenAI, Claude)
- One-click execution
- Real-time feedback

### 📁 File Management
- See all created files
- Automatic workspace monitoring
- Updates in real-time

### 🔄 Live Updates
- WebSocket connection
- Instant log streaming
- No page refresh needed

---

## 🎨 UI Features

### Beautiful Modern Design
- **Gradient backgrounds** - Eye-catching purple gradient
- **Card-based layout** - Clean, organized interface
- **Responsive design** - Works on desktop and tablet
- **Smooth animations** - Professional feel

### Status Indicators
- 🔵 **Idle** - Ready for new objective
- 🟠 **Running** - Currently executing tasks
- 🟢 **Completed** - Objective achieved
- 🔴 **Error** - Something went wrong

### Real-Time Log
- Color-coded messages (Info, Success, Error, Warning)
- Auto-scroll to latest
- Timestamps on all entries
- Clean monospace font

---

## 📖 Usage Examples

### Example 1: Create a Folder
1. Open http://localhost:8080
2. Type: "Create a folder called my_project"
3. Click "🚀 Start Baby AGI"
4. Watch it work in real-time!

### Example 2: Build a Calculator
1. Type: "Create a Python calculator"
2. Click Start
3. See the code being written live
4. Check created files in the dashboard

### Example 3: Complex Project
1. Type: "Build a TODO app with add, remove, and list functions"
2. Watch Baby AGI:
   - Plan the project
   - Create files
   - Write code
   - Organize structure
3. See all files appear in the dashboard

---

## 🛠️ Configuration

### LLM Models

**Local (Default)**
- No API key required
- Runs completely offline
- Rule-based task generation
- Fast and free

**OpenAI**
- Better reasoning
- More creative solutions
- Requires API key in environment: `OPENAI_API_KEY`

**Anthropic Claude**
- Advanced planning
- Detailed analysis
- Requires API key in environment: `ANTHROPIC_API_KEY`

### Workspace Settings

The web UI uses default workspace locations:
- **Workspace:** `./workspace`
- **Memory:** `./memory`

Files created by Baby AGI will appear in the workspace directory.

---

## 🎯 Web UI vs CLI

| Feature | Web UI | CLI |
|---------|--------|-----|
| Visual Interface | ✅ Beautiful | ❌ Terminal only |
| Real-time Updates | ✅ Live | ⚠️ Verbose mode |
| File Monitoring | ✅ Dashboard | ❌ Manual check |
| Easy to Use | ✅ Click & go | ⚠️ Commands |
| Multiple Objectives | ✅ Sequential | ⚠️ Restart needed |
| Progress Tracking | ✅ Visual | ⚠️ Text logs |

**Recommendation:** Use Web UI for better experience!

---

## 🔧 Technical Details

### Technology Stack
- **Backend:** FastAPI + Python
- **Frontend:** HTML + CSS + JavaScript
- **Real-time:** WebSockets
- **Async:** asyncio for non-blocking execution

### API Endpoints

```
GET  /                  - Main UI page
POST /api/objective     - Start new objective
GET  /api/status        - Get current status
GET  /api/files         - Get created files
GET  /api/logs          - Get execution logs
WS   /ws                - WebSocket connection
```

### WebSocket Messages

**From Server:**
```json
{
  "type": "log",
  "data": {
    "level": "INFO",
    "message": "Task completed"
  }
}
```

**Status Updates:**
```json
{
  "type": "status",
  "data": {"status": "running"}
}
```

---

## 🎨 Customization

### Change Port

Edit `baby_agi/web_server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # Change port here
```

### Modify UI

The HTML is embedded in `web_server.py` in the `get_default_html()` function. Edit the styles, layout, or colors there.

### Add Features

The web server is modular - easy to add:
- New API endpoints
- Additional dashboard cards
- Custom visualizations
- Enhanced controls

---

## 📱 Screenshots (What You'll See)

### Header
```
┌─────────────────────────────────────────┐
│  🤖 Baby AGI                            │
│  Autonomous Agent for Any Task          │
└─────────────────────────────────────────┘
```

### Objective Input
```
┌─────────────────────────────────────────┐
│  Set Objective                          │
│  Status: Idle                           │
│                                         │
│  [Text Area: Your objective here]       │
│  [Dropdown: Local/OpenAI/Claude]        │
│  [🚀 Start Baby AGI Button]            │
└─────────────────────────────────────────┘
```

### File List
```
┌─────────────────────────────────────────┐
│  Created Files                          │
│  📄 calculator.py                       │
│  📄 utils.py                            │
│  📄 README.md                           │
└─────────────────────────────────────────┘
```

### Execution Log
```
┌─────────────────────────────────────────┐
│  Execution Log                          │
│  [12:34:56] Starting objective...       │
│  [12:34:57] ✓ Task completed           │
│  [12:34:58] Creating file...            │
└─────────────────────────────────────────┘
```

---

## 🚦 Troubleshooting

### Port Already in Use
```bash
# Change port in web_server.py or:
python -m baby_agi.web_server --port 8081
```

### WebSocket Connection Failed
- Check firewall settings
- Ensure port is not blocked
- Try different browser

### Can't See Updates
- Check browser console for errors
- Refresh the page
- Restart the server

---

## 💡 Pro Tips

1. **Keep the browser tab open** - WebSocket needs active connection
2. **Use Chrome/Firefox** - Best WebSocket support
3. **Check workspace folder** - Files appear there immediately
4. **Try simple objectives first** - Learn how it works
5. **Watch the logs** - See exactly what Baby AGI is doing

---

## 🎯 Next Steps

1. **Start the server:** `./start_baby_agi_ui.sh`
2. **Open browser:** http://localhost:8080
3. **Enter objective:** Type what you want
4. **Watch the magic:** See Baby AGI work in real-time
5. **Check results:** View created files

---

## 📞 Need Help?

- Check the main [BABY_AGI_README.md](BABY_AGI_README.md) for concepts
- Read [QUICKSTART.md](QUICKSTART.md) for basics
- Run `python test_baby_agi.py` to verify installation

---

**Enjoy your beautiful Baby AGI dashboard! 🎨🤖**
