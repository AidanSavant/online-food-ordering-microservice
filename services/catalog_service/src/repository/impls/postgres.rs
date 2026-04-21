use uuid::Uuid;
use sqlx::PgPool;
use async_trait::async_trait;

use crate::repository::CatalogRepository;
use crate::models::{Restaurant, MenuItem};
use crate::errors::{CatalogError, CatalogResult};
use crate::dtos::{MenuItemCreateDto, MenuItemUpdateDto};
use crate::dtos::{RestaurantCreateDto, RestaurantUpdateDto};

pub struct PostgresRepository {
    pool: PgPool,
}

impl PostgresRepository {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl CatalogRepository for PostgresRepository {
    async fn get_restaurants(&self) -> CatalogResult<Vec<Restaurant>> {
        sqlx::query_as!(
            Restaurant,
            "SELECT * FROM restaurants ORDER BY created_at DESC"
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn get_restaurant_by_id(&self, id: Uuid) -> CatalogResult<Option<Restaurant>> {
        sqlx::query_as!(
            Restaurant,
            "SELECT * FROM restaurants WHERE id = $1",
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn create_restaurant(&self, restaurant: RestaurantCreateDto) -> CatalogResult<Restaurant> {
        sqlx::query_as!(
            Restaurant,
            "INSERT INTO restaurants (id, name, description, address, created_at, updated_at) 
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *",
            Uuid::new_v4(),
            restaurant.name,
            restaurant.description,
            restaurant.address,
            chrono::Utc::now(),
            chrono::Utc::now()
        )
        .fetch_one(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn update_restaurant(&self, id: Uuid, restaurant: RestaurantUpdateDto) -> CatalogResult<Option<Restaurant>> {
        sqlx::query_as!(
            Restaurant,
            "UPDATE restaurants 
            SET name = COALESCE($1, name), 
                description = COALESCE($2, description), 
                address = COALESCE($3, address), 
                updated_at = $4
            WHERE id = $5
            RETURNING *",
            restaurant.name,
            restaurant.description,
            restaurant.address,
            chrono::Utc::now(),
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn delete_restaurant(&self, id: Uuid) -> CatalogResult<bool> {
        let result = sqlx::query!(
            "DELETE FROM restaurants WHERE id = $1",
            id
        )
        .execute(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))?;

        Ok(result.rows_affected() > 0)
    }

    async fn get_menu_items_by_restaurant_id(&self, restaurant_id: Uuid) -> CatalogResult<Vec<MenuItem>> {
        sqlx::query_as!(
            MenuItem,
            "SELECT * FROM menu_items WHERE restaurant_id = $1 ORDER BY created_at DESC",
            restaurant_id
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn get_menu_item_by_id(&self, id: Uuid) -> CatalogResult<Option<MenuItem>> {
        sqlx::query_as!(
            MenuItem,
            "SELECT * FROM menu_items WHERE id = $1",
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn create_menu_item(&self, restaurant_id: Uuid, menu_item: MenuItemCreateDto) -> CatalogResult<MenuItem> {
        sqlx::query_as!(
            MenuItem,
            "INSERT INTO menu_items (id, restaurant_id, name, description, price, created_at, updated_at) 
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING *",
            Uuid::new_v4(),
            restaurant_id,
            menu_item.name,
            menu_item.description,
            menu_item.price,
            chrono::Utc::now(),
            chrono::Utc::now()
        )
        .fetch_one(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn update_menu_item(&self, id: Uuid, menu_item: MenuItemUpdateDto) -> CatalogResult<Option<MenuItem>> {
        sqlx::query_as!(
            MenuItem,
            "UPDATE menu_items 
            SET name = COALESCE($1, name), 
                description = COALESCE($2, description), 
                price = COALESCE($3, price), 
                updated_at = $4
            WHERE id = $5
            RETURNING *",
            menu_item.name,
            menu_item.description,
            menu_item.price,
            chrono::Utc::now(),
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))
    }

    async fn delete_menu_item(&self, id: Uuid) -> CatalogResult<bool> {
        let result = sqlx::query!(
            "DELETE FROM menu_items WHERE id = $1",
            id
        )
        .execute(&self.pool)
        .await
        .map_err(|e| CatalogError::DatabaseError(e.to_string()))?;

        Ok(result.rows_affected() > 0)
    }
}
