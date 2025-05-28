# Vehicle Assignment Suggestion API 

This is a FastAPI backend that allows adding vehicle data and suggesting optimal vehicle assignments for passenger trips based on capacity, range, fuel type, and profitability. It's built using **FastAPI**, **SQLAlchemy**, and **SQLite**.

---

##  Features

- Add and retrieve vehicle entries
- Suggest vehicle combinations for trips
- Profit estimation based on distance and fuel type
- SQLite database for easy setup

---

##  Project Structure
```
project/
│
├── main/
│   ├── crud/
│   │   └── vehicle.py         # Business logic for vehicle handling
│   ├── models/
│   │   └── vehicle.py         # SQLAlchemy ORM model
│   ├── schemas/
│   │   └── vehicle.py         # Pydantic schemas
│   ├── database.py            # Database setup and session management
│   ├── main.py                # FastAPI application
│   └── vehicles.db            # SQLite database (auto-created)
│
└── README.md                  # You're reading it!
```
---

## Requirements

- Python 3.8+
- https://pip.pypa.io/en/stable/
- Optional: https://docs.python.org/3/library/venv.html

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name/main
```

### 2. Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Install the dependencies

```
pip install -r reqirements.txt
```
---
##  Running the App
```
uvicorn main:app --reload
```

The API will be available at: http://127.0.0.1:8000

Interactive docs: http://127.0.0.1:8000/docs

Alternate docs: http://127.0.0.1:8000/redoc

---
# API Endpoints
## Add a vehicle

### POST /vehicles/
Request body:

```
{
  "passengerCapacity": 4,
  "range": 300,
  "fuelType": "gasoline"
}
```

### fuleType can be : gasoline | mildHybrid | pureElectric 

##  List all vehicles

### GET /vehicles

Returns a list of all vehicles in the database.

### GET /suggestions/

Returns a list of suitable vehicle combinations with estimated profit, travel fee, and refueling costs.

## Query parameters:

    passengers (int): number of passengers

    distance (float): trip distance in kilometers

---

## Notes

    On first run, the vehicles.db file is automatically created in the main/ directory.

    The project uses SQLite for simplicity. You can switch to PostgreSQL or MySQL if needed by modifying SQLALCHEMY_DATABASE_URL in database.py.

###  License
    MIT
### Author
    Akos Farago
