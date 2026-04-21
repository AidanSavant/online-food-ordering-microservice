import "dotenv/config";
import Fastify from "fastify";
import postgres from "postgres";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { drizzle } from "drizzle-orm/postgres-js";
import { migrate } from "drizzle-orm/postgres-js/migrator";

import { buildRouter } from "./router.js";
import { OrderError } from "./errors/errors.js";
import { PostgresOrderRepository } from "./repository/impls/postgres.repository.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = Fastify({ logger: true });

app.setErrorHandler((error, _request, reply) => {
    if (error instanceof OrderError) {
        return reply.status(error.statusCode).send({ error: error.message });
    }

    app.log.error(error);
    return reply.status(500).send({ error: "Internal Server Error" });
});

async function main() {
    const databaseUrl = process.env["POSTGRES_ORDER_URL"];
    if (!databaseUrl) {
        throw new Error("POSTGRES_ORDER_URL is not defined in environment variables");
    }

    const db = drizzle(postgres(databaseUrl));
    await migrate(db, { migrationsFolder: join(__dirname, "../drizzle") });

    const repo = new PostgresOrderRepository(db);
    await buildRouter(app, repo);

    try {
        await app.listen({ port: 8004, host: "0.0.0.0" });
    } catch (err) {
        app.log.error(`Failed to start server! Reason: ${String(err)}`);
        process.exit(1); 
    }
}

main();
