function ComparisonSummary({ articles }) {
  if (articles.length < 2) {
    return null
  }

  const sentiments = [...new Set(
    articles.map((article) => article.sentiment)
  )]

  const perspectives = [...new Set(
    articles.map((article) => article.perspective)
  )]

  return (
    <section className="comparison-summary" id="compare">
      <div className="comparison-summary-header">
        <p className="comparison-eyebrow">
          COMPARISON SUMMARY
        </p>

        <h3>
          What changes between perspectives?
        </h3>
      </div>

      <div className="comparison-insights">
        <div className="insight-card">
          <h4>Articles compared</h4>
          <p>{articles.length} sources are included in this comparison.</p>
        </div>

        <div className="insight-card">
          <h4>Tone difference</h4>
          <p>
            Sentiments found: {sentiments.join(', ')}
          </p>
        </div>

        <div className="insight-card">
          <h4>Perspective difference</h4>
          <p>
            Perspectives found: {perspectives.join(', ')}
          </p>
        </div>

        <div className="insight-card">
          <h4>Coverage insight</h4>
          <p>
            Different sources may emphasize different details, priorities,
            and interpretations of the same story.
          </p>
        </div>
      </div>
    </section>
  )
}

export default ComparisonSummary