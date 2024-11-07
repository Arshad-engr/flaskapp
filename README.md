# flaskapp
## Table of Contents
   - [Installation](#installation)
   - [Docker](#docker)

## Installation
  Follow these steps to set up the application local machine
  ### 1. Clone the repository:

   To get started, clone this repository to your local machine:

     
        git clone https://github.com/Arshad-engr/flaskapp.git

        

  ### 2. Set up a Virtual Environment

  To setup the project on local machine, run below command to create virtual environment 
  **For Linux/macOS**

        
            python3 -m venv venv
            source venv/bin/activate

        

  **For window OS**

     
        python -m venv venv
        venv\Scripts\activate
     

  ### 3. Install project dependencies
   Install all project necessary dependencies by running below command

     
     pip install -r > requirments.txt

     

  ### 4. Initilize Database
   To initlize your SQlite database, run below commands. I used SQLite database with **SQLAlchemy** and **Flask-migrate** packages

     
     flask db init
     flask db migrate
     flask db upgrade
     
## Docker
   If you have docker installed in your machine and don't to go with manuall installation, follow these steps to containerize your application
   ```
   docker-compose up --build

   ``` 


