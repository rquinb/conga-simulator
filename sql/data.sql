CREATE TABLE simulations (
	id VARCHAR PRIMARY KEY,
    created TIMESTAMP,
    total_games INT,
    mean_rounds_per_game FLOAT,
    details JSON
);