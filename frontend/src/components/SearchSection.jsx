import { useState } from 'react'
function SearchSection() {
    const [searchTerm, setSearchTerm] = useState('')
    const [startDate, setStartDate] = useState('')
    const [endDate, setEndDate] = useState('')
    const [submittedResults, setSubmittedResults] = useState(null)
    const [error, setError] = useState('')

    function handleSearch() {
        if(!searchTerm || !startDate || !endDate) {
            setError('Please fill in all fields.')
            setSubmittedResults(null)
            return
        }
        if(startDate > endDate) {
            setError('Start date cannot be after end date.')
            setSubmittedResults(null)
            return
        }

        setError('')

        setSubmittedResults({
            searchTerm: searchTerm,
            startDate: startDate,
            endDate: endDate
        })
    }

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
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />

          <button onClick={handleSearch}>Search</button>
        </div>
        <div className="date-filters">
            <div className="date-field">
                <label htmlFor="start-date">From</label>
                <input 
                    type="date" 
                    id="start-date" 
                    value={startDate}
                    onChange={(event) => setStartDate(event.target.value)}
                />
            </div>

            <div className="date-field">
                <label htmlFor="end-date">To</label>
                <input 
                    type="date" 
                    id="end-date" 
                    value={endDate}
                    onChange={(event) => setEndDate(event.target.value)}
                />
            </div>
        </div>
        {error && (
            <p className="error-message">{error}</p>
        )}
        {submittedResults && (
            <div className="submitted-results">
                <h2>Search Results</h2>
                <p>
                    Showing results for: <strong>{submittedResults.searchTerm}</strong>
                </p>
                <p>
                    Date range: {submittedResults.startDate} to {submittedResults.endDate}
                </p>
            </div>
        )}
      </div>
    </section>
  )
}

export default SearchSection