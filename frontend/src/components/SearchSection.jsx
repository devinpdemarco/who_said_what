function SearchSection() {
  return (
    <section className="search-section">
      <div className="search-content">
        <h1>Compare the Story. See the Difference.</h1>

        <p>
          Search a news topic to compare how different sources are covering it.
        </p>

        <div className="search-bar">
          <input
            type="text"
            placeholder="Search a news topic..."
          />

          <button>Search</button>
        </div>
      </div>
    </section>
  )
}

export default SearchSection