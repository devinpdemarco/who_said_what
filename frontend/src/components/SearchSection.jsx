
import { useState } from 'react'
import ArticleCard from './ArticleCard'
import ArticleCarousel from './ArticleCarousel'
import ComparisonSummary from './ComparisonSummary'
import BiasCoverage from './BiasCoverage'
import Timeline from './Timeline'

function SearchSection() {
  const [searchTerm, setSearchTerm] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [sourceFilter, setSourceFilter] = useState('All')
  const [submittedResults, setSubmittedResults] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Temporary mock data until the backend is connected
  const exampleArticles = [
    {
      source: 'Reuters',
      headline: 'Example headline from Reuters',
      summary: 'Example summary of how this source is covering the story.',
      sentiment: 'Neutral',
      perspective: 'Factual / Neutral',
      politicalLeaning: null,
      publishedDate: 'September 8, 2026',
      url: 'https://www.reuters.com'
    },
    {
      source: 'Associated Press',
      headline: 'Example headline from Associated Press',
      summary: 'Example summary of how a different source is covering the story.',
      sentiment: 'Positive',
      perspective: 'Context Focused',
      politicalLeaning: null,
      publishedDate: 'September 9, 2026',
      url: 'https://apnews.com'
    }
  ]

  const [articles] = useState(exampleArticles)

  const filteredArticles =
    sourceFilter === 'All'
      ? articles
      : articles.filter((article) => article.source === sourceFilter)

  function handleSearch() {
    if (!searchTerm.trim() || !startDate || !endDate) {
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

    // Temporary mock search until backend integration
    setSubmittedResults({
      searchTerm: searchTerm.trim(),
      startDate,
      endDate
    })

    setLoading(false)
  }

  return (
    <section className="search-section">
      <div className="search-content">

        {/* =========================
            HERO SEARCH DASHBOARD
           ========================= */}

        <div className="hero-layout">

          <div className="search-panel">
            <p className="eyebrow">INTERFACE CONCEPT</p>

            <h1>
              Compare perspectives.
              <br />
              Uncover the differences.
            </h1>

            <p className="search-description">
              Explore how different news sources cover the same
              story. Compare perspectives, identify potential bias,
              and track how narratives develop over time.
            </p>

            <div className="search-bar">
              <input
                type="text"
                placeholder="Search a news topic..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch()
                  }
                }}
              />

              <button onClick={handleSearch}>
                Search Topic
              </button>
            </div>

            <div className="date-filters">
              <div className="filter-group">
                <label htmlFor="start-date">From</label>
                <input
                  id="start-date"
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
              </div>

              <div className="filter-group">
                <label htmlFor="end-date">To</label>
                <input
                  id="end-date"
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </div>

              <div className="filter-group">
                <label htmlFor="source-filter">Source</label>
                <select
                  id="source-filter"
                  value={sourceFilter}
                  onChange={(e) => setSourceFilter(e.target.value)}
                >
                  <option value="All">All Sources</option>
                  <option value="Reuters">Reuters</option>
                  <option value="Associated Press">
                    Associated Press
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

          {/* DASHBOARD METRICS */}

          <div className="metric-column">
            <div className="metric-card">
              <span className="metric-label">
                SOURCES COMPARED
              </span>
              <h2>{submittedResults ? filteredArticles.length : 0}</h2>
              <p>News articles available for comparison</p>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                DIFFERENCES DETECTED
              </span>
              <h2>{submittedResults ? 3 : 0}</h2>
              <p>Example analysis metric</p>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                TIMELINE POINTS
              </span>
              <h2>{submittedResults ? filteredArticles.length : 0}</h2>
              <p>Articles in the current timeline</p>
            </div>
          </div>
        </div>

        {/* =========================
            SEARCH FEEDBACK
           ========================= */}

        {error && (
          <p className="error-message">{error}</p>
        )}

        {loading && (
          <p>Searching articles...</p>
        )}

        {!loading &&
          submittedResults &&
          filteredArticles.length === 0 && (
            <p className="no-result">
              No articles found for the given search criteria.
            </p>
          )}

        {/* =========================
            ARTICLE CAROUSEL
           ========================= */}

        {submittedResults && filteredArticles.length > 0 && (
          <ArticleCarousel articles={filteredArticles} />
        )}

        {/* =========================
            RESULTS DASHBOARD
           ========================= */}

        {submittedResults && filteredArticles.length > 0 && (
          <div className="results-area">

            {/* SIDE-BY-SIDE ARTICLE COMPARISON */}

            <div className="comparison-articles-section" id="compare">
              <h2>Compare News Coverage</h2>

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
                    politicalLeaning={article.politicalLeaning}
                  />
                ))}
              </div>
            </div>

            {/* ANALYSIS COMPONENTS SIDE BY SIDE */}

            <div className="analysis-grid">
              <ComparisonSummary articles={filteredArticles} />
              <BiasCoverage articles={filteredArticles} />
            </div>

            {/* NARRATIVE TIMELINE */}

            <Timeline articles={filteredArticles} />

          </div>
        )}
      </div>
    </section>
  )
}

export default SearchSection
