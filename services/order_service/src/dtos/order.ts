import { z } from "zod";
import type { Order } from "../models/order.js";

export const CreateOrderSchema = z.object({
    userId: z.uuid(),
    restaurantId: z.uuid(),
    items: z.array(
        z.object({
            itemId: z.uuid(),
            restaurantId: z.uuid(),
            name: z.string().min(1).max(255),
            price: z.number().positive(),
            quantity: z.number().int().positive(),
        })).min(1),
    totalPrice: z.number().positive(),
});

export const UpdateOrderStatusSchema = z.object({
    status: z.enum([
        "PENDING",
        "CONFIRMED",
        "PREPARING",
        "OUT_FOR_DELIVERY",
        "DELIVERED",
        "CANCELED",
    ]),
});

export type CreateOrderDto = z.infer<typeof CreateOrderSchema>;
export type UpdateOrderStatusDto = z.infer<typeof UpdateOrderStatusSchema>;

export interface OrderResponse {
    id: string;
    userId: string;
    restaurantId: string;

    items: Order["items"];
    totalPrice: number;

    status: Order["status"];

    createdAt: string;
    updatedAt: string;
}

export function toOrderResponse(order: Order): OrderResponse {
    return {
        id: order.id,
        userId: order.userId,
        restaurantId: order.restaurantId,
        items: order.items,
        totalPrice: order.totalPrice,
        status: order.status,
        createdAt: order.createdAt.toISOString(),
        updatedAt: order.updatedAt.toISOString(),
    }
}
