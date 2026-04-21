use uuid::Uuid;
use validator::Validate;
use axum::{
    http::StatusCode,
    extract::{State, Path},
    response::{IntoResponse, Json},
};

use crate::app_state::AppState;
use crate::errors::{CatalogError, CatalogResult};
use crate::dtos::{
    RestaurantCreateDto, RestaurantUpdateDto,
    RestaurantResponse,
};

pub async fn get_restaurants(State(state): State<AppState>) -> CatalogResult<impl IntoResponse> {
    let restaurants = state.repo.get_restaurants().await?;
    let resp = restaurants.into_iter()
        .map(RestaurantResponse::from)
        .collect::<Vec<_>>();

    Ok(Json(resp))
}

pub async fn get_restaurant_by_id(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
) -> CatalogResult<impl IntoResponse> {
    let restaurant = state.repo.get_restaurant_by_id(id).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Restaurant with id {} not found", id)))?;
    
    Ok(Json(RestaurantResponse::from(restaurant)))
}

pub async fn create_restaurant(
    State(state): State<AppState>,
    Json(payload): Json<RestaurantCreateDto>
) -> CatalogResult<impl IntoResponse> {
    payload.validate().map_err(|e| CatalogError::ValidationError(e.to_string()))?;

    let restaurant = state.repo.create_restaurant(payload).await?;
    Ok((StatusCode::CREATED, Json(RestaurantResponse::from(restaurant))))
}

pub async fn update_restaurant(
    State(state): State<AppState>,
    Path(id): Path<Uuid>,
    Json(payload): Json<RestaurantUpdateDto>
) -> CatalogResult<impl IntoResponse> {
    payload.validate().map_err(|e| CatalogError::ValidationError(e.to_string()))?;
    
    let restaurant = state.repo.update_restaurant(id, payload).await?
        .ok_or_else(|| CatalogError::NotFound(format!("Restaurant with id {} not found", id)))?;
    
    Ok(Json(RestaurantResponse::from(restaurant)))
}

pub async fn delete_restaurant(
    State(state): State<AppState>,
    Path(id): Path<Uuid>
) -> CatalogResult<impl IntoResponse> {
    let true = state.repo.delete_restaurant(id).await? else {
        return Err(CatalogError::NotFound(format!("Restaurant with id {} not found", id)));
    };

    Ok(StatusCode::NO_CONTENT.into_response())
}
