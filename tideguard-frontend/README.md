# TideGuard Frontend

A React-based frontend for the TideGuard Alerter system that displays real-time weather and tide data with live alerts.

## Features

- 🌊 Real-time weather and tide data display
- 🚨 Live alert banner when thresholds are breached
- 📱 Responsive design for all devices
- 🔌 WebSocket connection for live updates
- 🎨 Modern UI with Tailwind CSS
- ⚡ Data updates every 5 seconds

## Technologies

- **React 18** - Frontend framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling framework
- **Socket.IO Client** - Real-time communication
- **Lucide React** - Icon library

## Setup

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd tideguard-frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Set up environment variables:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` with your backend URL:
   - `VITE_BACKEND_URL`: Your backend server URL (default: http://localhost:5000)

### Running Locally

```bash
npm run dev
```

The application will start on `http://localhost:3000`

## Components

### Dashboard
The main dashboard displays:
- Wind speed with threshold monitoring
- Wave height with threshold monitoring
- Weather conditions
- Temperature, humidity, and pressure
- Connection status and system information

### AlertBanner
A prominent banner that appears when:
- Wind speed exceeds 80 km/h
- Wave height exceeds 4 meters
- Can be dismissed by the user

## Data Flow

1. **Connection**: Frontend connects to backend via WebSocket
2. **Data Reception**: Backend broadcasts weather data every 5 seconds
3. **Threshold Monitoring**: Frontend checks data against thresholds
4. **Alert Display**: Alert banner appears when thresholds are breached
5. **Real-time Updates**: UI updates automatically with new data

## Deployment to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Set environment variables in Vercel dashboard:
   - `VITE_BACKEND_URL`: Your deployed backend URL

### Manual Deployment

1. Build the project:
   ```bash
   npm run build
   ```

2. Deploy the `dist` folder to your hosting service

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_BACKEND_URL` | Backend server URL | Yes |

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Project Structure

```
src/
├── components/
│   ├── Dashboard.jsx      # Main dashboard component
│   └── AlertBanner.jsx    # Alert banner component
├── App.jsx                # Main app component
├── main.jsx              # React entry point
├── sockets.js            # WebSocket connection manager
└── index.css             # Global styles
```

## Styling

The application uses Tailwind CSS with custom:
- Color scheme (ocean-blue, storm-gray, alert-red, safe-green)
- Custom animations (pulse-slow, bounce-slow)
- Responsive design patterns
- Component-specific utility classes

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT License
