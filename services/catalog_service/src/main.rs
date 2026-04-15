mod dto;
mod errors;
mod models;
mod router;
mod app_state;
mod handlers;
mod repository;

use std::sync::Arc;

use app_state::AppState;
use repository::PostgresRepository;

use sqlx::postgres::PgPoolOptions;
use tracing_subscriber::EnvFilter;

#[tokio::main]
async fn main() {
    dotenvy::dotenv().ok();

    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::new("catalog_service=debug,tower_http=info"))
        .init();

    tracing::info!("Catalog service starting...");

    let database_url = std::env::var("POSTGRES_CATALOG_URL")
        .expect("Failed to find 'POSTGRES_CATALOG_URL' environment variable!");

    tracing::info!("Connected to the catalog database at: {database_url}!");

    let pool = PgPoolOptions::new()
        .connect(&database_url)
        .await
        .expect("Failed to connect to the catalog database!");

    tracing::info!("Running database migrations...");

    sqlx::migrate!("./migrations")
        .run(&pool)
        .await
        .expect("Failed to run database migrations!");

    tracing::info!("Connected to the catalog database!");

    let state = AppState {
        repo: Arc::new(PostgresRepository::new(pool)),
    };

    let router = router::new_router(state);
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8001")
        .await
        .expect("Failed to bind to address to port 8001!");

    tracing::info!("Catalog Service is running on port 8001!");

    axum::serve(listener, router)
        .await
        .expect("Failed to start the server!");
}

