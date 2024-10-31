# Movie Tracker

## Setup Instructions

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
2. **Create Database**
   ```bash
   python3 -m scripts.createDB
   ```
3. **Run Migrations for authentication**
   ```bash
   python3 manage.py migrate
   ```
4. **Insert Initial Data**
   ```bash
   python3 -m scripts.insertData
   ```
5. **Run the application**
   ```bash
   python3 manage.py runserver
   ```
6. Admin User credentials
   - Username: admin
   - Password: admin

## Important Notes

- Creating a movie may cause the application to become unresponsive while it fetches data for actors and genres due to high load
- Database settings can be found in MovieTracker/settings.py, and SQLAlchemy configurations are in utilities/sqlalchemy_setup.py.

### Improvements

- Make the movie creation process responsive by returning JSON responses or implementing a search feature for actors instead of a complete list.
- Enhance visual validations for better user experience.
- Improve overall user-friendliness of the interface
