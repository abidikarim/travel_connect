# TravelConnect

TravelConnect is an application designed to help users share trips and connect with others. This repository contains the source code and related resources for the project.

## Environment Prerequisites

Before running the application, ensure your environment meets the following requirements:

1. **Python Version**:
   - Python 3.9 or higher is required for compatibility.
   - You can download Python from the [official Python website](https://www.python.org/downloads/).

   **Note**: FastAPI code syntax may vary depending on the Python version. Make sure to match your version with the project's requirements.

2. **Additional Tools**:
   - [Git](https://git-scm.com/) for version control.
   - A virtual environment manager such as `venv` or `virtualenv` (included with Python).

## Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone  git@github.com:abidikarim/travel_connect.git
   cd travel_connect
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/MacOS
   venv\Scripts\activate    # On Windows
   ```

3. **Install Dependencies**:
   - Use `pip` to install the required packages listed in the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
   - This will start the FastAPI application on `http://127.0.0.1:8000`.
