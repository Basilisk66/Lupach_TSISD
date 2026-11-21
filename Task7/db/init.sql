CREATE TABLE IF NOT EXISTS stops (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    route_number VARCHAR(10) NOT NULL,
    stop_id INTEGER NOT NULL REFERENCES stops(id) ON DELETE CASCADE,
    departure_time TIME NOT NULL
);

INSERT INTO stops (name) VALUES
    ('улица Врублевского'),
    ('Университет'),
    ('Парк Жилибера');

INSERT INTO trips (route_number, stop_id, departure_time) VALUES
    ('5',  1, '08:00'), ('5',  1, '08:30'), ('12', 1, '09:15'),
    ('12', 1, '12:00'), ('7',  1, '18:45'),
    ('5',  2, '08:10'), ('7',  2, '10:20'), ('7',  2, '14:40'),
    ('12', 3, '09:00'), ('5',  3, '17:30');
