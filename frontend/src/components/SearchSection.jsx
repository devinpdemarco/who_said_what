import { useState } from 'react'
import ArticleCard from './ArticleCard'
import ComparisonSummary from './ComparisonSummary'
import Timeline from './Timeline'
import BiasCoverage from './BiasCoverage'

function SearchSection() {
  const [searchTerm, setSearchTerm] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [submittedResults, setSubmittedResults] = useState(null)
  const [error, setError] = useState('')
  const [sourceFilter, setSourceFilter] = useState('All')
  const [loading, setLoading] = useState(false)

  const exampleArticles = [
    {
      source: 'example source',
      headline: 'Example headline from example source',
      summary: 'Example summary of how this source is covering the story.',
      sentiment: 'Neutral',
      perspective: 'Factual / Neutral',
      publishedDate: 'September 8, 2026',
      url: 'https://www.examplesource.com'
    },
    {
      source: 'example source 2',
      headline: 'Example headline from example source 2',
      summary: 'Example summary of how a different source is covering the story.',
      sentiment: 'Positive',
      perspective: 'Context Focused',
      publishedDate: 'September 9, 2026',
      url: 'https://examplesource2.com'
    }
  ]

  const [articles, setArticles] = useState(exampleArticles)

  const filteredArticles =
    sourceFilter === 'All'
      ? articles
      : articles.filter(
          (article) => article.source === sourceFilter
        )

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

        {/* HERO */}
        <div className="hero-layout">

          {/* SEARCH PANEL */}
          <div className="search-panel">

            <h1>
              Compare perspectives. Uncover the differences.
            </h1>

            <p className="search-description">
              Search a news topic to compare how different sources
              frame the same story, identify tone differences, and
              track how coverage evolves over time.
            </p>

            <div className="search-bar">
              <input
                type="text"
                placeholder="Search a news topic..."
                value={searchTerm}
                onChange={(event) =>
                  setSearchTerm(event.target.value)
                }
              />

              <button onClick={handleSearch}>
                Search Topic
              </button>
            </div>

            <div className="date-filters">
              <div className="date-field">
                <label htmlFor="start-date">
                  From
                </label>

                <input
                  type="date"
                  id="start-date"
                  value={startDate}
                  onChange={(event) =>
                    setStartDate(event.target.value)
                  }
                />
              </div>

              <div className="date-field">
                <label htmlFor="end-date">
                  To
                </label>

                <input
                  type="date"
                  id="end-date"
                  value={endDate}
                  onChange={(event) =>
                    setEndDate(event.target.value)
                  }
                />
              </div>

              <div className="date-field">
                <label htmlFor="source-filter">
                  Source
                </label>

                <select
                  id="source-filter"
                  value={sourceFilter}
                  onChange={(event) =>
                    setSourceFilter(event.target.value)
                  }
                >
                  <option value="All">
                    All Sources
                  </option>

                  <option value="example source">
                    example source
                  </option>

                  <option value="example source 2">
                    example source 2
                  </option>
                </select>
              </div>
            </div>

            <div className="feature-tags">
              <span>Bias markers</span>
              <span>Perspective comparison</span>
              <span>Timeline tracking</span>
              <span>Coverage gaps</span>
            </div>
          </div>

          {/* METRIC CARDS */}
          <div className="metric-column">

            <div className="metric-card">
              <span className="metric-label">
                METRIC
              </span>

              <strong>
                {articles.length}
              </strong>

              <p>Sources compared</p>

              <span className="metric-description">
                interface data
              </span>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                METRIC
              </span>

              <strong>
                {submittedResults ? 3 : 0}
              </strong>

              <p>Differences detected</p>

              <span className="metric-description">
                insight summaries
              </span>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                METRIC
              </span>

              <strong>
                {submittedResults
                  ? filteredArticles.length
                  : 0}
              </strong>

              <p>Timeline points</p>

              <span className="metric-description">
                Narrative stages found
              </span>
            </div>

          </div>
        </div>

        {/* ERROR */}
        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        {/* LOADING */}
        {loading && (
          <p>Searching articles...</p>
        )}

        {/* NO RESULTS */}
        {!loading &&
          submittedResults &&
          filteredArticles.length === 0 && (
            <p className="no-result">
              No articles found for the given search criteria.
            </p>
          )}

        {/* RESULTS */}
        {submittedResults && (
          <div className="results-area">

            <div className="submitted-results">
              <h2>Search Results</h2>

              <p>
                Showing results for:{' '}
                <strong>
                  {submittedResults.searchTerm}
                </strong>
              </p>

              <p>
                Date range:{' '}
                {submittedResults.startDate} to{' '}
                {submittedResults.endDate}
              </p>
            </div>

            <ComparisonSummary
              articles={filteredArticles}
            />

            <BiasCoverage
                articles={filteredArticles}
            />
            
            <Timeline
              articles={filteredArticles}
            />

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