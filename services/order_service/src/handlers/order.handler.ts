import type { FastifyRequest, FastifyReply } from "fastify";

import { NotFoundError, ValidationError } from "../errors/errors.js";
import type { IOrderRespository } from "../repository/order.repository.js";
import { CreateOrderSchema, UpdateOrderStatusSchema, toOrderResponse } from "../dtos/order.js";

export class OrderHandler {
    constructor(private repo: IOrderRespository) {}

    async getAllOrders(_request: FastifyRequest, reply: FastifyReply) {
        const orders = await this.repo.getAllOrders();
        return reply.send(orders.map(toOrderResponse));
    }

    async getOrderById(
        request: FastifyRequest<{ Params: { id: string }}>,
        reply: FastifyReply
    ) {
        const order = await this.repo.getOrderByOrderId(request.params.id);
        if (!order) {
            throw new NotFoundError("Order not found");
        }
    
        return reply.send(toOrderResponse(order));
    }

    async getOrderByUserId(
        request: FastifyRequest<{ Params: { userId: string } }>,
        reply: FastifyReply
    ) {
        const { userId } = request.params;
        const orders = await this.repo.getOrderByUserId(userId);

        return reply.send(orders.map(toOrderResponse));
    }

    async createOrder(
        request: FastifyRequest,
        reply: FastifyReply
    ) {
        const result = CreateOrderSchema.safeParse(request.body);
        if (!result.success) {
            throw new ValidationError(`Invalid request body: ${result.error.message}`);
        }

        const order = await this.repo.createOrder(result.data);
        return reply.status(201).send(toOrderResponse(order));
    }

    async updateOrderStatus(
        request: FastifyRequest<{ Params: { id: string } }>,
        reply: FastifyReply
    ) {
        const result = UpdateOrderStatusSchema.safeParse(request.body);
        if (!result.success) {
            throw new ValidationError(`Invalid request body: ${result.error.message}`);
        }

        const order = await this.repo.updateOrderStatus(request.params.id, result.data);
        if (!order) {
            throw new NotFoundError(`Order '${request.params.id}' not found`);
        }

        return reply.send(toOrderResponse(order));
    }

    async deleteOrder(
        request: FastifyRequest<{ Params: { id: string } }>,
        reply: FastifyReply
    ) {
        const success = await this.repo.deleteOrder(request.params.id);
        if (!success) {
            throw new NotFoundError("Order not found");
        }

        return reply.status(204).send();
    } 
}
