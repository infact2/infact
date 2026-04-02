# InFact

InFact is a news corroboration platform that fights media bias. Give it a news article URL and it finds a story covering the same event from an outlet with an opposing political lean, then uses GPT-4 to synthesize an unbiased summary with direct quotes from both sources.

## Setup

1. Clone the repo and `cd infact`
2. Create a `.env` file with the following keys:

```
SUPABASE_URL=
SUPABASE_KEY=
NEWS_API_KEY=
GOOGLE_API_KEY=
OPENAI_API_KEY=
```

## Running

**Docker (recommended):**

```bash
# Build
docker build -t infact .

# Run (detached / server)
docker run --name infact -d -p 8000:8000 infact

# Run (interactive / local debug)
docker run --name infact -it -p 8000:8000 infact

# Stop
docker stop --signal SIGKILL infact
```

**Without Docker:**

```bash
pip install -r requirements.txt
python main.py
```

App runs at `http://localhost:8000`.

## How It Works

1. A user submits a news article URL.
2. InFact determines the political bias of the source using AllSides data.
3. It searches Google for coverage of the same story from an outlet with the opposite bias.
4. Both articles are sent to GPT-4-turbo, which writes a 3-paragraph corroboration with quotes attributed to each source.
5. The result is displayed alongside political lean indicators for both outlets.

## API Reference

### `extractText(url)`

Extracts the body text of a news article.

```python
extractText("https://example.com/article")
# Returns: plain text string of article content
```

### `corroborate(url1, url2)`

Corroborates two news articles into a single synthesis.

```python
corroborate("https://cnn.com/...", "https://abcnews.go.com/...")
# Returns: corroborated string (may take several seconds)
```

### `textToHTML(text)`

Converts newlines to `<br>` tags for HTML rendering.

```python
textToHTML("Line one\n\nLine two")
# Returns: "Line one<br><br>Line two"
```
