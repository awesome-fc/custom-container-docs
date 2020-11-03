FROM openjdk:8-jdk-alpine

# Install maven
RUN apk add maven && mkdir /workspace

COPY ./src /workspace/src
COPY ./pom.xml /workspace/

# Install packages and build jar with maven
RUN cd /workspace && mvn package

WORKDIR /workspace
EXPOSE 8080

# Starts the Spring Boot http server
ENTRYPOINT ["java", "-jar", "/workspace/target/gs-spring-boot-docker-0.1.0.jar"]
