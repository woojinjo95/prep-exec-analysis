import React from 'react'
import cx from 'classnames'

interface ButtonGroupProps {
  colorScheme?: 'dark' | 'charcoal' | 'light'
  children: React.ReactNode
}

/**
 * 버튼 그룹 컴포넌트
 *
 * GroupButton를 하위 컴포넌트로 사용
 */
const ButtonGroup: React.FC<ButtonGroupProps> = ({ colorScheme = 'charcoal', children }) => {
  return (
    <div
      className={cx('flex items-center border p-[3px] rounded-lg w-fit', {
        'bg-charcoal': colorScheme === 'charcoal',
        'border-light-charcoal': colorScheme === 'charcoal',
      })}
    >
      {children}
    </div>
  )
}

export default ButtonGroup
