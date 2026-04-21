import {
    pgTable,
    uuid,
    numeric,
    timestamp,
    pgEnum,
    jsonb
} from "drizzle-orm/pg-core";

export const orderStatusEnum = pgEnum("order_status", [
    "PENDING",
    "CONFIRMED",
    "PREPARING",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "CANCELED"
]);

export const orders = pgTable("orders", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").notNull(),
    restaurantId: uuid("restaurant_id").notNull(),
    
    items: jsonb("items").notNull(),
    totalPrice: numeric("total_price", { precision: 10, scale: 2 }).notNull(),
    
    status: orderStatusEnum("status").notNull().default("PENDING"),

    createdAt: timestamp("created_at").notNull().defaultNow(),
    updatedAt: timestamp("updated_at").notNull().defaultNow()
});

export type OrderRecord = typeof orders.$inferSelect;
export type NewOrderRecord = typeof orders.$inferInsert;
