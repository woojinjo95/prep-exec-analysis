import React from 'react'
import { MenuButton } from '@chakra-ui/react'
import { ReactComponent as DropdownIcon } from '@assets/images/dropdown.svg'
import classnames from 'classnames/bind'
import styles from './DropdownButton.module.scss'

const cx = classnames.bind(styles)

interface DropdownProps {
  children: React.ReactNode
  theme?: 'black' | 'white'
}

/**
 * 드롭다운
 *
 * @param theme 테마 색상
 *
 * TODO: 탭 시 드롭다운 리스트 내에서만 포커스 위치
 *
 * TODO: 방향키 위 아래 조절 시 선택될 아이템 배경색으로 표시? 포커싱?
 */
const DropdownButton: React.FC<DropdownProps> = ({ children, theme = 'black' }) => {
  return (
    <MenuButton className="w-[60%] flex justify-end">
      <div
        className={cx('flex justify-between px-2 py-1 border-b-[1px]', {
          'border-black': theme === 'black',
          'border-white': theme === 'white',
        })}
      >
        <p
          className={cx('font-medium text-[14px]', {
            'text-black': theme === 'black',
            'text-white': theme === 'white',
          })}
        >
          {children}
        </p>
        <DropdownIcon className={cx('w-[10px] rotate-180', theme)} />
      </div>
    </MenuButton>
  )
}

export default DropdownButton
