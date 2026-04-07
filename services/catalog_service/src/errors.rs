use thiserror::Error;
use serde_json::json;
use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};

#[derive(Debug, Error)]
pub enum CatalogError {
    #[error("Database error: {0}")]
    DatabaseError(String),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Validation error: {0}")]
    ValidationError(String),

    #[allow(dead_code)]
    #[error("Internal server error {0}")]
    InternalServerError(String),
}

impl IntoResponse for CatalogError {
    fn into_response(self) -> Response {
        let (status, err_msg) = match self {
            CatalogError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            CatalogError::ValidationError(msg) => (StatusCode::BAD_REQUEST, msg),
            CatalogError::DatabaseError(msg) => {
                tracing::error!("Database error: {:?}", msg);
                (StatusCode::INTERNAL_SERVER_ERROR, msg)
            },
            
            CatalogError::InternalServerError(msg) => {
                tracing::error!("Internal server error: {:?}", msg);
                (StatusCode::INTERNAL_SERVER_ERROR, msg)
            },
        };

        let body = Json(json!({
            "error": err_msg,
        }));

        (status, body).into_response()
    }
}

pub type CatalogResult<T> = Result<T, CatalogError>;
