FROM rust:latest AS builder

WORKDIR /app

COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
ENV SQLX_OFFLINE=true

RUN --mount=type=cache,target=/usr/local/cargo/registry \
    cargo build --release

COPY src ./src
COPY migrations ./migrations
COPY .sqlx ./.sqlx

RUN --mount=type=cache,target=/usr/local/cargo/registry <<EOF
  set -e
  touch src/main.rs
  cargo build --release
EOF

FROM debian:bookworm-slim AS app

RUN apt-get update && apt-get install -y \
  libssl-dev \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/target/release/catalog_service .
COPY --from=builder /app/migrations ./migrations

EXPOSE 8001

CMD ["./catalog_service"]

