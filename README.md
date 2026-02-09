# Online Library Project

## Overview
This project is an online library web application. Users can browse content, track reading progress, bookmark items, and leave reviews. Admins can manage content and moderate reviews.  
It follows a **three-tier architecture**: frontend (client), backend (server), and database.

## Technologies
- **Backend**: Python + Flask  
- **Frontend**: HTML, CSS (with Bootstrap), JavaScript  
- **Database**: MySQL (SQL scripts, triggers, routines)  
- **Testing**: Python unittest or pytest  
- **Tools**: Git, OBS Studio (for demo recording)

## Frontend Styling
- Uses **Bootstrap 5** via CDN for responsive layouts and components  
- `main.css` contains custom styles for branding or overrides  

## Installation
1. Clone the repository:
```bash
git clone <repo-url>
cd online-library
```
2. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```
3. Create the MySQL database and populate:
```sql
# run backend/db/init.sql and backend/db/data.sql
```
4. Run the Flask server:
```bash
python backend/app.py
```
5. Open the site in a browser at http://127.0.0.1:5000/
