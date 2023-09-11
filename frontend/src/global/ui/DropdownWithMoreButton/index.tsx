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
  positionX?: 'left' | 'right'
  iconColorScheme?: 'light' | 'charcoal'
  disabled?: boolean
}

/**
 *
 * @param type 버튼 모양 타입. icon-button: 테두리 있는 아이콘 버튼 / icon: 테두리 없는 아이콘
 */
const DropdownWithMoreButton: React.FC<DropdownWithMoreButtonProps> = ({
  children,
  colorScheme = 'light',
  type = 'icon-button',
  positionX = 'right',
  iconColorScheme,
  disabled,
}) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [isButtonClicked, setIsButtonClicked] = useState<boolean>(false)
  const { ref: selectListRef } = useOutsideClick<HTMLUListElement>({ onClickOutside: () => setIsButtonClicked(false) })

  return (
    <div className="relative" ref={divRef}>
      {type === 'icon-button' && (
        <IconButton
          colorScheme={colorScheme}
          className={cx('w-[50px] h-8', {
            '!bg-light-grey': colorScheme === 'light' && disabled,
            // TODO : colorScheme가 light가 아닐 떄
          })}
          onClick={(e) => {
            e.stopPropagation()
            if (disabled) return

            setIsButtonClicked((prev) => !prev)
          }}
          icon={<MoreIcon className="w-[20px] h-[20px] cursor-pointer" />}
        />
      )}
      {type === 'icon' && (
        <MoreIcon
          className={cx(
            'dropdown-with-more-button-icon',
            iconColorScheme || colorScheme,
            'w-[20px] h-[20px] cursor-pointer',
          )}
          onClick={(e) => {
            e.stopPropagation()
            setIsButtonClicked((prev) => !prev)
          }}
        />
      )}

      <OptionList
        ref={selectListRef}
        isVisible={isButtonClicked}
        wrapperRef={divRef}
        widthOption="fit-content"
        positionX={positionX}
        onClick={() => {
          if (disabled) return
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
