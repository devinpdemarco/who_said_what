function Timeline ({ articles }) {
    return (
        <div className="timeline" id="timeline">
            <h3>Story Timeline</h3>
        
        {[...articles]
            .sort(
                (a,b) =>
                    new Date(a.publishedDate) - new Date(b.publishedDate)
            )
            .map((article) => (
            <div className="timeline-item" key={article.headline}>
                <strong>{article.publishedDate}</strong>
            
                <p>
                    {article.source}: {article.headline}
                </p>
            </div>
        ))}
        </div>
    )
}

export default Timeline