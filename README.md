**

## OSTicket API

OSTicket is an open source ticketing platform with all the mature functionalities for a ticketing system. Although the system does not expose certain API's as of yet to support interaction with an external application.

OSTicket API is a layer over the osticket database to interact with the osticket directly at the db level without messing with the PHP functionalities in any way. This project is currently supported for users who are trying to interact with OSTicket and who tend to create OSTicket users, organizations from a separate application outside the OSTicket domain.

***Code Navigation***

This project consists of a main folder `src` which contains all the project files. The files outside the source folder consists of `docker-compose.yml`, `Dockerfile` and a `local.env` file which are used for running the docker containers. The `src` folder contains the entrypoint of the Flask project `app.py`, `settings` folder which contains your application settings and an `apis` folder that stores all your urls and views. There is a `services` folder which currently has a user service and an organization service for creating of users and creation of organizations. The code is pretty straight forward and uses python api for mysql to directly connect to the osticket database. The service functions are simple mysql queries and are pretty straightforward. Any functionality that you need to add: "go through the logic of how the php code affects the database and write a simple sql query to do the same using python". For exposing the API write a simple url and views scheme and call the service function as essential.

***Installation***

Running the osticket-api app is very easy. First [install](https://docs.docker.com/install/) docker for your operating system from the docs provided in the docker website. Also [install](https://docs.docker.com/compose/install/) docker-compose

Then run

    sudo docker-compose build

and then

    sudo docker-compose up
  
This will run the server at port http://localhost:8085/

The docker-compose also uses the osticket image from [here](https://hub.docker.com/r/campbellsoftwaresolutions/osticket/)

It also runs a sql database server with some default credentials which can be changed in `local.env` file

***Queries***

For any queries:
Contact: arpitgoyal.iitkgp@gmail.com

Feel free to incorporate more basic features as you will and submit pull requests. I will be more than happy to incorporate those features.
