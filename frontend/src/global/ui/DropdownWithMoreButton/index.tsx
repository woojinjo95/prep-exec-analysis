import React, { useRef, useState } from 'react'
import classnames from 'classnames/bind'
import { ReactComponent as MoreIcon } from '@assets/images/button_more.svg'
import useOutsideClick from '@global/hook/useOutsideClick'
import OptionList from '../OptionList'
import { IconButton } from '..'
import styles from './DropdownWithMoreButton.module.scss'

const cx = classnames.bind(styles)

interface DropdownWithMoreButtonProps {
  children: React.ReactNode
  colorScheme?: 'light' | 'charcoal'
  type?: 'icon-button' | 'icon'
}

const DropdownWithMoreButton: React.FC<DropdownWithMoreButtonProps> = ({
  children,
  colorScheme = 'light',
  type = 'icon-button',
}) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [isButtonClicked, setIsButtonClicked] = useState<boolean>(false)
  const { ref: selectListRef } = useOutsideClick<HTMLUListElement>({ onClickOutside: () => setIsButtonClicked(false) })

  return (
    <div className="relative" ref={divRef}>
      {type === 'icon-button' && (
        <IconButton
          colorScheme={colorScheme}
          className="w-[50px] h-8"
          onClick={() => {
            setIsButtonClicked((prev) => !prev)
          }}
          icon={<MoreIcon className="w-[20px] h-[20px] cursor-pointer" />}
        />
      )}
      {type === 'icon' && (
        <MoreIcon
          className={cx('dropdown-with-more-button-icon', colorScheme, 'w-[20px] h-[20px] cursor-pointer')}
          onClick={() => {
            setIsButtonClicked((prev) => !prev)
          }}
        />
      )}

      <OptionList
        ref={selectListRef}
        isVisible={isButtonClicked}
        wrapperRef={divRef}
        widthOption="fit-content"
        positionX="right"
        onClick={() => {
          setIsButtonClicked(false)
        }}
        colorScheme={colorScheme}
      >
        {children}
      </OptionList>
    </div>
  )
}

export default DropdownWithMoreButton
