import React from 'react'
import cx from 'classnames'
import { Text } from '..'

interface OptionItemProps extends React.LiHTMLAttributes<HTMLLIElement> {
  children: React.ReactNode

  colorScheme?: 'dark' | 'charcoal' | 'light'
  isActive?: boolean
  disabled?: boolean
}

/**
 * OptionList 아이템 컴포넌트
 *
 * OptionList 컴포넌트와 같이 사용
 */
const OptionItem: React.FC<OptionItemProps> = ({
  children,
  colorScheme = 'charcoal',
  isActive,
  disabled,
  ...props
}) => {
  return (
    <li
      className={cx(
        'rounded-[4px] px-3 py-2 cursor-pointer truncate hover:backdrop-brightness-110',
        {
          'bg-charcoal': colorScheme === 'dark' && isActive,
          'bg-light-charcoal': colorScheme === 'charcoal' && isActive,
          'bg-[#F1F2F4]': colorScheme === 'light' && isActive,
          '!bg-light-grey': colorScheme === 'light' && disabled,

          'hover:bg-charcoal': colorScheme === 'dark',
          'hover:bg-light-charcoal': colorScheme === 'charcoal',
          'hover:bg-[#F1F2F4]': colorScheme === 'light',
          '!hover:bg-light-grey': colorScheme === 'light' && disabled,
        },
        props.className,
      )}
      {...props}
    >
      <Text size="sm" colorScheme={colorScheme === 'light' ? 'dark' : 'light'}>
        {children}
      </Text>
    </li>
  )
}

export default OptionItem
