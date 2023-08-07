import React from 'react'
import { MenuButton } from '@chakra-ui/react'
import { Text } from '@global/ui'
import { ReactComponent as DropdownIcon } from '@assets/images/select_arrow.svg'
import classnames from 'classnames/bind'
import styles from './DropdownButton.module.scss'

const cx = classnames.bind(styles)

interface DropdownProps {
  children: React.ReactNode
  colorScheme?: 'dark' | 'charcoal' | 'light'
  className?: string
}

/**
 * 드롭다운
 *
 * @param colorScheme 컬러 테마 색상
 *
 * TODO: 탭 시 드롭다운 리스트 내에서만 포커스 위치
 *
 * TODO: 방향키 위 아래 조절 시 선택될 아이템 배경색으로 표시? 포커싱?
 */
const DropdownButton: React.FC<DropdownProps> = ({ children, colorScheme = 'light', className }) => {
  return (
    <MenuButton className="flex justify-end">
      <div
        className={cx(
          'flex justify-between border rounded-lg py-3 px-4',
          {
            'bg-white': colorScheme === 'light',
            'border-light-grey': colorScheme === 'light',
            'bg-charcoal': colorScheme === 'charcoal',
            'border-light-charcoal': colorScheme === 'charcoal',
            'bg-light-black': colorScheme === 'dark',
            'border-charcoal': colorScheme === 'dark',
          },
          className,
        )}
      >
        <Text size="sm" weight="bold" colorScheme={colorScheme === 'light' ? 'dark' : 'light'}>
          {children}
        </Text>
        <DropdownIcon className={cx('w-[10px]', colorScheme)} />
      </div>
    </MenuButton>
  )
}

export default DropdownButton
