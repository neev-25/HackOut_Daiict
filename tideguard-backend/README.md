# TideGuard Backend

A Flask-based backend service for the TideGuard Alerter system that simulates weather and tide data, monitors thresholds, and sends SMS alerts via Twilio.

## Features

- 🌊 Real-time weather and tide data simulation
- 📱 SMS alerts via Twilio when thresholds are breached
- 🔌 WebSocket support for real-time client communication
- 🏥 Health check endpoint
- ⚡ Data updates every 5 seconds

## Thresholds

- **Wind Speed**: > 80 km/h
- **Wave Height**: > 4 meters

## Setup

### Prerequisites

- Python 3.8+
- Twilio account (for SMS alerts)

### Installation

1. Clone the repository
2. Navigate to the backend directory:
   ```bash
   cd tideguard-backend
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your actual values:
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `TWILIO_PHONE_NUMBER`: Your Twilio phone number
   - `ALERT_PHONE_NUMBER`: Phone number to receive alerts

### Running Locally

```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns server status

### WebSocket Events

- **connect**: Client connects to server
- **disconnect**: Client disconnects from server
- **request_data**: Client requests current data
- **weather_data**: Server broadcasts weather data (every 5 seconds)

## Data Format

The server broadcasts weather data in the following format:

```json
{
  "timestamp": 1640995200,
  "wind_speed": 45.2,
  "wave_height": 2.1,
  "weather_condition": "Partly Cloudy",
  "temperature": 18.5,
  "humidity": 75.2,
  "pressure": 1015.3,
  "alert_active": false
}
```

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Add environment variables in Render dashboard:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE_NUMBER`
   - `ALERT_PHONE_NUMBER`
   - `SECRET_KEY`

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID | No (for SMS) |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token | No (for SMS) |
| `TWILIO_PHONE_NUMBER` | Twilio phone number | No (for SMS) |
| `ALERT_PHONE_NUMBER` | Phone number for alerts | No (for SMS) |

## Development

The backend uses:
- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket support
- **Flask-CORS**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management
- **twilio**: SMS service integration

## License

MIT License
