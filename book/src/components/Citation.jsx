import React from 'react';

const Citation = ({ id, author, year, title, publisher }) => {
  // This is a placeholder component - in a real implementation,
  // this would render properly formatted APA citations
  return (
    <span className="citation" id={`citation-${id}`}>
      [{author}, {year}]
    </span>
  );
};

export default Citation;