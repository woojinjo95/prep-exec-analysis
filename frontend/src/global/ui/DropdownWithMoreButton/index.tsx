import React, { useRef, useState } from 'react'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import useOutsideClick from '@global/hook/useOutsideClick'
import OptionList from '../OptionList'
import { IconButton } from '..'

interface DropdownWithMoreButtonProps {
  children: React.ReactNode
}

const DropdownWithMoreButton: React.FC<DropdownWithMoreButtonProps> = ({ children }) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [isButtonClicked, setIsButtonClicked] = useState<boolean>(false)
  const { ref: selectListRef } = useOutsideClick<HTMLUListElement>({ onClickOutside: () => setIsButtonClicked(false) })

  return (
    <div className="relative" ref={divRef}>
      <IconButton
        className="w-[50px] h-[32px] "
        onClick={() => {
          setIsButtonClicked((prev) => !prev)
        }}
        icon={<MoreIcon className="w-[20px] h-[20px] cursor-pointer" />}
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
