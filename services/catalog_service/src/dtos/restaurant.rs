use crate::models::Restaurant;

use uuid::Uuid;
use validator::Validate;
use serde::{Serialize, Deserialize};

#[derive(Debug, Deserialize, Validate)]
pub struct RestaurantCreateDto {
    #[validate(length(min = 1, max = 255))]
    pub name: String,
    
    #[validate(length(min = 1, max = 255))]
    pub description: String,
    
    #[validate(length(min = 1,  max = 255))]
    pub address: String,
}

#[derive(Debug, Deserialize, Validate)]
pub struct RestaurantUpdateDto {
    #[validate(length(min = 1, max = 255))]
    pub name: Option<String>,
    
    #[validate(length(min = 1, max = 255))]
    pub description: Option<String>,

    #[validate(length(min = 1, max = 255))]
    pub address: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct RestaurantResponse {
    pub id: Uuid,
    
    pub name: String,
    pub description: String,
    pub address: String,

    pub created_at: String,
    pub updated_at: String,
}

impl From<Restaurant> for RestaurantResponse {
    fn from(restaurant: Restaurant) -> Self {
        Self {
            id: restaurant.id,
            name: restaurant.name,
            description: restaurant.description,
            address: restaurant.address,
            created_at: restaurant.created_at.to_rfc3339(),
            updated_at: restaurant.updated_at.to_rfc3339(),
        }
    }
}
