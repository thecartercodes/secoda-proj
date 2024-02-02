CREATE TABLE IF NOT EXISTS price_metrics (
	category VARCHAR(255),
	price_sum NUMERIC(32,2),
	price_avg NUMERIC(32,2),
	listings INT,
	published_at TIMESTAMP,
	created_at TIMESTAMP
);
