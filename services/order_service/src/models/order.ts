export type OrderStatus = 
    | "PENDING"
    | "CONFIRMED"
    | "PREPARING"
    | "OUT_FOR_DELIVERY"
    | "DELIVERED"
    | "CANCELED";

export interface OrderItem {
    item_id: string;
    restaurantId: string;
    
    name: string;
    price: number;
    quantity: number;
}

export interface Order {
    id: string;
    userId: string;
    restaurantId: string;

    items: OrderItem[];
    totalPrice: number;

    status: OrderStatus;

    createdAt: Date;
    updatedAt: Date;
}
