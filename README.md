Initialize the project:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Create Django superuser for debug and maintainence:
```bash
python manage.py createsuperuser 
```
We may then go to "localhost:8000/admin/" to manage the Django Database (which is SQLite by default)

PyQt5 based Frontend:
```
cd desktop-frontend/
python -m gui.main
```

React based Frontend:
```
cd web-frontend/
npm install
npm run dev
```
Access the frontend at: `http://localhost:5173`

Django API Endpoints:

- POST /api/register/ - Register a new user
- POST /api/login/ - Login to get a token
- POST /api/logout/ - Logout and delete token
- GET /api/profile/ - Get user profile
- GET /api/health_check/ - Health check
- POST /api/upload - Upload CSV dataset
- GET /api/datasets/ - Get all datasets
- GET /api/datasets/<dataset_id>/ - Get dataset details
- DELETE /api/datasets/<dataset_id>/delete/ - Delete a dataset
- GET /api/datasets/<dataset_id>/type_distribution/ - Get type distribution
- GET /api/datasets/<dataset_id>/report/ - Generate PDF report
- GET /api/datasets/<dataset_id>/raw/ - Raw data from the csv for the React Frontend


