import React from 'react'
import cx from 'classnames'

interface TextProps extends React.DetailedHTMLProps<React.HTMLAttributes<HTMLSpanElement>, HTMLSpanElement> {
  children: React.ReactNode
  className?: string
  size?: 'xs' | 'sm' | 'md'
  weight?: 'regular' | 'medium' | 'bold'
  isActive?: boolean
  colorScheme?:
    | 'dark'
    | 'light'
    | 'pink'
    | 'red'
    | 'orange'
    | 'yellow'
    | 'navy'
    | 'green'
    | 'grey'
    | 'dark-grey'
    | 'light-orange'
  invertBackground?: boolean
}

/**
 * 텍스트 컴포넌트
 *
 * @param size 폰트크기
 * @param invertBackground 글자색 대신 글자 배경에 색을 입히는 옵션
 */
const Text: React.FC<TextProps> = ({
  children,
  className,
  size = 'md',
  weight = 'regular',
  colorScheme = 'light',
  isActive = true,
  invertBackground = false,
  ...props
}) => {
  return (
    <span
      className={cx(
        'tracking-tighter text-black',
        {
          'text-[13px]': size === 'xs', // tooltip
          'text-[15px]': size === 'sm', // button, input, select
          'text-base': size === 'md',

          'font-light': weight === 'regular',
          'font-medium': weight === 'medium',
          'font-bold': weight === 'bold',
        },
        !invertBackground && {
          'text-white': colorScheme === 'light',
          'text-black': colorScheme === 'dark',
          'text-pink': colorScheme === 'pink',
          'text-red': colorScheme === 'red',
          'text-orange': colorScheme === 'orange',
          'text-yellow': colorScheme === 'yellow',
          'text-navy': colorScheme === 'navy',
          'text-green': colorScheme === 'green',
          'text-grey': !isActive || colorScheme === 'grey',
        },
        invertBackground && {
          'px-1.5 py-px': true,
          'text-white': colorScheme !== 'light' && colorScheme !== 'yellow',
          'text-black': colorScheme === 'light' || colorScheme === 'yellow',

          'bg-black': colorScheme === 'dark',
          'bg-white': colorScheme === 'light',
          'bg-pink': colorScheme === 'pink',
          'bg-red': colorScheme === 'red',
          'bg-orange': colorScheme === 'orange',
          'bg-yellow': colorScheme === 'yellow',
          'bg-navy': colorScheme === 'navy',
          'bg-green': colorScheme === 'green',
          'bg-grey': colorScheme === 'grey',
          'bg-dark-grey': colorScheme === 'dark-grey',
          'bg-light-orange': colorScheme === 'light-orange',
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
