function Timeline({ articles }) {
  const sortedArticles = [...articles].sort(
    (a, b) =>
      new Date(a.publishedDate) - new Date(b.publishedDate)
  )

  return (
    <section className="timeline" id="timeline">
      <div className="timeline-header">
        <p className="timeline-eyebrow">
          TIMELINE
        </p>

        <h3>
          How the story develops over time
        </h3>
      </div>

      <div className="timeline-list">
        {sortedArticles.map((article, index) => (
          <div
            className="timeline-item"
            key={article.headline}
          >
            <div className="timeline-marker">
              {index + 1}
            </div>

            <div className="timeline-content">
              <span className="timeline-date">
                {article.publishedDate}
              </span>

              <h4>
                {article.source}
              </h4>

              <p>
                {article.headline}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default Timeline