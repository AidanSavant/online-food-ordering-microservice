import type { Order } from "../models/order.js"
import type { CreateOrderDto, UpdateOrderStatusDto } from "../dtos/order.js"

export interface IOrderRespository {
    getAllOrders(): Promise<Order[]>;
    getOrderByOrderId(id: string): Promise<Order | null>;
    getOrderByUserId(userId: string): Promise<Order[]>;
    createOrder(dto: CreateOrderDto): Promise<Order>;
    updateOrderStatus(id: string, dto: UpdateOrderStatusDto): Promise<Order | null>;
    deleteOrder(id: string): Promise<boolean>;
}
