import React from 'react'
import cx from 'classnames'

interface SkeletonProps {
  className?: string
  colorScheme: 'light' | 'dark' | 'charcoal'
  isLoaded?: boolean
  children?: React.ReactNode | React.ReactNode[]
  style?: React.CSSProperties
}

/**
 * 스켈레톤 로딩 컴포넌트
 *
 * @param isLoaded 스켈레톤 로딩을 표현할지 여부. true = children 표시 및 스켈레톤 로딩 제거
 */
const Skeleton: React.FC<SkeletonProps> = ({ className, colorScheme, isLoaded, children, style }) => {
  return (
    <div
      className={cx([
        !isLoaded && [
          'animate-pulse',
          {
            'bg-light-black': colorScheme === 'dark',
            'bg-light-charcoal': colorScheme === 'charcoal',
            'bg-light-grey': colorScheme === 'light',
          },
        ],
        className,
      ])}
      style={style}
    >
      <div className={cx({ invisible: !isLoaded })}>{children}</div>
    </div>
  )
}

export default Skeleton
