import React from 'react'
import cx from 'classnames'

import Text from '../Text'

interface ButtonProps
  extends React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
  children: React.ReactNode
  colorScheme?: 'dark' | 'charcoal' | 'grey' | 'primary'
  size?: 'md' | 'sm'
  className?: string
  isRoundedFull?: boolean
}

/**
 * 버튼 컴포넌트
 *
 * @param isRoundedFull 모서리 둥글기, true면 완전히 동그래짐. false면 기본 rounded
 */
const Button: React.ForwardRefExoticComponent<Omit<ButtonProps, 'ref'> & React.RefAttributes<HTMLButtonElement>> =
  React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ children, colorScheme = 'charcoal', size = 'md', isRoundedFull = true, className, ...props }, ref) => {
      return (
        <button
          ref={ref}
          // eslint-disable-next-line react/button-has-type
          type="button"
          className={cx(
            'h-fit',
            {
              'py-3 px-10': size === 'md',
              'py-1 px-5': size === 'sm',
              'bg-light-black': colorScheme === 'dark',
              'bg-light-charcoal': colorScheme === 'charcoal',
              'bg-grey': colorScheme === 'grey',
              'bg-primary': colorScheme === 'primary',
              'rounded-full': isRoundedFull,
              'rounded-lg': !isRoundedFull,
              'grayscale-[.75] brightness-75': props.disabled,
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
    },
  )

Button.displayName = 'Button'

export default Button
