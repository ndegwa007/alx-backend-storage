-- script creates users table
-- with uniq & default attributes
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    country ENUM('US','CO','TN') NOT NULL DEFAULT 'US',
    UNIQUE (email)
);
