import React, { useState, useEffect } from 'react';
import { AlertTriangle, X, Bell } from 'lucide-react';

const AlertBanner = ({ weatherData, isVisible }) => {
  const [isDismissed, setIsDismissed] = useState(false);
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    if (weatherData && weatherData.alert_active && !isDismissed) {
      setShowBanner(true);
    } else {
      setShowBanner(false);
    }
  }, [weatherData, isDismissed]);

  const handleDismiss = () => {
    setIsDismissed(true);
    setShowBanner(false);
  };

  const getAlertMessage = () => {
    if (!weatherData) return '';
    
    const windBreached = weatherData.wind_speed > 80;
    const waveBreached = weatherData.wave_height > 4;
    
    if (windBreached && waveBreached) {
      return `DANGER: High winds (${weatherData.wind_speed} km/h) and large waves (${weatherData.wave_height}m) detected!`;
    } else if (windBreached) {
      return `WARNING: High wind speed detected (${weatherData.wind_speed} km/h)!`;
    } else if (waveBreached) {
      return `WARNING: Large waves detected (${weatherData.wave_height}m)!`;
    }
    
    return '';
  };

  const getAlertLevel = () => {
    if (!weatherData) return 'info';
    
    const windBreached = weatherData.wind_speed > 80;
    const waveBreached = weatherData.wave_height > 4;
    
    if (windBreached && waveBreached) {
      return 'critical';
    } else if (windBreached || waveBreached) {
      return 'warning';
    }
    
    return 'info';
  };

  if (!showBanner || !isVisible) {
    return null;
  }

  const alertLevel = getAlertLevel();
  const alertMessage = getAlertMessage();

  const getAlertStyles = () => {
    switch (alertLevel) {
      case 'critical':
        return {
          container: 'bg-red-600 border-red-700',
          text: 'text-white',
          icon: 'text-red-200',
          button: 'text-red-200 hover:text-white hover:bg-red-700'
        };
      case 'warning':
        return {
          container: 'bg-yellow-600 border-yellow-700',
          text: 'text-white',
          icon: 'text-yellow-200',
          button: 'text-yellow-200 hover:text-white hover:bg-yellow-700'
        };
      default:
        return {
          container: 'bg-blue-600 border-blue-700',
          text: 'text-white',
          icon: 'text-blue-200',
          button: 'text-blue-200 hover:text-white hover:bg-blue-700'
        };
    }
  };

  const styles = getAlertStyles();

  return (
    <div className={`fixed top-0 left-0 right-0 z-50 border-b ${styles.container} animate-bounce-slow`}>
      <div className="max-w-7xl mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <div className={`flex-shrink-0 ${styles.icon}`}>
              {alertLevel === 'critical' ? (
                <AlertTriangle className="h-6 w-6 animate-pulse" />
              ) : (
                <Bell className="h-6 w-6 animate-pulse" />
              )}
            </div>
            <div className="ml-3">
              <p className={`text-sm font-medium ${styles.text}`}>
                {alertMessage}
              </p>
              <p className={`text-xs ${styles.icon} mt-1`}>
                SMS alert sent • Take immediate action
              </p>
            </div>
          </div>
          <div className="flex-shrink-0">
            <button
              onClick={handleDismiss}
              className={`inline-flex items-center justify-center p-1 rounded-md ${styles.button} transition-colors duration-200`}
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
      
      {/* Pulsing border effect */}
      <div className={`absolute bottom-0 left-0 right-0 h-1 ${styles.container} animate-pulse-slow`}></div>
    </div>
  );
};

export default AlertBanner;
