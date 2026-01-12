CREATE TABLE reviews (
  id INT NOT NLL,
  reviewer_id INT NOT NULL,
  score INT CHECK (score BETWEEN 1 AND 10),
  comment TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
