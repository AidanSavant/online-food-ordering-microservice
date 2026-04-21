import type { FastifyInstance } from "fastify";
import { OrderHandler } from "./handlers/order.handler.js";
import type { IOrderRespository } from "./repository/order.repository.js";

import swagger from "@fastify/swagger";
import swaggerUi from "@fastify/swagger-ui";

export async function buildRouter(
    app: FastifyInstance,
    repo: IOrderRespository
): Promise<void> {
    await app.register(swagger, {
        openapi: {
            info: {
            title: "Order Service API",
            description: "API documentation for the Order Service",
            version: "1.0.0",
        },
    }}); 
    
    await app.register(swaggerUi, {
        routePrefix: "/docs",
    }); 
    
    const handler = new OrderHandler(repo); 
    
    app.get("/orders", handler.getAllOrders.bind(handler));
    app.get("/orders/:id", handler.getOrderById.bind(handler));
    app.get("/users/:userId/orders", handler.getOrderByUserId.bind(handler));   
    app.delete("/orders/:id", handler.deleteOrder.bind(handler));

    app.post("/orders", {
    schema: {
        body: {
          type: "object",
          required: ["userId", "restaurantId", "items", "totalPrice"],
          properties: {
            userId: { type: "string", format: "uuid" },
            restaurantId: { type: "string", format: "uuid" },
            items: {
              type: "array",
              minItems: 1,
              items: {
                type: "object",
                required: ["itemId", "restaurantId", "name", "price", "quantity"],
                properties: {
                  itemId: { type: "string", format: "uuid" },
                  restaurantId: { type: "string", format: "uuid" },
                  name: { type: "string" },
                  price: { type: "number" },
                  quantity: { type: "number" },
                },
              },
            },
            totalPrice: { type: "number" },
          },
        },
      },
    }, handler.createOrder.bind(handler));
    
    app.patch("/orders/:id/status", {
      schema: {
        body: {
          type: "object",
          required: ["status"],
          properties: {
            status: {
              type: "string",
              enum: ["PENDING", "CONFIRMED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"],
            },
          },
        },
      },
    }, handler.updateOrderStatus.bind(handler));
}
