DROP TABLE IF EXISTS certificates;

CREATE TABLE certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    public_id TEXT UNIQUE,
    certificate_id TEXT NOT NULL UNIQUE,
    author_name TEXT NOT NULL,
    article_name TEXT NOT NULL UNIQUE,
    pdf_drive_link TEXT,
    generation_timestamp TEXT NOT NULL,
    pdf_path TEXT
);

-- index id, fast lookup, check documentation again

CREATE INDEX idx_certificate_id ON certificates (certificate_id);