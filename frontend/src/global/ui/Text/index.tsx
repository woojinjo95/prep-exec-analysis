import React from 'react'
import cx from 'classnames'

interface TextProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
  weight?: 'regular' | 'medium' | 'bold'
}

/**
 * 텍스트 컴포넌트
 *
 * @param size 폰트크기
 */
const Text: React.FC<TextProps> = ({ children, size = 'md', weight = 'regular', ...props }) => {
  return (
    <span
      className={cx(
        'font-medium tracking-tighter text-black',
        {
          'text-sm': size === 'sm',
          'text-base': size === 'md',
          'text-lg': size === 'lg',
          'font-normal': weight === 'regular',
          'font-medium': weight === 'medium',
          'font-bold': weight === 'bold',
        },
        props.className,
      )}
      {...props}
    >
      {children}
    </span>
  )
}

export default Text
