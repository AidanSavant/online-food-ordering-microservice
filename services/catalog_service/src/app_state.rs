use std::sync::Arc;
use crate::repository::CatalogRepository;

#[derive(Clone)]
pub struct AppState {
    pub repo: Arc<dyn CatalogRepository>,
}

