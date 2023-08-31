import React from 'react'

interface DividerProps {
  direction?: 'horizontal' | 'vertical'
}

/**
 * 구분선 컴포넌트
 */
const Divider: React.FC<DividerProps> = ({ direction = 'horizontal' }) => {
  if (direction === 'horizontal') return <div className="bg-light-charcoal w-full h-px mt-4 mb-5" />

  return <div />
}

export default Divider
