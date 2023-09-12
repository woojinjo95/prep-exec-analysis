import React from 'react'
import cx from 'classnames'

interface SimpleButtonProps
  extends React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement> {
  isIcon?: boolean
  children: React.ReactNode | React.ReactNode[]
  colorScheme?: 'dark' | 'charcoal' | 'light-charcoal' | 'light' | 'grey'
}

/**
 * 간단한 버튼 컴포넌트
 *
 * @param isIcon 버튼안에 아이콘만 들어가는 경우. 아이콘 크기는 12px * 12px 권장
 */
const SimpleButton: React.FC<SimpleButtonProps> = ({
  isIcon = false,
  colorScheme = 'dark',
  className,
  children,
  ...props
}) => {
  return (
    <button
      type="button"
      className={cx(
        'rounded-md transition-colors flex items-center gap-x-3',
        {
          'py-1 px-3': !isIcon,
          'p-2': isIcon,

          'hover:bg-light-black': colorScheme === 'dark',
          'hover:bg-charcoal': colorScheme === 'charcoal',
          'hover:bg-light-charcoal': colorScheme === 'light-charcoal',
          'hover:bg-grey/50': colorScheme === 'grey',
          'hover:bg-[#F1F2F4]': colorScheme === 'light',
        },
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}

export default SimpleButton
