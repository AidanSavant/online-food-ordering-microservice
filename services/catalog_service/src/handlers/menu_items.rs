use uuid::Uuid;
use axum::{
    Json,
    http::StatusCode,
    extract::{State, Path},
    response::IntoResponse,
};

use validator::Validate;

use crate::app_state::AppState;
use crate::errors::{CatalogError, CatalogResult};
use crate::dto::{MenuItemCreateDto, MenuItemUpdateDto, MenuItemResponse};

pub async fn get_menu_items_by_restaurant_id(
    State(state): State<AppState>,
    Path(restaurant_id): Path<Uuid>,
) -> CatalogResult<impl IntoResponse> {
    state.repo.get_restaurant_by_id(restaurant_id).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Restaurant {} not found", restaurant_id)))?;
    
    let menu_items = state.repo.get_menu_items_by_restaurant_id(restaurant_id).await?;
    let resp = menu_items.into_iter()
        .map(MenuItemResponse::from)
        .collect::<Vec<_>>();
    
    Ok(Json(resp))
}

pub async fn get_menu_item_by_id(
    State(state): State<AppState>,
    Path((restaurant_id, menu_item_id)): Path<(Uuid, Uuid)>,
) -> CatalogResult<impl IntoResponse> {
    let menu_item = state.repo.get_menu_item_by_id(menu_item_id).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)))?;
    
    if menu_item.restaurant_id != restaurant_id {
        return Err(CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)));
    }
    
    Ok(Json(MenuItemResponse::from(menu_item)))
}

pub async fn create_menu_item(
    State(state): State<AppState>,
    Path(restaurant_id): Path<Uuid>,
    Json(payload): Json<MenuItemCreateDto>,
) -> CatalogResult<impl IntoResponse> {
    payload.validate().map_err(|e| CatalogError::ValidationError(e.to_string()))?;
    
    state.repo.get_restaurant_by_id(restaurant_id).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Restaurant {} not found", restaurant_id)))?;
    
    let menu_item = state.repo.create_menu_item(restaurant_id, payload).await?;
    Ok((StatusCode::CREATED, Json(MenuItemResponse::from(menu_item))))
}

pub async fn update_menu_item(
    State(state): State<AppState>,
    Path((restaurant_id, menu_item_id)): Path<(Uuid, Uuid)>,
    Json(payload): Json<MenuItemUpdateDto>,
) -> CatalogResult<impl IntoResponse> {
    payload.validate().map_err(|e| CatalogError::ValidationError(e.to_string()))?;
    
    let existing = state.repo.get_menu_item_by_id(menu_item_id).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)))?;
    
    if existing.restaurant_id != restaurant_id {
        return Err(CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)));
    }
    
    let updated = state.repo.update_menu_item(menu_item_id, payload).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)))?;
    
    Ok(Json(MenuItemResponse::from(updated)))
}

pub async fn delete_menu_item(
    State(state): State<AppState>,
    Path((restaurant_id, menu_item_id)): Path<(Uuid, Uuid)>,
) -> CatalogResult<impl IntoResponse> {
    let existing = state.repo.get_menu_item_by_id(menu_item_id).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)))?;
    
    if existing.restaurant_id != restaurant_id {
        return Err(CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)));
    }
    
    let true = state.repo.delete_menu_item(menu_item_id).await? else {
        return Err(CatalogError::NotFound(format!("Menu item {} not found", menu_item_id)));
    };
    
    Ok(StatusCode::NO_CONTENT.into_response())
}
