import PoliticalLeaningIndicator from './PoliticalLeaningIndicator'
function ArticleCard({
  source,
  headline,
  summary,
  sentiment,
  perspective,
  publishedDate,
  url,
  politicalLeaning,
  keywords = []
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

            {keywords.length > 0 && (
        <div className="article-keywords">
          <h4>Related Cluster Keywords</h4>

          <div className="keyword-tags">
            {keywords.slice(0, 5).map((keyword) => (
              <span className="keyword-tag" key={keyword.text}>
                {keyword.text}
              </span>
            ))}
          </div>
        </div>
      )}

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

      <PoliticalLeaningIndicator leaning={politicalLeaning} />

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