import React from 'react'
import cx from 'classnames'

interface TextProps extends React.DetailedHTMLProps<React.HTMLAttributes<HTMLSpanElement>, HTMLSpanElement> {
  children: React.ReactNode
  className?: string
  size?: 'xs' | 'sm' | 'md'
  weight?: 'regular' | 'medium' | 'bold'
  isActive?: boolean
  colorScheme?: 'dark' | 'light'
}

/**
 * 텍스트 컴포넌트
 *
 * @param size 폰트크기
 */
const Text: React.FC<TextProps> = ({
  children,
  className,
  size = 'md',
  weight = 'regular',
  colorScheme = 'light',
  isActive = true,
  ...props
}) => {
  return (
    <span
      className={cx(
        'tracking-tighter text-black',
        {
          'text-[13px]': size === 'xs',
          'text-[15px]': size === 'sm',
          'text-base': size === 'md',
          'font-light': weight === 'regular',
          'font-medium': weight === 'medium',
          'font-bold': weight === 'bold',
          'text-white': colorScheme === 'light',
          'text-black': colorScheme === 'dark',
          '!text-grey': !isActive,
        },
        className,
      )}
      {...props}
    >
      {children}
    </span>
  )
}

export default Text
