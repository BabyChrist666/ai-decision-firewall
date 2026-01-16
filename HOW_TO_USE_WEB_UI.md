# 🚀 How to Use Baby AGI Web UI

## Step-by-Step Guide

### 1️⃣ Start the Web UI

**Option A: Use the startup script (Easiest)**

On **Linux/Mac**:
```bash
cd /home/user/ai-decision-firewall
./start_baby_agi_ui.sh
```

On **Windows**:
```bash
cd C:\path\to\ai-decision-firewall
start_baby_agi_ui.bat
```

**Option B: Start manually**:
```bash
python -m baby_agi.web_server
```

You'll see:
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                      🤖 Baby AGI UI 🤖                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Starting web server...
Open your browser and go to: http://localhost:8080
```

---

### 2️⃣ Open Your Browser

Open any modern browser (Chrome, Firefox, Edge, Safari) and go to:

```
http://localhost:8080
```

---

### 3️⃣ What You'll See

You'll see a beautiful dashboard with:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              🤖 Baby AGI                            │
│         Autonomous Agent for Any Task               │
│                                                     │
└─────────────────────────────────────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│  Set Objective       │  │  Created Files       │
│  ─────────────       │  │  ──────────────      │
│  Status: Idle        │  │                      │
│                      │  │  No files yet...     │
│  [Text Area]         │  │                      │
│                      │  │                      │
│  LLM Model: [▼]      │  │                      │
│                      │  │                      │
│  [🚀 Start Button]   │  │                      │
└──────────────────────┘  └──────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Execution Log                                      │
│  ──────────────                                     │
│  Waiting for objective...                           │
└─────────────────────────────────────────────────────┘
```

---

### 4️⃣ Give Baby AGI an Objective

**In the text area**, type what you want Baby AGI to do:

**Examples:**

```
Create a folder called my_project
```

```
Create a Python calculator
```

```
Build a TODO app with add, remove, and list functions
```

```
Create a web scraper that extracts article titles
```

---

### 5️⃣ Choose LLM Model (Optional)

In the dropdown, select:

- **Local** (Default) - No API key needed, works offline
- **OpenAI** - Better reasoning (requires API key)
- **Anthropic** - Advanced planning (requires API key)

For most tasks, **Local** works great!

---

### 6️⃣ Click "🚀 Start Baby AGI"

The button will become disabled and you'll see:

```
Status: Running
```

---

### 7️⃣ Watch the Magic Happen! ✨

You'll see **real-time updates** in the Execution Log:

```
[12:34:56] Objective set: Create a Python calculator
[12:34:56] Generated 1 initial tasks
[12:34:56] Starting Baby AGI execution loop...
[12:34:56] Executing: [code_write] Create python file
[12:34:56] ✓ Success: Code written: workspace/script.py
[12:34:57] ✓ Objective completed!
```

---

### 8️⃣ See Created Files

The **Created Files** section will update automatically:

```
┌──────────────────────┐
│  Created Files       │
│  ──────────────      │
│  📄 calculator.py    │
│  📄 utils.py         │
│  📄 README.md        │
└──────────────────────┘
```

---

### 9️⃣ Check Your Results

All files are in the `workspace/` folder:

```bash
ls workspace/
# Output: calculator.py  utils.py  README.md
```

---

### 🔟 Try Another Objective!

The UI stays open - just enter a new objective and click Start again!

---

## 🎨 What Makes It Special

### Real-Time Updates
- See every action Baby AGI takes
- No page refresh needed
- Instant feedback

### Beautiful Design
- Purple gradient background
- Clean card layout
- Smooth animations
- Professional look

### Easy to Use
- Type and click - that's it!
- No commands to remember
- Visual feedback on everything
- Color-coded log messages

### Live File Monitoring
- See files as they're created
- Automatic updates
- No need to check folders

---

## 💡 Pro Tips

1. **Keep the browser tab open** - WebSocket connection needs it
2. **Watch the logs** - See exactly what's happening
3. **Start simple** - Try easy objectives first
4. **Check workspace/** - Files appear there immediately
5. **Try multiple objectives** - The UI stays running

---

## 🎯 Example Session

Let's create a calculator:

1. **Start UI:** `./start_baby_agi_ui.sh`
2. **Open:** http://localhost:8080
3. **Type:** "Create a Python calculator"
4. **Click:** 🚀 Start Baby AGI
5. **Watch:** Real-time execution in logs
6. **See:** calculator.py appears in file list
7. **Check:** `cat workspace/calculator.py`
8. **Run:** `python workspace/calculator.py`

Result:
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# ... full calculator code
```

---

## 🔧 Troubleshooting

### "Connection Failed"
- Make sure server is running
- Check http://localhost:8080 is accessible
- Try refreshing the page

### "No Updates Showing"
- Open browser console (F12)
- Look for WebSocket errors
- Restart the server

### "Port Already in Use"
- Another program is using port 8080
- Stop it: `pkill -f web_server`
- Or change port in `web_server.py`

---

## 🎬 Video Walkthrough (Concept)

If this were a video, you'd see:

1. ✅ Terminal starting the server
2. ✅ Browser opening to beautiful UI
3. ✅ Typing an objective
4. ✅ Clicking Start button
5. ✅ Logs scrolling with updates
6. ✅ Files appearing in real-time
7. ✅ Success message
8. ✅ Checking the created files

---

## 🌟 Why Use the Web UI?

| Feature | Web UI | CLI |
|---------|--------|-----|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Visual Appeal | ⭐⭐⭐⭐⭐ | ⭐ |
| Real-time Updates | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| File Monitoring | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Beginner Friendly | ⭐⭐⭐⭐⭐ | ⭐⭐ |

**Web UI wins for user experience!** 🏆

---

## 📞 Next Steps

1. **Try it now:** `./start_baby_agi_ui.sh`
2. **Experiment:** Give it different objectives
3. **Learn:** Watch how it breaks down tasks
4. **Build:** Create real projects with it
5. **Share:** Show friends your autonomous AI!

---

**Enjoy your beautiful Baby AGI interface! 🎨🤖**

Made with ❤️ for easy AI automation
