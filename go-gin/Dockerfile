FROM golang:alpine3.13 AS builder

RUN apk update && apk add alpine-sdk git && rm -rf /var/cache/apk/*

# Create app directory
WORKDIR /usr/src/app

# Copy app dependencies
COPY go.mod .
COPY go.sum .
RUN go mod download

# Build executable binary
COPY server.go .
RUN go build -o ./server ./server.go

FROM alpine:latest

# Get CA certs for networking
RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*

# Create app directory
WORKDIR /usr/src/app

# Copy static executable
COPY --from=builder /usr/src/app/server .

# Run the server binary
EXPOSE 9000
ENTRYPOINT ["./server"]
