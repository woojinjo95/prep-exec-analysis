import React from 'react'
import cx from 'classnames'

import Text from '../Text'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
  colorScheme?: 'dark' | 'charcoal' | 'grey' | 'primary'
  className?: string
  isRoundedFull?: boolean
}

/**
 * 버튼 컴포넌트
 *
 * @param variant 버튼 스타일
 */
const Button: React.FC<ButtonProps> = ({
  children,
  colorScheme = 'charcoal',
  isRoundedFull = true,
  className,
  ...props
}) => {
  return (
    <button
      // eslint-disable-next-line react/button-has-type
      type="button"
      className={cx(
        'py-3 px-10',
        {
          'bg-light-black': colorScheme === 'dark',
          'bg-light-charcoal': colorScheme === 'charcoal',
          'bg-grey': colorScheme === 'grey',
          'bg-primary': colorScheme === 'primary',
          'rounded-full': isRoundedFull,
          'rounded-lg': !isRoundedFull,
        },
        className,
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
