# Version 11.0.0

## Dockers
Dockerfiles and docker-compose have been added start prod enviroment and running tests.
### Prod

Dockerfile-prod has been added
docker-compose command prod has been added that start the production enviroment together with a mysql server.

### Test
Dockerfile-test has been added
docker-compose command test has been added that run the `make test` command on the production enviroment and shutdown after the test has been completed. 