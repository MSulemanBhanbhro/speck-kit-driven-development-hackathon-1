import React, { useState } from 'react';
import clsx from 'clsx';

const Spoiler = ({ title, children }) => {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <details
      className={clsx('spoiler', 'margin-top--md', 'margin-bottom--md')}
      onClick={(e) => e.preventDefault()}
    >
      <summary className="spoiler-summary">
        {title || 'Spoiler'}
      </summary>
      <div className="spoiler-content">
        {children}
      </div>
    </details>
  );
};

export default Spoiler;