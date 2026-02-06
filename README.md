Initialize the project:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

API Endpoints:

- POST /api/register/ - Register a new user
- POST /api/login/ - Login to get a token
- POST /api/logout/ - Logout and delete token
- GET /api/profile/ - Get user profile
- GET /api/health-check/ - Health check
- POST /api/upload - Upload CSV dataset
- GET /api/datasets/ - Get all datasets
- GET /api/datasets/<dataset_id>/ - Get dataset details
- DELETE /api/datasets/<dataset_id>/delete/ - Delete a dataset
- GET /api/datasets/<dataset_id>/type_distribution/ - Get type distribution
- GET /api/datasets/<dataset_id>/report/ - Generate PDF report


