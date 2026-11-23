import { useState } from 'react'
import PoliticalLeaningIndicator from './PoliticalLeaningIndicator'

function ArticleCarousel({ articles, clusters = [] }) {
  const [currentIndex, setCurrentIndex] = useState(0)

  if (articles.length === 0) {
    return null
  }

  const safeIndex = Math.min(currentIndex, articles.length - 1)
  const article = articles[safeIndex]
  const cluster = clusters.find(
    (cluster) => cluster.cluster_id === article.clusterId
  )

  const keywords = cluster?.keywords ?? []

  return (
    <section className="article-carousel">
      <div className="carousel-header">
        <h2>Browse Articles</h2>
        <span>
          {safeIndex + 1} of {articles.length}
        </span>
      </div>

      <div className="carousel-article">
        <span className="carousel-source">
          {article.source}
        </span>

        <h3>{article.headline}</h3>

        <p>{article.excerpt || article.summary}</p>

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

        <PoliticalLeaningIndicator
          leaning={article.politicalLeaning}
        />
      </div>

      <div className="carousel-navigation">
        <button
          disabled={safeIndex === 0}
          onClick={() => setCurrentIndex(safeIndex - 1)}
        >
          ← Previous
        </button>

        <button
          disabled={safeIndex === articles.length - 1}
          onClick={() => setCurrentIndex(safeIndex + 1)}
        >
          Next →
        </button>
      </div>
    </section>
  )
}

export default ArticleCarousel