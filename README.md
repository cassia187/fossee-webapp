# FOSSEE WebApp

A full-stack data analysis and visualization platform with dual frontend support (PyQt5 desktop and React web). Upload CSV datasets, visualize data through interactive charts, and generate comprehensive PDF reports. Created to solve the FOSSEE 2026 semester-long internship screening task.

## Try it at: https://test.komisan.dev

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **User Authentication**: Secure registration, login, and token-based authentication
- **Dataset Management**: Upload, view, and delete CSV datasets
- **Data Visualization**: 
  - Interactive charts (bar, pie, scatter, histogram)
  - Type distribution analysis
  - Equipment-specific visualizations
- **Report Generation**: Export comprehensive PDF reports of your data analysis
- **Dual Frontend**: Choose between desktop (PyQt5) or web (React) interface
- **RESTful API**: Complete Django REST Framework backend

## 🛠 Tech Stack

**Backend:**
- Django 4.2.28
- Django REST Framework 3.16.1
- SQLite (default database)
- ReportLab (PDF generation)
- Pandas & NumPy (data processing)

**Web Frontend:**
- React 19.2.0
- Vite 7.3.1
- Chart.js 4.5.1
- Axios (API communication)
- React Router DOM

**Desktop Frontend:**
- PyQt5 5.15.9
- Matplotlib 3.9.4

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher
- **pip**: Latest version
- **Git**: For cloning the repository

### Optional:
- **Virtual environment tool**: `venv` (comes with Python) or `virtualenv`

## 📁 Project Structure

```
fossee-webapp-main/
├── backend/
│   ├── api/                 # Main Django project settings
│   ├── core/                # Core app with models, views, serializers
│   │   └── migrations/      # Database migrations
│   ├── rest_demo/           # Additional REST configurations
│   └── manage.py            # Django management script
├── desktop-frontend/
│   ├── api/                 # API client for desktop app
│   └── gui/                 # PyQt5 GUI components
│       ├── dashboard.py     # Main dashboard
│       ├── login.py         # Login screen
│       ├── signup.py        # Registration screen
│       ├── data_visualizer.py
│       └── svg/             # Assets
├── web-frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   └── charts/      # Chart components
│   │   ├── pages/           # Page components
│   │   └── services/        # API services
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── requirements.txt         # Python dependencies
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/cassia187/fossee-webapp.git
cd fossee-webapp-main
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

**On Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r ../requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

### 3. Web Frontend Setup (Optional)

If you want to use the React web interface:

```bash
cd ../web-frontend
npm install
```

### 4. Desktop Frontend Setup (Optional)

The desktop frontend dependencies are already included in `requirements.txt`, so no additional setup is needed if you've installed the backend requirements.

## 💻 Usage

### Running the Backend Server

From the `backend` directory with your virtual environment activated:

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

Admin panel: `http://localhost:8000/admin/`

### Running the Web Frontend

From the `web-frontend` directory:

```bash
npm run dev
```

Access the application at: `http://localhost:5173`

### Running the Desktop Frontend

From the `desktop-frontend` directory:

```bash
python -m gui.main
```

### Running Both Frontends Simultaneously

1. Open **three** terminal windows
2. **Terminal 1** - Start the backend:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python manage.py runserver
   ```
3. **Terminal 2** - Start the web frontend:
   ```bash
   cd web-frontend
   npm run dev
   ```
4. **Terminal 3** - Start the desktop frontend:
   ```bash
   cd desktop-frontend
   python -m gui.main
   ```

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| POST | `/api/register/` | Register a new user | No |
| POST | `/api/login/` | Login and receive token | No |
| POST | `/api/logout/` | Logout and invalidate token | Yes |
| GET | `/api/profile/` | Get current user profile | Yes |

### Dataset Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/api/health_check/` | API health check | No |
| POST | `/api/upload/` | Upload CSV dataset | Yes |
| GET | `/api/datasets/` | List all user datasets | Yes |
| GET | `/api/datasets/<dataset_id>/` | Get dataset details | Yes |
| DELETE | `/api/datasets/<dataset_id>/delete/` | Delete a dataset | Yes |
| GET | `/api/datasets/<dataset_id>/type_distribution/` | Get data type distribution | Yes |
| GET | `/api/datasets/<dataset_id>/report/` | Generate PDF report | Yes |
| GET | `/api/datasets/<dataset_id>/raw/` | Get raw CSV data (for React) | Yes |

### Request Examples

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

**Upload CSV (with authentication token):**
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Token <your-token-here>" \
  -F "file=@/path/to/your/dataset.csv"
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use

**Problem**: `Error: That port is already in use.`

**Solutions**:
- **Django** (port 8000):
  ```bash
  # Find and kill the process
  lsof -ti:8000 | xargs kill -9  # Linux/macOS
  netstat -ano | findstr :8000   # Windows - note the PID, then:
  taskkill /PID <PID> /F         # Windows
  
  # Or run on a different port
  python manage.py runserver 8001
  ```

- **React** (port 5173):
  ```bash
  # Vite will usually auto-increment to 5174
  # Or specify a different port
  npm run dev -- --port 3000
  ```

#### Migration Errors

**Problem**: `No migrations to apply` or migration conflicts

**Solution**:
```bash
# Reset migrations (WARNING: This deletes data)
python manage.py migrate core zero
rm -rf core/migrations/
python manage.py makemigrations core
python manage.py migrate
```

#### CORS Issues

**Problem**: Frontend can't connect to backend

**Solution**: Check `backend/api/settings.py` for CORS settings:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

#### Module Not Found Errors

**Problem**: `ModuleNotFoundError: No module named 'X'`

**Solutions**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt

# For PyQt5 issues on Linux, you may need:
sudo apt-get install python3-pyqt5
```

#### npm Install Failures

**Problem**: Errors during `npm install`

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, try with legacy peer deps
npm install --legacy-peer-deps
```

#### PyQt5 Display Issues

**Problem**: Desktop app window doesn't appear or crashes

**Solutions**:
```bash
# Linux: Install Qt5 dependencies
sudo apt-get install qt5-default

# macOS: May need to allow Python in System Preferences
# Windows: Ensure Visual C++ Redistributables are installed
```

### Database Issues

**Reset the database completely:**
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Default Ports:**
- Django Backend: `http://localhost:8000`
- React Frontend: `http://localhost:5173`
- Django Admin: `http://localhost:8000/admin/`

**Database:** SQLite (db.sqlite3)
