GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;
CREATE SCHEMA IF NOT EXISTS postgres;
CREATE TABLE IF NOT EXISTS logger (
                     id SERIAL PRIMARY KEY,
                     function_name VARCHAR(255),
                     date_time timestamp NOT NULL,
                     error_level INTEGER NOT NULL,
                     level_name VARCHAR(50) NOT NULL,
                     info TEXT NOT NULL
                 )
