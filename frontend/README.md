# AI Decision Firewall - Frontend Dashboard

A cyberpunk-styled frontend dashboard for the AI Decision Firewall backend.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend server running on `http://127.0.0.1:8000`

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The application will open at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

## 🎨 Features

- **Cyberpunk Design**: Dark theme with neon accents
- **Firewall Interface**: Submit AI outputs for evaluation
- **Live Verdict Display**: Real-time verdict, risk score, and explanations
- **System Log Stream**: Animated terminal-style logs
- **Risk Visualization**: Visual risk meter with color coding

## 🔧 Configuration

The API endpoint is configured in `src/api.js`. Default backend URL:
- `http://127.0.0.1:8000`

## 📦 Tech Stack

- React 18
- Vite
- Tailwind CSS
- JetBrains Mono font

## 🎯 Usage

1. Enter AI-generated output in the text area
2. Set confidence level (0-100%)
3. Select intended action (answer, email, trade, execute_code)
4. Optionally add source URLs (comma-separated)
5. Click "INTERCEPT OUTPUT"
6. View the verdict and detailed analysis

## 🎨 Theme Colors

- **Background**: Deep black/dark blue
- **Accents**: Neon cyan, magenta, green
- **Status Colors**: 
  - Green: ALLOW
  - Yellow: REQUIRE_EVIDENCE
  - Red: BLOCK, REQUIRE_HUMAN_REVIEW




