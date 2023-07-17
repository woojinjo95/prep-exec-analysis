import React from 'react'
import cx from 'classnames'

interface PageContainerProps {
  children: React.ReactNode
  className?: string
}

/**
 * 페이지를 감싸는 컴포넌트
 */
const PageContainer: React.FC<PageContainerProps> = ({ children, className }) => {
  return <div className={cx('w-screen h-screen py-2 px-4 gap-2', className)}>{children}</div>
}

export default PageContainer
