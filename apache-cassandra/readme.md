# To run the Cassandra docker container

## Build your Docker image

`docker build -t my-cassandra-image .`

## Run your Docker container

`docker run --name my-cassandra-container -p 9042:9042 -d my-cassandra-image`
