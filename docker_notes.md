docker ps //list of all the running containers
docker ps -a //list of all the containers
docker containe run <container name> //run a container
docker -exec -it <container id> bash //get inside a container

Docker notes

1) Create a docker file
2) Create a docker compose

3) docker-compose up --build : This command will rebuild the Docker image, ensuring that any changes in the requirements.txt file are applied during the build process
4) docker-compose down / docker-compose up --build : Cleanup and Restart:

For debugging in vscode
docker-compose build
docker-compose run -p 4000:4000 -p 8000:8000 --rm web sh -c 'RUN_IN_DOCKER=True python manage.py runserver --noreload --nothreading 0.0.0.0:8000'
and after this
attach debugger 
follow (https://medium.com/djangotube/dajngo-docker-compose-with-postgres-and-vs-code-debug-example-4875c6666674)