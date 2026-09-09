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
    <div className="article-card">
      <h3>{source}</h3>
      <p className="article-date">{publishedDate}</p>
      <h4>{headline}</h4>
      <p>{summary}</p>
      <div className="article-analysis">
        <p>Sentiment: <strong>{sentiment}</strong></p>
        <p>Perspective: <strong>{perspective}</strong></p>
      </div>
      <a href={url} target="_blank" rel="noreferrer">Read Full Article</a>
    </div>
  )
}

export default ArticleCard