import React from 'react'
import classnames from 'classnames/bind'
import styles from './Skeleton.module.scss'

const cx = classnames.bind(styles)

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
    <div className={cx(['skeleton', className, colorScheme])} style={style}>
      {children}
    </div>
  )
}

export default Skeleton
