import React from 'react'
import cx from 'classnames'

interface TitleProps {
  as?: 'h1' | 'h2' | 'h3'
  colorScheme?: 'dark' | 'charcoal' | 'light'
  active?: boolean
  className?: string
  children: React.ReactNode
}

/**
 * 타이틀 컴포넌트
 */
const Title: React.FC<TitleProps> = ({ as = 'h1', colorScheme = 'dark', active = true, className, children }) => {
  const style: cx.ArgumentArray = [
    {
      'text-white': colorScheme === 'light' || colorScheme === 'charcoal',
      'text-black': colorScheme === 'dark',
      '!text-grey': !active,

      'text-lg': as === 'h3',
      'text-xl': as === 'h2',
      'text-2xl': as === 'h1',

      '-tracking-[0.45px]': as === 'h3',
      '-tracking-[0.5px]': as === 'h2',
      '-tracking-[0.6px]': as === 'h1',

      'leading-[26px]': as === 'h3',
      'leading-6': as === 'h2' || as === 'h1',

      'font-medium': as === 'h3' || as === 'h2',
      'font-bold': as === 'h1',
    },
    className,
  ]

  if (as === 'h3') {
    return <h3 className={cx(style)}>{children}</h3>
  }
  if (as === 'h2') {
    return <h2 className={cx(style)}>{children}</h2>
  }
  return <h1 className={cx(style)}>{children}</h1>
}

export default Title
