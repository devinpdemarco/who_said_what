// ArticleCarousel component for displaying a carousel of articles
import { useState } from 'react'
import PoliticalLeaningIndicator from './PoliticalLeaningIndicator'

function ArticleCarousel({ articles }) {
  const [currentIndex, setCurrentIndex] = useState(0)

  if (articles.length === 0) {
    return null
  }

  const article = articles[currentIndex]

  return (
    <section className="article-carousel">
      <div className="carousel-header">
        <h2>Browse Articles</h2>
        <span>
          {currentIndex + 1} of {articles.length}
        </span>
      </div>

      <div className="carousel-article">
        <span className="carousel-source">
          {article.source}
        </span>

        <h3>{article.headline}</h3>

        <p>{article.excerpt || article.summary}</p>

        <PoliticalLeaningIndicator
          leaning={article.politicalLeaning}
        />
      </div>

      <div className="carousel-navigation">
        <button
          disabled={currentIndex === 0}
          onClick={() => setCurrentIndex(currentIndex - 1)}
        >
          ← Previous
        </button>

        <button
          disabled={currentIndex === articles.length - 1}
          onClick={() => setCurrentIndex(currentIndex + 1)}
        >
          Next →
        </button>
      </div>
    </section>
  )
}

export default ArticleCarousel