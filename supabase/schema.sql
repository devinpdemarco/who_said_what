CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    author TEXT,
    published_date TIMESTAMPTZ,
    cleaned_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);