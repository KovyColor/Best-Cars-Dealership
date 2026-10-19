# Best Cars Dealership

Best Cars Dealership is a full-stack vehicle marketplace for browsing makes and
models, locating dealerships, reading reviews, and registering customers.

## Technology stack

- React and Axios for the frontend
- Django and Django REST-style JSON views for the backend
- Node.js tooling for frontend development
- Express-compatible service integration points for dealership data
- MongoDB-compatible dealership/review service integration (the starter
  implementation includes a deterministic local mock)
- IBM Cloud Code Engine for deployment

## Project layout

```text
server/
  djangoproj/       Django project configuration
  djangoapp/        Models, views, and API routes
  frontend/
    static/         About, Contact, CSS, and image assets
    src/components/ React components
submission_files/   Capstone endpoint evidence
```

## Local setup

1. Create and activate a Python virtual environment.
2. Install Django:

   ```powershell
   python -m pip install django
   ```

3. From the repository root, create the database and start Django:

   ```powershell
   python server\manage.py migrate
   python server\manage.py runserver 8000
   ```

4. Open `http://127.0.0.1:8000/static/About.html` or use the React
   application configured by the course starter.

The JSON API is available under `/djangoapp/`. For production, replace the
local dealership adapter in `server/djangoapp/views.py` with the deployed
dealership/review service and configure the IBM Code Engine environment
variables for its URL.

## API examples

```powershell
curl http://127.0.0.1:8000/djangoapp/get_cars
curl http://127.0.0.1:8000/fetchDealers/Kansas
curl http://127.0.0.1:8000/fetchDealer/15
```

## CI

The GitHub Actions workflow runs `flake8 --max-line-length=120` against Python
sources and `jshint` against JavaScript/JSX sources.
