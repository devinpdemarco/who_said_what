const positions = [
  'Left',
  'Center-left',
  'Center',
  'Center-right',
  'Right'
]

function PoliticalLeaningIndicator({ leaning }) {
  const validLeaning = positions.includes(leaning)
    ? leaning
    : null

  return (
    <div className="political-indicator">
      <div className="political-indicator-header">
        <span>Estimated political leaning</span>
        <strong>{validLeaning || 'Not analyzed'}</strong>
      </div>

      <div className="political-scale">
        {positions.map((position) => (
          <div
            key={position}
            className={
              'political-segment ' +
              (position === validLeaning ? 'active' : '')
            }
          >
            <span className="political-segment-bar" />
            <span className="political-segment-label">
              {position}
            </span>
          </div> 
        ))}
      </div>
    </div>
  )
}

export default PoliticalLeaningIndicator