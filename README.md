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

### Run the project using docker (locally)
To run the project using docker:
1. Clone the project
2. In the project's root directory run
`docker build -t rats-pro-project .`
3. After command run succesfully, run the docker image
`docker run -p 8000:8000 rats-pro-project`
4. Access `http://127.0.0.1:8000/collate/` to access the UI
