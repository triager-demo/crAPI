FROM golang:1.21-bookworm AS builder
WORKDIR /app

COPY go.* ./
RUN go mod download

COPY . ./

# Build the binary.
RUN go build -v -o server

RUN openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
    -keyout private.key -out public.crt -subj "/CN=api.mypremiumdealership.com" \
    -addext "subjectAltName=IP:127.0.0.1,DNS:gateway-service,DNS:api.mypremiumdealership.com,DNS:mypremiumdealership.com"

FROM debian:bookworm-slim
SHELL ["/bin/bash", "-c"]
WORKDIR /app

RUN set -x && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy the binary to the production image from the builder stage.
COPY --from=builder /app/server /app/server
COPY --from=builder /app/public.crt /app/server.crt
COPY --from=builder /app/private.key /app/server.key

EXPOSE 443

CMD ["/app/server"]

