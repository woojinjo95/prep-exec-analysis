import React from 'react'
import cx from 'classnames'

import Text from '../Text'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
  variant?: 'outline' | 'unstyled'
}

/**
 * 버튼 컴포넌트
 *
 * @param variant 버튼 스타일
 */
const Button: React.FC<ButtonProps> = ({ children, type = 'button', variant = 'outline', ...props }) => {
  return (
    <button
      // eslint-disable-next-line react/button-has-type
      type={type}
      className={cx(
        'px-4 py-1 rounded-full inline-flex items-center hover:bg-slate-100 active:bg-slate-200 transition-colors',
        {
          'shadow-[0px_1px_5px_#7777775E]': variant === 'outline',
        },
        props.className,
      )}
      {...props}
    >
      {typeof children === 'string' && (
        <Text size="sm" weight="medium">
          {children}
        </Text>
      )}
      {typeof children !== 'string' && children}
    </button>
  )
}

export default Button
