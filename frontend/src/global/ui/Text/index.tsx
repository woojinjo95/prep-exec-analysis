import React from 'react'
import cx from 'classnames'

interface TextProps extends React.DetailedHTMLProps<React.HTMLAttributes<HTMLSpanElement>, HTMLSpanElement> {
  children: React.ReactNode
  className?: string
  size?: 'sm' | 'md' | 'lg'
  weight?: 'regular' | 'medium' | 'bold'
  theme?: 'dark' | 'light'
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
  theme = 'light',
  ...props
}) => {
  return (
    <span
      className={cx(
        'tracking-tighter text-black',
        {
          'text-sm': size === 'sm',
          'text-base': size === 'md',
          'text-lg': size === 'lg',
          'font-normal': weight === 'regular',
          'font-medium': weight === 'medium',
          'font-bold': weight === 'bold',
          'text-black': theme === 'light',
          'text-white': theme === 'dark',
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
