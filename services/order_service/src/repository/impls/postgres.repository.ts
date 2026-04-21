import { eq } from "drizzle-orm"
import type { PostgresJsDatabase } from "drizzle-orm/postgres-js"

import { orders } from "../../db/schema.js"
import { DatabaseError } from "../../errors/errors.js"
import type { Order, OrderItem } from "../../models/order.ts"
import type { IOrderRespository } from "../order.repository.ts"
import type { CreateOrderDto, UpdateOrderStatusDto } from "../../dtos/order.ts"

export class PostgresOrderRepository implements IOrderRespository {
    constructor(private readonly db: PostgresJsDatabase) {}

    private toOrder(record: typeof orders.$inferSelect): Order {
        return {
            id: record.id,
            userId: record.userId,
            restaurantId: record.restaurantId,
            items: record.items as OrderItem[],
            totalPrice: Number(record.totalPrice),
            status: record.status,
            createdAt: record.createdAt,
            updatedAt: record.updatedAt,
        }
    }

    async getAllOrders(): Promise<Order[]> {
        try {
            const records = await this.db.select().from(orders);
            return records.map((record) => this.toOrder(record));
        } catch (e) {
            throw new DatabaseError(`Failed to fetch orders! Reason: ${String(e)}`);
        }
    }

    async getOrderByOrderId(id: string): Promise<Order | null> {
        try {
            const records = await this.db
                .select()
                .from(orders)
                .where(eq(orders.id, id));
            
            return records[0] ? this.toOrder(records[0]) : null;
        } catch (e) {
            throw new DatabaseError(`Failed to fetch order with id ${id}! Reason: ${String(e)}`);
        }
    }

    async getOrderByUserId(userId: string): Promise<Order[]> {
        try {
            const records = await this.db
                .select()
                .from(orders)
                .where(eq(orders.userId, userId));
            
            return records.map((record) => this.toOrder(record));
        } catch (e) {
            throw new DatabaseError(`Failed to fetch orders for user with id ${userId}! Reason: ${String(e)}`);
        }
    }

    async createOrder(dto: CreateOrderDto): Promise<Order> {
        try {
            const records = await this.db
                .insert(orders)
                .values({
                    userId: dto.userId,
                    restaurantId: dto.restaurantId,
                    items: dto.items,
                    totalPrice: String(dto.totalPrice),
                })
                .returning();

            const record = records[0];
            if(!record) {
                throw new DatabaseError("Failed to create order! Reason: No record returned!");
            }

            return this.toOrder(record);
        } catch (e) {
            if(e instanceof DatabaseError) throw e;
            throw new DatabaseError(`Failed to create order! Reason: ${String(e)}`);
        }
    }

    async updateOrderStatus(id: string, dto: UpdateOrderStatusDto): Promise<Order | null> {
        try {
            const records = await this.db
                .update(orders)
                .set({ status: dto.status, updatedAt: new Date() })
                .where(eq(orders.id, id))
                .returning();

            return records[0] ? this.toOrder(records[0]) : null;
        } catch (e) {
            throw new DatabaseError(`Failed to update order with id ${id}! Reason: ${String(e)}`);
        }
    }

    async deleteOrder(id: string): Promise<boolean> {
        try {
            const records = await this.db
                .delete(orders)
                .where(eq(orders.id, id))
                .returning();

            return records.length > 0;
        } catch (e) {
            throw new DatabaseError(`Failed to delete order with id ${id}! Reason: ${String(e)}`);
        }
    }
}
