function ArticleCard({
  source,
  headline,
  summary,
  sentiment,
  perspective,
  publishedDate,
  url
}) {
  return (
    <article className="article-card">
      <div className="article-card-top">
        <span className="source-badge">
          {source}
        </span>

        <span className="article-date">
          {publishedDate}
        </span>
      </div>

      <h3>{headline}</h3>

      <p className="article-summary">
        {summary}
      </p>

      <div className="article-analysis">
        <div className="analysis-box">
          <span>Sentiment</span>
          <strong>{sentiment}</strong>
        </div>

        <div className="analysis-box">
          <span>Perspective</span>
          <strong>{perspective}</strong>
        </div>
      </div>

      <a
        className="article-link"
        href={url}
        target="_blank"
        rel="noreferrer"
      >
        Read full article
      </a>
    </article>
  )
}

export default ArticleCard