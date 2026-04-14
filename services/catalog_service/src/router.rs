use axum::{Router, routing::get};

use crate::app_state::AppState;
use crate::handlers::restaurants::{
    get_restaurants, get_restaurant_by_id,
    create_restaurant, update_restaurant, delete_restaurant,
};

use crate::handlers::menu_items::{
    get_menu_items_by_restaurant_id, get_menu_item_by_id,
    create_menu_item, update_menu_item, delete_menu_item,
};

pub fn new_router(state: AppState) -> Router {
    let restaurant_routes = Router::new()
        .route("/", get(get_restaurants).post(create_restaurant))
        .route("/{id}",
            get(get_restaurant_by_id)
            .patch(update_restaurant)
            .delete(delete_restaurant)
        );

    let menu_item_routes = Router::new()
        .route("/", get(get_menu_items_by_restaurant_id).post(create_menu_item))
        .route("/{id}",
            get(get_menu_item_by_id)
            .patch(update_menu_item)
            .delete(delete_menu_item)
        );

    Router::new()
        .nest("/restaurants", restaurant_routes)
        .nest("/restaurants/{restaurant_id}/items", menu_item_routes)
        .with_state(state)
}
