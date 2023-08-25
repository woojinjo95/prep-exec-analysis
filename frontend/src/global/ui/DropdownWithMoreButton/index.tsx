import React, { useRef, useState } from 'react'
import { ReactComponent as MoreButton } from '@assets/images/button_more.svg'
import useOutsideClick from '@global/hook/useOutsideClick'
import cx from 'classnames'
import OptionList from '../OptionList'

interface DropdownWithMoreButtonProps {
  position?: 'topLeft' | 'topRight' | 'bottomLeft' | 'bottomRight'
  children?: React.ReactNode
  dropboxWidth?: number
}

const DropdownWithMoreButton: React.FC<DropdownWithMoreButtonProps> = ({ position, children, dropboxWidth = 154 }) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [isButtonClicked, setIsButtonClicked] = useState<boolean>(false)
  const { ref: selectListRef } = useOutsideClick<HTMLUListElement>({ onClickOutside: () => setIsButtonClicked(false) })

  return (
    <div className="relative" ref={divRef}>
      <MoreButton
        className="w-[20px] h-[20px] cursor-pointer"
        onClick={() => {
          setIsButtonClicked((prev) => !prev)
        }}
      />

      <OptionList
        ref={selectListRef}
        isVisible={isButtonClicked}
        wrapperRef={divRef}
        widthOption="fit-content"
        positionX="right"
        onClick={() => {
          setIsButtonClicked(false)
        }}
        colorScheme="light"
      >
        {children}
      </OptionList>
    </div>
  )
}

export default DropdownWithMoreButton
