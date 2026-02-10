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

## Requirements
- Python 3.10+
- MySQL server
- pip (Python package manager)

## Installation
1. Clone the repository:
```bash
git clone <repo-url>
cd online-library
```

2. Create a virtual environment
```bash
python -m venv venv
```

3. Activate the environment
- Windows PowerShell:
```bash
source venv/Scripts/activate
```
- Linux/macOS:
```bash
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r backend/requirements.txt
```

5. Setup the database

**Option A**: MySQL Workbench (GUI)
If you prefer a visual interface, follow these steps:
- **Connect**: Open MySQL Workbench and connect to your local instance using your credentials (e.g., root).
- **Create Schema**: Run the following command in a new query tab:
	```sql
	CREATE DATABASE online_library;
	```
- **Initialize Tables**: Open the file *backend/db/init.sql* and execute the entire script to generate the required tables.
- **Populate Data**: Open *backend/db/data.sql* and execute it to load the sample data.

**Option B**: Command Line (CLI)
For those who like to stay in the terminal, run these commands from the root of the project:
- **Connect**: Open MySQL Workbench and connect to your local instance using your credentials (e.g., root).
- **Create Schema**: Run the following command in a new query tab:
	```sql
	CREATE DATABASE online_library;
	```
*run the following commands from project root*:
- Initialize tables:
```bash
mysql -u <user> -p online_library < backend/db/init.sql
```

- Populate with sample data:
```sql
# mysql -u <user> -p online_library < backend/db/data.sql
```

[!IMPORTANT] Replace ```<user>``` with your MySQL username. After running the command, you will be prompted to enter your password due to the ```-p``` flag.

6. Run the Flask server:
```bash
python backend/app.py
```

7. Open the site in a browser at http://127.0.0.1:5000/

## Notes
- Make sure the virtual environment is activated whenever you work on the project.
- Dependencies are installed only in the virtual environment.
