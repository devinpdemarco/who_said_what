
# Who Said What - Data Pipeline Format

## 1. Overview

The Python data pipeline processes raw news articles before they are stored in Supabase or passed to the machine learning component.

The pipeline accepts a list of article dictionaries, cleans the article text, normalizes metadata, removes duplicates, and validates required fields.

The main function is:

`process_articles(raw_articles)`

It returns two lists:
- `valid_articles`: Articles that passed validation and are ready for storage or ML processing.
- `invalid_articles`: Articles that failed validation because they are missing required information.

## 2. Input Format

The pipeline expects a list of Python dictionaries. Each dictionary represents one raw news article.

### Required fields

| Field | Type | Description |
|---|---|---|
| `title` | String | Article headline |
| `url` | String | Original article URL |
| `source` | String | Name of the news outlet |
| `raw_content` | String | Original article text before cleaning |

The first three fields are required for an article to pass validation. `raw_content` is used to generate `cleaned_text`.

### Optional fields

| Field | Type | Description |
|---|---|---|
| `author` | String or None | Article author |
| `published_date` | String, datetime, or None | Article publication date |

If the author or publication date is unavailable, the pipeline sets the corresponding value to `None`.

### Example input

```json
[
  {
    "title": "Example News Headline",
    "url": "https://example.com/news/article-1",
    "source": "Example News",
    "author": "Jane Doe",
    "published_date": "2026-10-19",
    "raw_content": "This is the original text of the news article."
  }
]
```

## 3. Processing Steps

The pipeline processes each article through the following steps:

1. **Text Cleaning:** Removes unwanted formatting and extra whitespace from the original article text.
2. **Normalization:** Standardizes titles, URLs, source names, author names, and publication dates.
3. **Deduplication:** Removes articles that have the same URL or identical cleaned article text.
4. **Validation:** Checks that all required fields contain values.

## 4. Output Format

The pipeline returns a tuple containing two lists of `Article` objects.

### Article data model

Each processed article uses the following fields:

| Field | Type | Required |
|---|---|---|
| `title` | String | Yes |
| `url` | String | Yes |
| `source` | String | Yes |
| `author` | String or None | No |
| `published_date` | datetime or None | No |
| `cleaned_text` | String | Yes |

### Example valid output

```python
Article(
    title="Example News Headline",
    url="https://example.com/news/article-1",
    source="Example News",
    author="Jane Doe",
    published_date=datetime(2026, 10, 19),
    cleaned_text="This is the original text of the news article."
)
```

### Example invalid output

An article is placed in `invalid_articles` if it is missing a required field.

For example:

```python
Article(
    title="",
    url="https://example.com/news/article-2",
    source="Example News",
    author=None,
    published_date=None,
    cleaned_text="This article is missing a title."
)
```

This article fails validation because its title is empty.

## 5. Deduplication Rules

Articles are considered duplicates if either condition is met:

- They have the same URL (case-insensitive comparison).
- They have identical cleaned article text after converting it to lowercase and normalizing whitespace.

When duplicates are found, the pipeline keeps the first article and skips subsequent copies.

## 6. Validation Rules

The following fields must contain non-empty values:

- `title`
- `url`
- `source`
- `cleaned_text`

The author and publication date are optional.

Articles that fail validation are returned in `invalid_articles` rather than being included in `valid_articles`.

## 7. Pipeline Usage

The pipeline can be called directly from Python:

```python
valid_articles, invalid_articles = process_articles(raw_articles)
```

Example:

```python
print(f"Valid articles: {len(valid_articles)}")
print(f"Invalid articles: {len(invalid_articles)}")
```

## 8. Integration Notes

The expected input is a list of article dictionaries, with the original article text provided under `raw_content`.

The processed output consists of `Article` objects, not JSON dictionaries. If the pipeline is exposed through an HTTP API for n8n, the objects will need to be converted into JSON before being returned.

The processed fields are designed to align with the current Supabase `articles` table:

- `title`
- `url`
- `source`
- `author`
- `published_date`
- `cleaned_text`

The n8n-to-Python connection and the final method of transferring processed articles to Supabase still need to be coordinated and tested.
