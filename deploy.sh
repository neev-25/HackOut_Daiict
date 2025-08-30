#!/bin/bash

echo "🌊 TideGuard Alerter Deployment Script"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    
    print_status "All requirements met ✓"
}

# Deploy backend
deploy_backend() {
    print_status "Deploying backend..."
    
    cd tideguard-backend
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Please create one from env.example"
        cp env.example .env
        print_status "Created .env file from template. Please edit with your settings."
    fi
    
    # Test the backend
    print_status "Testing backend..."
    python -c "import app; print('Backend test successful')" 2>/dev/null || {
        print_error "Backend test failed"
        exit 1
    }
    
    print_status "Backend ready for deployment ✓"
    cd ..
}

# Deploy frontend
deploy_frontend() {
    print_status "Deploying frontend..."
    
    cd tideguard-frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Please create one from env.example"
        cp env.example .env
        print_status "Created .env file from template. Please edit with your settings."
    fi
    
    # Build the project
    print_status "Building frontend..."
    npm run build
    
    if [ $? -eq 0 ]; then
        print_status "Frontend build successful ✓"
    else
        print_error "Frontend build failed"
        exit 1
    fi
    
    cd ..
}

# Start development servers
start_dev() {
    print_status "Starting development servers..."
    
    # Start backend in background
    cd tideguard-backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend
    cd tideguard-frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_status "Development servers started:"
    print_status "Backend: http://localhost:5000"
    print_status "Frontend: http://localhost:3000"
    print_status "Press Ctrl+C to stop servers"
    
    # Wait for interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
}

# Main menu
main() {
    echo ""
    echo "Choose an option:"
    echo "1) Deploy both backend and frontend"
    echo "2) Deploy backend only"
    echo "3) Deploy frontend only"
    echo "4) Start development servers"
    echo "5) Exit"
    echo ""
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            check_requirements
            deploy_backend
            deploy_frontend
            print_status "Deployment complete! ✓"
            ;;
        2)
            check_requirements
            deploy_backend
            ;;
        3)
            check_requirements
            deploy_frontend
            ;;
        4)
            check_requirements
            deploy_backend
            deploy_frontend
            start_dev
            ;;
        5)
            print_status "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac
}

# Run main function
main
