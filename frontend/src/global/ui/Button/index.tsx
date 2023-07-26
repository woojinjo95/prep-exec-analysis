import React from 'react'
import cx from 'classnames'

import Text from '../Text'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
}

/**
 * 버튼 컴포넌트
 */
const Button: React.FC<ButtonProps> = ({ children, type = 'button', ...props }) => {
  return (
    <button
      // eslint-disable-next-line react/button-has-type
      type={type}
      className={cx('shadow-[0px_1px_5px_#7777775E] px-4 py-1 rounded-full inline-flex items-center', props.className)}
      {...props}
    >
      {typeof children === 'string' && <Text size="sm">{children}</Text>}
      {typeof children !== 'string' && children}
    </button>
  )
}

export default Button
