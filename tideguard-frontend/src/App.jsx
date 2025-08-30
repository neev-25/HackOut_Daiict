import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard.jsx';
import AlertBanner from './components/AlertBanner.jsx';
import socketManager from './sockets.js';

function App() {
  const [weatherData, setWeatherData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Connect to WebSocket
    const socket = socketManager.connect();
    
    // Listen for connection status
    const handleConnect = () => {
      setIsConnected(true);
    };

    const handleDisconnect = () => {
      setIsConnected(false);
    };

    // Listen for weather data updates
    const handleWeatherData = (data) => {
      setWeatherData(data);
    };

    // Set up event listeners
    socket.on('connect', handleConnect);
    socket.on('disconnect', handleDisconnect);
    socket.on('weather_data', handleWeatherData);

    // Request initial data
    socket.emit('request_data');

    // Cleanup on unmount
    return () => {
      socket.off('connect', handleConnect);
      socket.off('disconnect', handleDisconnect);
      socket.off('weather_data', handleWeatherData);
    };
  }, []);

  return (
    <div className="App">
      <AlertBanner 
        weatherData={weatherData} 
        isVisible={isConnected} 
      />
      <Dashboard />
    </div>
  );
}

export default App;
