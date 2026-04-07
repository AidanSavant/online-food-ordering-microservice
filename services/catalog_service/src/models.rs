use uuid::Uuid;
use chrono::{DateTime, Utc};
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Restaurant {
    pub id: Uuid,
    
    pub name: String,
    pub description: String,
    pub address: String,

    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MenuItem {
    pub id: Uuid,
    pub restaurant_id: Uuid,

    pub name: String,
    pub description: Option<String>,
    pub price: f64,

    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}
