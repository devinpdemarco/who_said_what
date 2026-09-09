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
    <div className="comparison-summary" id="compare">
      <h3>Coverage Comparison</h3>

      <p>
        <strong>Articles compared:</strong> {articles.length}
      </p>

      <p>
        <strong>Sentiments found:</strong> {sentiments.join(', ')}
      </p>

      <p>
        <strong>Perspectives found:</strong> {perspectives.join(', ')}
      </p>
    </div>
  )
}

export default ComparisonSummary