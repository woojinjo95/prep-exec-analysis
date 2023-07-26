import React from 'react'
import { MenuButton } from '@chakra-ui/react'
import { ReactComponent as DropdownIcon } from '@assets/images/dropdown.svg'

interface DropdownProps {
  children: React.ReactNode
}

/**
 * 드롭다운
 *
 * TODO: 탭 시 드롭다운 리스트 내에서만 포커스 위치
 * TODO: 방향키 위 아래 조절 시 선택될 아이템 배경색으로 표시? 포커싱?
 */
const DropdownButton: React.FC<DropdownProps> = ({ children }) => {
  return (
    <MenuButton className="w-[60%] flex justify-end">
      <div className="flex justify-between pr-[5px] pl-[5px] border-b-[1px] border-black">
        <p className="pl-[8px] font-medium text-[14px]">{children}</p>
        <DropdownIcon className="w-[10px] rotate-180" />
      </div>
    </MenuButton>
  )
}

export default DropdownButton
