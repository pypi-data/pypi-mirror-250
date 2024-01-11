deps:
    cargo install cross

build-x86-linux-musl:
    RUSTFLAGS="-C target-feature=-crt-static" cross build --target x86_64-unknown-linux-musl --release

build-arm64-linux-musl:
    RUSTFLAGS="-C target-feature=-crt-static" cross build --target aarch64-unknown-linux-musl --release

build:
    cargo build --release

build-all: build-x86-linux-musl build-arm64-linux-musl build
