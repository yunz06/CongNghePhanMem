CREATE TABLE conferences (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    submission_deadline TIMESTAMP NOT NULL
);

CREATE TABLE tracks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    conference_id INT NOT NULL,
    CONSTRAINT fk_conference
        FOREIGN KEY (conference_id)
        REFERENCES conferences(id)
        ON DELETE CASCADE
);
