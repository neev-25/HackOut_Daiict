import React, { useState, useEffect } from 'react';
import { Wind, Waves, Thermometer, Droplets, Gauge, Cloud } from 'lucide-react';
import socketManager from '../sockets.js';

const Dashboard = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    // Connect to WebSocket
    const socket = socketManager.connect();
    
    // Listen for connection status
    const handleConnect = () => {
      setIsConnected(true);
      console.log('Connected to backend');
    };

    const handleDisconnect = () => {
      setIsConnected(false);
      console.log('Disconnected from backend');
    };

    // Listen for weather data updates
    const handleWeatherData = (data) => {
      setWeatherData(data);
      setLastUpdate(new Date());
      console.log('Received weather data:', data);
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

  const getStatusColor = (value, threshold, type) => {
    if (type === 'wind_speed') {
      if (value > 80) return 'border-red-500 bg-red-50';
      if (value > 60) return 'border-yellow-500 bg-yellow-50';
      return 'border-green-500 bg-green-50';
    }
    if (type === 'wave_height') {
      if (value > 4) return 'border-red-500 bg-red-50';
      if (value > 2.5) return 'border-yellow-500 bg-yellow-50';
      return 'border-green-500 bg-green-50';
    }
    return 'border-blue-500 bg-blue-50';
  };

  const getStatusIndicator = (value, threshold, type) => {
    if (type === 'wind_speed') {
      if (value > 80) return 'status-danger';
      if (value > 60) return 'status-warning';
      return 'status-safe';
    }
    if (type === 'wave_height') {
      if (value > 4) return 'status-danger';
      if (value > 2.5) return 'status-warning';
      return 'status-safe';
    }
    return 'status-safe';
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return 'Never';
    return new Date(timestamp * 1000).toLocaleTimeString();
  };

  if (!weatherData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ocean-blue mx-auto mb-4"></div>
          <p className="text-gray-600">Connecting to TideGuard Backend...</p>
          <div className={`mt-2 inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
            isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            <div className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            {isConnected ? 'Connected' : 'Disconnected'}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">TideGuard Alerter</h1>
          <p className="text-gray-600">Real-time coastal weather monitoring</p>
          
          {/* Connection Status */}
          <div className="mt-4 flex items-center justify-center space-x-4">
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
              isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            }`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              {isConnected ? 'Connected' : 'Disconnected'}
            </div>
            <span className="text-sm text-gray-500">
              Last update: {lastUpdate ? lastUpdate.toLocaleTimeString() : 'Never'}
            </span>
          </div>
        </div>

        {/* Main Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* Wind Speed */}
          <div className={`metric-card ${getStatusColor(weatherData.wind_speed, 80, 'wind_speed')}`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Wind className="w-6 h-6 text-gray-600 mr-2" />
                <span className="metric-label">Wind Speed</span>
              </div>
              <div className={`status-indicator ${getStatusIndicator(weatherData.wind_speed, 80, 'wind_speed')}`}></div>
            </div>
            <div className="metric-value">{weatherData.wind_speed} km/h</div>
            <div className="text-sm text-gray-500 mt-2">
              Threshold: 80 km/h
            </div>
          </div>

          {/* Wave Height */}
          <div className={`metric-card ${getStatusColor(weatherData.wave_height, 4, 'wave_height')}`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Waves className="w-6 h-6 text-gray-600 mr-2" />
                <span className="metric-label">Wave Height</span>
              </div>
              <div className={`status-indicator ${getStatusIndicator(weatherData.wave_height, 4, 'wave_height')}`}></div>
            </div>
            <div className="metric-value">{weatherData.wave_height} m</div>
            <div className="text-sm text-gray-500 mt-2">
              Threshold: 4.0 m
            </div>
          </div>

          {/* Weather Condition */}
          <div className="metric-card border-blue-500 bg-blue-50">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Cloud className="w-6 h-6 text-gray-600 mr-2" />
                <span className="metric-label">Weather</span>
              </div>
              <div className="status-indicator status-safe"></div>
            </div>
            <div className="metric-value">{weatherData.weather_condition}</div>
            <div className="text-sm text-gray-500 mt-2">
              Current conditions
            </div>
          </div>

          {/* Temperature */}
          <div className="metric-card border-blue-500 bg-blue-50">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Thermometer className="w-6 h-6 text-gray-600 mr-2" />
                <span className="metric-label">Temperature</span>
              </div>
              <div className="status-indicator status-safe"></div>
            </div>
            <div className="metric-value">{weatherData.temperature}°C</div>
            <div className="text-sm text-gray-500 mt-2">
              Air temperature
            </div>
          </div>

          {/* Humidity */}
          <div className="metric-card border-blue-500 bg-blue-50">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Droplets className="w-6 h-6 text-gray-600 mr-2" />
                <span className="metric-label">Humidity</span>
              </div>
              <div className="status-indicator status-safe"></div>
            </div>
            <div className="metric-value">{weatherData.humidity}%</div>
            <div className="text-sm text-gray-500 mt-2">
              Relative humidity
            </div>
          </div>

          {/* Pressure */}
          <div className="metric-card border-blue-500 bg-blue-50">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Gauge className="w-6 h-6 text-gray-600 mr-2" />
                <span className="metric-label">Pressure</span>
              </div>
              <div className="status-indicator status-safe"></div>
            </div>
            <div className="metric-value">{weatherData.pressure} hPa</div>
            <div className="text-sm text-gray-500 mt-2">
              Atmospheric pressure
            </div>
          </div>
        </div>

        {/* Additional Info */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-600">Data Timestamp:</span>
              <span className="ml-2 text-gray-900">{formatTime(weatherData.timestamp)}</span>
            </div>
            <div>
              <span className="font-medium text-gray-600">Alert Status:</span>
              <span className={`ml-2 font-medium ${weatherData.alert_active ? 'text-red-600' : 'text-green-600'}`}>
                {weatherData.alert_active ? 'ACTIVE' : 'Normal'}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-600">Connection:</span>
              <span className={`ml-2 font-medium ${isConnected ? 'text-green-600' : 'text-red-600'}`}>
                {isConnected ? 'Live' : 'Offline'}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-600">Update Frequency:</span>
              <span className="ml-2 text-gray-900">Every 5 seconds</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
