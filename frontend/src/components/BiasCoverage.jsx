function BiasCoverage({ articles }) {
    if (articles.length === 0) {
        return null
    }

    return (
        <section className="bias-coverage" id="coverage">
            <div className="bias-header">
                <p className="bias-eyebrow">
                </p>
                <h3>
                    How different sources frame the story
                </h3>

                <p className="bia-description">
                    Compare perspective, tone, emphasis across different news sources.
                </p>
            </div>

            <div className="bias-grid">
                {articles.map((article) => (
                    <div
                    className="bias-card"
                    key={article.headline}
                    >
                        <div className="bias-card-header">
                            <span className="bias-source">
                                {article.source}
                            </span>

                            <span className="bias-sentiment">
                                {article.sentiment}
                            </span>
        
                        </div>

                        <h4>{article.headline}</h4>

                        <div className="bias-detail">
                            <span>Perspective</span>
                            <strong>{article.perspective}</strong>
                        </div>

                        <div className="bias-detail">
                            <span>Coverage focus</span>
                            <strong>
                                Example
                            </strong>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    )
}

export default BiasCoverage