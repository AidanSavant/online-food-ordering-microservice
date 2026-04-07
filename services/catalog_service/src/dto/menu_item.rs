use crate::models::MenuItem;

use uuid::Uuid;
use validator::Validate;
use serde::{Serialize, Deserialize};

#[derive(Debug, Deserialize, Validate)]
pub struct MenuItemCreateDto {
    #[validate(length(min = 1, max = 255))]
    pub name: String,

    #[validate(length(min = 1, max = 255))]
    pub description: Option<String>,

    #[validate(range(min = 0.50, max=1000.00))]
    pub price: f64,
}

#[derive(Debug, Deserialize, Validate)]
pub struct MenuItemUpdateDto {
    #[validate(length(min = 1, max = 255))]
    pub name: Option<String>,

    #[validate(length(min = 1, max = 255))]
    pub description: Option<String>,

    #[validate(range(min = 0.50, max=1000.00))]
    pub price: Option<f64>,
}

#[derive(Debug, Serialize)]
pub struct MenuItemResponse {
    pub id: Uuid,
    pub restaurant_id: Uuid,

    pub name: String,
    pub description: Option<String>,
    pub price: f64,

    pub created_at: String,
    pub updated_at: String,
}

impl From<MenuItem> for MenuItemResponse {
    fn from(menu_item: MenuItem) -> Self {
        Self {
            id: menu_item.id,
            restaurant_id: menu_item.restaurant_id,
            name: menu_item.name,
            description: menu_item.description,
            price: menu_item.price,
            created_at: menu_item.created_at.to_rfc3339(),
            updated_at: menu_item.updated_at.to_rfc3339(),
        }
    }
}
