export class OrderError extends Error {
    constructor(
        public readonly message: string,
        public readonly statusCode: number = 500,
    ) {
        super(message);
        this.name = "OrderError";
    }
}

export class NotFoundError extends OrderError {
    constructor(message: string) {
        super(message, 404);
        this.name = "NotFoundError";
    }
}

export class ValidationError extends OrderError {
    constructor(message: string) {
        super(message, 422);
        this.name = "ValidationError";
    }
}

export class UnauthorizedError extends OrderError {
    constructor(message: string) {
        super(message, 401);
        this.name = "UnauthorizedError";
    }
}

export class DatabaseError extends OrderError {
    constructor(message: string) {
        super(message, 500);
        this.name = "DatabaseError";
    }
}
