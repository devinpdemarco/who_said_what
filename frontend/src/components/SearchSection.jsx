
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

  // State for articles, clusters, loading, and message
  const [articles, setArticles] = useState([])
  const [clusters, setClusters] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const filteredArticles =
    sourceFilter === 'All'
      ? articles
      : articles.filter((article) => article.source === sourceFilter)

  
  async function handleSearch() {
    // Validate search inputs
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
    setMessage('')
    setLoading(true)
    setSubmittedResults(null)
    setArticles([])
    setClusters([])

    try {
      const response = await fetch(import.meta.env.VITE_SEARCH_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          topic: searchTerm.trim(),
          start_date: startDate,
          end_date: endDate,
          source: 'All'
        })
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.message || 'Search failed. Please try again.')
      }

      setArticles(data.articles ?? [])
      setClusters(data.clusters ?? [])
      setSourceFilter('All')
      setMessage(data.message || '')

      setSubmittedResults({
        searchTerm: searchTerm.trim(),
        startDate,
        endDate
      })
    } catch (error) {
      setError(error.message || 'Something went wrong. Please try again.')
      setSubmittedResults(null)
    } finally {
      setLoading(false)
    }
  }


  return (
    <section className="search-section">
      <div className="search-content">

        {/* HERO SEARCH DASHBOARD */}

        <div className="hero-layout">

          <div className="search-panel">
<p className="eyebrow">News Comparison</p>

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

              <button onClick={handleSearch} disabled={loading}>
                {loading ? 'Searching...' : 'Search Topic'}
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
                  {[... new Set(articles.map((article) => article.source))]
                    .filter(Boolean)
                    .sort()
                    .map((source) => (
                      <option key={source} value={source}>
                        {source}
                      </option>
                    ))}
                </select>
              </div>
            </div>

            <div className="feature-tags">
              <span>Article-level leaning</span>
              <span>Perspective comparison</span>
              <span>Timeline tracking</span>
              <span>Coverage gaps</span>
            </div>
          </div>

          {/* DASHBOARD METRICS */}

          <div className="metric-column">
            <div className="metric-card">
              <span className="metric-label">
                ARTICLES FOUND
              </span>
              <h2>{submittedResults ? filteredArticles.length : 0}</h2>
              <p>Articles in the current selection</p>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                SENTIMENT LABELS
              </span>
              <h2>{submittedResults ? new Set(filteredArticles.map(article => article.sentiment)).size : 0}</h2>
              <p>Sentiment labels</p>
            </div>

            <div className="metric-card">
              <span className="metric-label">
                TIMELINE POINTS
              </span>
              <h2>{submittedResults ? filteredArticles.length : 0}</h2>
              <p>Published entries in timeline</p>
            </div>
          </div>
        </div>

        {/* SEARCH FEEDBACK */}

        {loading && ( 
          <p className="loading-message" role="status">
            Searching for articles...
          </p>
        )}

        {error && (
          <p className="error-message">{error}</p>
        )}

        {submittedResults && filteredArticles.length === 0 && (
            <p className="no-result">
              {message || "No articles have been found for the given search criteria."}
            </p>
          )}

        {/* ARTICLE CAROUSEL */}

        {submittedResults && filteredArticles.length > 0 && (
          <ArticleCarousel articles={filteredArticles} />
        )}

        {/* RESULTS DASHBOARD */}

        {submittedResults && filteredArticles.length > 0 && (
          <div className="results-area">

            {/* SIDE-BY-SIDE ARTICLE COMPARISON */}

            <div className="results-heading">
              <div>
                <p className="section-kicker">ANALYSIS</p>
                <h2>Coverage, side by side.</h2>
                <p>Explore the articles and compare how each source approaches the story.</p>
              </div>
              <span className="results-count">{filteredArticles.length} articles</span>
            </div>

            <div className="comparison-articles-section" id="compare">
              <div className="section-heading">
                <div>
                  <p className="section-kicker">01 / ARTICLE COMPARISON</p>
                  <h2>Compare news coverage</h2>
                </div>
                <span className="section-note">Individual source analysis</span>
              </div>

              <div className="article-cards">
                {filteredArticles.map((article) => (
                  <ArticleCard
                    key={article.id}
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

            <div className="section-heading analysis-heading">
              <div>
                <p className="section-kicker">02 / KEY FINDINGS</p>
                <h2>What stands out?</h2>
              </div>
              <span className="section-note">A closer look at differences</span>
            </div>
            <div className="analysis-grid">
              <ComparisonSummary articles={filteredArticles} />
              <BiasCoverage articles={filteredArticles} />
            </div>

            {/* NARRATIVE Over Time */}

            <div className="timeline-wrap">
              <div className="section-heading">
                <div>
                  <p className="section-kicker">03 / STORY PROGRESSION</p>
                  <h2>Follow the narrative timeline</h2>
                </div>
              </div>
              <Timeline articles={filteredArticles} />
            </div>

          </div>
        )}
      </div>
    </section>
  )
}

export default SearchSection
