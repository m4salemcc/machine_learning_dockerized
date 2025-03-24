# Docker login with creds
docker login
# Tag the build to be able to push
docker tag random_forest_dockerized-flask-app m4salemcc/att-docker-repo:latest

#docker push 
docker push m4salemcc/att-docker-repo:latest

#docker pull 
docker pull m4salemcc/att-docker-repo:latest

#modify the docker compose file to run from registry