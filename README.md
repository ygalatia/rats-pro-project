# rats-pro-project
Rats Pro Project

## About
The project contains *Data Collation* application to collate two datasets of Rats Pro and create a new dataset with specific fields.

## Data Collation Application
The Data Collation application can be accessed through uri 'http://{base_path}:8000/collate'.

In the interface you will found three input:
1. Dataset 1: Dataset which contains personal identification of the clients (e.g, id, country, email)
2. Dataset 2: Dataset which contain the financial informations of the client (e.g, id, credit card type, bitcoin address)
3. Countries: Default value is Netherlands and UK

### How it works
After filling out the form and "Upload" button is clicked, it sends a POST request to the backend.

Then, after each field is validated, each dataset is loaded as a dataframe using Pandas. 

With pandas, several preprocessing such as filtering by country, removing private fields, and finally renaming all fields as required.

Then, dataset 2 will be left merged to dataset 1 using `merge` function on `id` field.

Finally, the output of these processes is stored as a csv file to the `client_data` folder in the root directory of the project.

### Clone then Run the project using docker
To run the project using docker:
1. Clone the project
2. In the project's root directory run
`docker build -t rats-pro-project .`
3. After command run succesfully, run the docker image
`docker run -p 8000:8000 rats-pro-project`
4. Access `http://127.0.0.1:8000/collate/` to access the UI

### Pull and Run Docker Images from DockerHub
To pull and run the project from DockerHub:
1. Run `docker run -p 8000:8000 yesayagm/rats-pro-project`
2. Access `http://127.0.0.1:8000/collate/` to access the UI

### Install and import Software Distribution Package
To install and import the sdist package:
1. Clone the project or download the sdis file on `https://github.com/ygalatia/rats-pro-project/blob/main/dist/datasets_collation-0.1.tar.gz`
2. Install the package using pip `pip install path/to/sdist/datasets_collation-0.1.tar.gz`
3. Import the package in the desired python file or project:
`import datasets_collation.views as dc` or `from datasets_collation.views import {module/function}`
