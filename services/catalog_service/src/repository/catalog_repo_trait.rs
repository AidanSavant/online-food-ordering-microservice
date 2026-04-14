use uuid::Uuid;
use async_trait::async_trait;

use crate::errors::CatalogResult;
use crate::models::{Restaurant, MenuItem};
use crate::dto::{MenuItemCreateDto, MenuItemUpdateDto};
use crate::dto::{RestaurantCreateDto, RestaurantUpdateDto};

#[async_trait]
pub trait CatalogRepository: Send + Sync {
    async fn get_restaurants(&self) -> CatalogResult<Vec<Restaurant>>;
    async fn get_restaurant_by_id(&self, id: Uuid) -> CatalogResult<Option<Restaurant>>;
    async fn create_restaurant(&self, restaurant: RestaurantCreateDto) -> CatalogResult<Restaurant>;
    async fn update_restaurant(&self, id: Uuid, restaurant: RestaurantUpdateDto) -> CatalogResult<Option<Restaurant>>;
    async fn delete_restaurant(&self, id: Uuid) -> CatalogResult<bool>;

    async fn get_menu_items_by_restaurant_id(&self, restaurant_id: Uuid) -> CatalogResult<Vec<MenuItem>>;
    async fn get_menu_item_by_id(&self, id: Uuid) -> CatalogResult<Option<MenuItem>>;
    async fn create_menu_item(&self, restaurant_id: Uuid, menu_item: MenuItemCreateDto) -> CatalogResult<MenuItem>;
    async fn update_menu_item(&self, id: Uuid, menu_item: MenuItemUpdateDto) -> CatalogResult<Option<MenuItem>>;
    async fn delete_menu_item(&self, id: Uuid) -> CatalogResult<bool>;
}
