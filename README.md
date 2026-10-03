\# Product Sales Analytics System



A Python-based product sales analytics system that combines a CLI application with a FastAPI backend and MySQL database. The system processes sales data, provides authenticated API access, supports flexible filtering and analytics, and generates visualizations from analytical results.



\## Features



\- CSV-based sales data processing using Pandas

\- Data cleaning and preprocessing

\- MySQL database integration

\- FastAPI REST API

\- CLI-based user interface

\- User registration and login

\- Password hashing using bcrypt

\- JWT-based authentication

\- Role-based access control

\- Sales filtering, sorting, and pagination

\- Flexible analytical queries

\- Multiple aggregation metrics

\- Grouped analytics

\- Ranking-based analytics

\- Bar, line, and pie chart visualizations



\## Tech Stack



\- Python

\- FastAPI

\- Uvicorn

\- Pandas

\- MySQL

\- MySQL Connector/Python

\- Matplotlib

\- PyJWT

\- Passlib

\- bcrypt

\- Requests

\- python-dotenv



\## Project Architecture



CLI Application

&#x20;     |

&#x20;     | HTTP Requests

&#x20;     v

FastAPI Backend

&#x20;     |

&#x20;     +-- Authentication

&#x20;     +-- Authorization

&#x20;     +-- Sales Endpoints

&#x20;     +-- Analytics Endpoints

&#x20;     |

&#x20;     v

MySQL Database



The CLI communicates with the FastAPI backend using HTTP requests. The API handles authentication, validation, database queries, and analytics before returning results to the CLI.



\## Project Structure



Product\_Sales\_project/

|

+-- api/

|   +-- analytics.py

|   +-- auth.py

|   +-- constants.py

|   +-- database.py

|   +-- main.py

|   +-- models.py

|   +-- query\_builder.py

|   +-- sales.py

|   +-- security.py

|   +-- validation.py

|

+-- cli/

|   +-- api\_client.py

|   +-- display.py

|   +-- main.py

|   +-- menus.py

|   +-- visualizations.py

|

+-- Data/

|   +-- industry\_sales\_raw\_100k.csv

|   +-- industry\_sales\_cleaned\_100k.csv

|

+-- docs/

|   +-- API\_specifications\_v1.docx

|   +-- API\_specifications\_v2.docx

|   +-- visualizations\_plan.txt

|

+-- scripts/

|   +-- clean\_data.py

|   +-- explore\_data.py

|   +-- load\_to\_MySQL.py

|

+-- .env.example

+-- .gitignore

+-- requirements.txt

+-- README.md



\## Dataset



The project uses a sales dataset containing approximately 100,000 records.



The dataset contains fields including:



\- Customer ID

\- Customer name

\- Product

\- Category

\- Amount

\- City

\- Payment mode

\- Order status

\- Order date

\- Quantity

\- Customer type

\- Customer age

\- Gender

\- Rating

\- Sales channel



The raw dataset is cleaned and prepared before being loaded into MySQL.



\## Setup



\### 1. Clone the Repository



git clone https://github.com/YOUR\_USERNAME/product-sales-analytics.git

cd product-sales-analytics



Replace YOUR\_USERNAME with your GitHub username.



\### 2. Install Dependencies



Make sure Python is installed, then run:



python -m pip install -r requirements.txt



\### 3. Configure Environment Variables



Create a .env file in the project root.



Use .env.example as a template:



DB\_HOST=localhost

DB\_USER=root

DB\_PASSWORD=your\_mysql\_password

DB\_NAME=product\_sales\_db

JWT\_SECRET\_KEY=your\_jwt\_secret\_key



Do not commit the .env file to GitHub.



\### 4. Configure MySQL



Create a MySQL database named:



product\_sales\_db



The required database tables should be created before loading the sales data.



\### 5. Explore the Dataset



To inspect the dataset and perform exploratory analysis:



python scripts/explore\_data.py



\### 6. Clean the Dataset



Run:



python scripts/clean\_data.py



This prepares the raw sales data for database insertion and analysis.



\### 7. Load Data into MySQL



After configuring MySQL and cleaning the dataset:



python scripts/load\_to\_MySQL.py



This loads the cleaned sales data into the MySQL database.



\## Running the Application



\### Start the FastAPI Server



From the project root:



uvicorn api.main:app --reload



The API will run at:



http://127.0.0.1:8000



FastAPI's interactive API documentation can be accessed at:



http://127.0.0.1:8000/docs



\### Start the CLI



Open a separate terminal while the API server is running:



python -m cli.main



The CLI communicates with the FastAPI server and provides access to authentication, sales queries, analytics, and visualizations.



\## Authentication



The system uses:



\- Password hashing with bcrypt

\- JWT access tokens

\- OAuth2 password authentication

\- Role-based authorization



Users can register and authenticate through the API.



Authenticated requests use a Bearer token:



Authorization: Bearer <access\_token>



\## API Endpoints



\### Authentication



POST /register

POST /login



\### Sales



GET /sales



The sales endpoint supports filtering, sorting, and pagination.



\### Analytics



GET /analytics



The analytics endpoint supports metrics, grouping, and ranking operations.



\## Analytics



The system supports multiple analytical metrics, including:



total\_revenue

average\_order\_value

highest\_sale

lowest\_sale

total\_orders

total\_quantity\_sold

average\_quantity

distinct\_customers

average\_customer\_age

average\_rating

highest\_rating

lowest\_rating



Analytics can be grouped by fields such as:



product

category

city

payment\_mode

customer\_type

gender

sales\_channel

month

year



Ranking-based analysis is also supported for selected metrics.



\## Data Visualization



The CLI can generate visualizations from analytical results, including:



\- Bar charts

\- Line charts

\- Pie charts



Charts are generated dynamically based on the selected analytical query and grouping.



\## Security



Sensitive configuration values are stored in environment variables rather than directly in the source code.



The following file is intentionally excluded from version control:



.env



A safe configuration template is provided as:



.env.example



The JWT signing secret and database credentials are therefore not stored in the public source code.



\## Future Improvements



Possible future improvements include:



\- Web-based frontend

\- Cloud deployment

\- Automated testing

\- CI/CD pipeline

\- Improved logging and monitoring

\- Additional analytics and dashboards

\- Production database configuration

\- Extended API documentation



\## Author



Kunal Singh



B.Tech Computer Science \& Engineering

Jaypee Institute of Information Technology

