import React from 'react'
import Scrollbars from 'react-custom-scrollbars-2'
import cx from 'classnames'

/**
 * react-custom-scrollbars-2를 활용한 Scroll Components
 * @param
 */

interface ScrollComponentProps {
  children: React.ReactNode
  className?: string
}

const ScrollComponent: React.FC<ScrollComponentProps> = ({ children, className }) => {
  return (
    <Scrollbars
      autoHide
      renderThumbVertical={({ ...props }) => (
        <div {...props} className={cx('bg-light-charcoal w-2 rounded-[5px] pr-2', className)} />
      )}
    >
      {children}
    </Scrollbars>
  )
}

export default ScrollComponent
