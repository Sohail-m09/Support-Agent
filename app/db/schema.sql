-- schema.sql - the tables of our database.
-- Run by scripts/setup_db.py. It DROPS and recreates the tables,
-- so it is only for setup or a full reset.

CREATE EXTENSION IF NOT EXISTS vector;   -- teaches Postgres to store and search vectors

DROP TABLE IF EXISTS refund_requests;
DROP TABLE IF EXISTS policy_chunks;
DROP TABLE IF EXISTS orders;

-- Fake customer orders
CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_id    TEXT NOT NULL,
    item           TEXT NOT NULL,
    category       TEXT NOT NULL,
    price          NUMERIC(10, 2) NOT NULL,   -- NUMERIC, not float, for money
    status         TEXT NOT NULL
                   CHECK (status IN ('placed', 'shipped', 'delivered', 'cancelled')),
    order_date     DATE NOT NULL,
    delivered_date DATE                       -- empty until delivered
);

-- Refund requests. The agent can only create 'pending' ones.
CREATE TABLE refund_requests (
    id         SERIAL PRIMARY KEY,
    ticket_id  TEXT NOT NULL,
    order_id   INTEGER NOT NULL REFERENCES orders (order_id),
    amount     NUMERIC(10, 2) NOT NULL,
    reason     TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'pending'
               CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    decided_at TIMESTAMPTZ
);

-- Only ONE pending request per order, so repeats cannot pile up
CREATE UNIQUE INDEX one_pending_refund_per_order
    ON refund_requests (order_id) WHERE status = 'pending';

-- Policy text split into chunks, with its vector and a keyword index
CREATE TABLE policy_chunks (
    id          SERIAL PRIMARY KEY,
    doc_id      TEXT NOT NULL,
    category    TEXT NOT NULL,
    content     TEXT NOT NULL,
    embedding   vector(768) NOT NULL,         -- must match EMBEDDING_DIMENSIONS
    content_tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', content)) STORED
);

CREATE INDEX policy_chunks_text_idx ON policy_chunks USING gin (content_tsv);