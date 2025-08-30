# TideGuard Alerter

A full-stack coastal weather monitoring system that provides real-time alerts for dangerous weather conditions.

## 🌊 Overview

TideGuard Alerter is a comprehensive weather monitoring solution designed for coastal areas. It simulates weather and tide data, monitors thresholds, and provides instant SMS alerts when dangerous conditions are detected.

### Key Features

- *Real-time Data Simulation*: Generates realistic weather and tide data every 5 seconds
- *Threshold Monitoring*: Alerts when wind speed > 80 km/h OR wave height > 4m
- *SMS Alerts*: Instant notifications via Twilio when thresholds are breached
- *Live Dashboard*: Beautiful React frontend with real-time data display
- *WebSocket Communication*: Real-time updates between backend and frontend
- *Responsive Design*: Works on desktop, tablet, and mobile devices

## 🏗 Architecture


┌─────────────────┐    WebSocket    ┌─────────────────┐
│   Frontend      │ ◄──────────────► │    Backend      │
│   (React)       │                  │   (Flask)       │
│                 │                  │                 │
│ • Dashboard     │                  │ • Data Simulator │
│ • Alert Banner  │                  │ • Threshold Check│
│ • Real-time UI  │                  │ • SMS Alerts    │
└─────────────────┘                  └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │     Twilio      │
                                    │   SMS Service   │
                                    └─────────────────┘


## 📁 Project Structure


TideGuard Alerter/
├── tideguard-backend/          # Flask backend
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── env.example           # Environment variables template
│   ├── README.md             # Backend documentation
│   └── utils/
│       └── data_simulator.py  # Weather data simulation
│
└── tideguard-frontend/        # React frontend
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.jsx  # Main dashboard component
    │   │   └── AlertBanner.jsx # Alert banner component
    │   ├── App.jsx            # Main app component
    │   ├── main.jsx          # React entry point
    │   ├── sockets.js        # WebSocket connection
    │   └── index.css         # Global styles
    ├── package.json          # Node.js dependencies
    ├── tailwind.config.js    # Tailwind configuration
    ├── env.example          # Environment variables template
    └── README.md            # Frontend documentation


## 🚀 Quick Start

### Prerequisites

- *Backend*: Python 3.8+, Twilio account (optional)
- *Frontend*: Node.js 16+, npm or yarn

### Backend Setup

1. Navigate to backend directory:
   bash
   cd tideguard-backend
   

2. Create virtual environment:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   

3. Install dependencies:
   bash
   pip install -r requirements.txt
   

4. Set up environment variables:
   bash
   cp env.example .env
   # Edit .env with your Twilio credentials (optional)
   

5. Run the backend:
   bash
   python app.py
   

Backend will start on http://localhost:5000

### Frontend Setup

1. Navigate to frontend directory:
   bash
   cd tideguard-frontend
   

2. Install dependencies:
   bash
   npm install
   

3. Set up environment variables:
   bash
   cp env.example .env
   # Edit .env with your backend URL
   

4. Run the frontend:
   bash
   npm run dev
   

Frontend will start on http://localhost:3000

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SECRET_KEY | Flask secret key | Yes |
| TWILIO_ACCOUNT_SID | Twilio Account SID | No |
| TWILIO_AUTH_TOKEN | Twilio Auth Token | No |
| TWILIO_PHONE_NUMBER | Twilio phone number | No |
| ALERT_PHONE_NUMBER | Phone number for alerts | No |

### Frontend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| VITE_BACKEND_URL | Backend server URL | Yes |

## 📊 Data Flow

1. *Data Generation*: Backend simulates weather data every 5 seconds
2. *Threshold Check*: Backend checks if wind speed > 80 km/h OR wave height > 4m
3. *SMS Alert*: If thresholds breached, sends SMS via Twilio
4. *WebSocket Broadcast*: Backend broadcasts data to all connected clients
5. *Frontend Update*: Frontend receives data and updates UI
6. *Alert Display*: Frontend shows alert banner if thresholds breached

## 🚨 Alert System

### Thresholds
- *Wind Speed*: > 80 km/h
- *Wave Height*: > 4 meters

### Alert Types
- *Warning*: Single threshold breached
- *Critical*: Both thresholds breached
- *SMS Notification*: Sent to configured phone number
- *Visual Alert*: Red banner appears on frontend

## 🚀 Deployment

### Backend (Render)

1. Create new Web Service on Render
2. Connect your GitHub repository
3. Set build command: pip install -r requirements.txt
4. Set start command: python app.py
5. Add environment variables in Render dashboard

### Frontend (Vercel)

1. Install Vercel CLI: npm i -g vercel
2. Deploy: vercel
3. Set environment variables in Vercel dashboard

## 🛠 Development

### Backend Development
- Flask with Flask-SocketIO for WebSocket support
- Python-dotenv for environment management
- Twilio for SMS notifications
- Realistic data simulation with tidal patterns

### Frontend Development
- React 18 with hooks
- Vite for fast development
- Tailwind CSS for styling
- Socket.IO client for real-time communication
- Lucide React for icons

## 📱 Features

### Real-time Monitoring
- Live weather data updates every 5 seconds
- Connection status indicators
- Automatic reconnection handling

### Visual Alerts
- Prominent alert banner for dangerous conditions
- Color-coded status indicators
- Dismissible alerts with cooldown

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interface

## 🔒 Security

- Environment variables for sensitive data
- CORS configuration for cross-origin requests
- Input validation and sanitization
- Secure WebSocket connections

## 📈 Monitoring

- Health check endpoint (/health)
- Connection status tracking
- Error logging and handling
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the individual README files in each directory
- Review the deployment guides
- Test the health endpoints

---

*TideGuard Alerter* - Keeping coastal communities safe with real-time weather monitoring.
