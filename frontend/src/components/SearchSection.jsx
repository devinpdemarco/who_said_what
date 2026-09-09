import { useState } from 'react'
import ArticleCard from './ArticleCard'
import ComparisonSummary from './ComparisonSummary'
import Timeline from './Timeline'

function SearchSection() {
  const [searchTerm, setSearchTerm] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [submittedResults, setSubmittedResults] = useState(null)
  const [error, setError] = useState('')
  const [sourceFilter, setSourceFilter] = useState('All')
  //const [articles, setArticles] = useState(exampleArticles)
  const [loading, setLoading] = useState(false)
  
  const exampleArticles = [
    {
      source: 'Reuters',
      headline: 'Example headline from Reuters',
      summary: 'Example summary of how this source is covering the story.',
      sentiment: 'Neutral',
      perspective: 'Factual / Neutral',
      publishedDate: 'September 8, 2026',
      url: "https://www.reuters.com"
    },
    {
      source: 'Associated Press',
      headline: 'Example headline from Associated Press',
      summary: 'Example summary of how a different source is covering the story.',
      sentiment: 'Positive',
      perspective: 'Context Focused',
      publishedDate: 'September 9, 2026',
      url: "https://apnews.com"
    }
  ]
  const [articles, setArticles] = useState(exampleArticles)
  const filteredArticles =
    sourceFilter === 'All'
        ? articles
        : articles.filter(article => article.source === sourceFilter)
        
  function handleSearch() {
    if (!searchTerm || !startDate || !endDate) {
      setError('Please fill in all fields.')
      setSubmittedResults(null)
      return
    }

    if (startDate > endDate) {
      setError('Start date cannot be after end date.')
      setSubmittedResults(null)
      return
    }

    setError('')

    setLoading(true)

    setSubmittedResults({
      searchTerm: searchTerm,
      startDate: startDate,
      endDate: endDate
    })
    setLoading(false)
  }

  return (
    <section className="search-section">
      <div className="search-content">
        <h1>Compare the Story. See the Difference.</h1>

        <p>
          Search a news topic to compare how different sources are covering it.
        </p>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Search a news topic..."
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />

          <button onClick={handleSearch}>Search</button>
        </div>

        <div className="date-filters">
          <div className="date-field">
            <label htmlFor="start-date">From</label>
            <input
              type="date"
              id="start-date"
              value={startDate}
              onChange={(event) => setStartDate(event.target.value)}
            />
          </div>

          <div className="date-field">
            <label htmlFor="end-date">To</label>
            <input
              type="date"
              id="end-date"
              value={endDate}
              onChange={(event) => setEndDate(event.target.value)}
            />
          </div>
        
        <div className="date-field">
            <label htmlFor="source-filter">Source:</label>

            <select
                id="source-filter"
                value={sourceFilter}
                onChange={(event) => setSourceFilter(event.target.value)}
            >
                <option value="All">All Sources</option>
                <option value="Reuters">Reuters</option>
                <option value="Associated Press">Associated Press</option>
            </select>
        </div>
        </div>

        {error && (
          <p className="error-message">{error}</p>
        )}

        {loading && (<p> Searching articles...</p>)}

        {!loading && submittedResults && filteredArticles.length === 0 &&
        (
        <p className="no-result">
            No articles found for the given search criteria.
            </p>
        )}

        {submittedResults && (
          <div>
            <div className="submitted-results">
              <h2>Search Results</h2>

              <p>
                Showing results for:{' '}
                <strong>{submittedResults.searchTerm}</strong>
              </p>

              <p>
                Date range: {submittedResults.startDate} to{' '}
                {submittedResults.endDate}
              </p>
            </div>

            <ComparisonSummary articles={filteredArticles} />

            <Timeline articles={filteredArticles} />

            <div className="article-cards">
              {filteredArticles.map((article) => (
                <ArticleCard
                  key={article.headline}
                  source={article.source}
                  headline={article.headline}
                  summary={article.summary}
                  sentiment={article.sentiment}
                  perspective={article.perspective}
                  publishedDate={article.publishedDate}
                  url={article.url}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

export default SearchSection