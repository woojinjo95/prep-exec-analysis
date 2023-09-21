import React from 'react'
import cx from 'classnames'

interface SkeletonProps {
  className?: string
  colorScheme: 'light' | 'dark' | 'charcoal'
  children?: React.ReactNode | React.ReactNode[]
  style?: React.CSSProperties
}

/**
 * 스켈레톤 로딩 컴포넌트
 */
const Skeleton: React.FC<SkeletonProps> = ({ className, colorScheme, children, style }) => {
  return (
    <div
      className={cx([
        'animate-pulse',
        {
          'bg-light-black': colorScheme === 'dark',
          'bg-light-charcoal': colorScheme === 'charcoal',
          'bg-light-grey': colorScheme === 'light',
        },
        className,
      ])}
      style={style}
    >
      <div className="invisible">{children}</div>
    </div>
  )
}

export default Skeleton
