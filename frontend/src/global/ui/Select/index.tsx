import React, { useRef, useState } from 'react'
import classnames from 'classnames/bind'

import { ReactComponent as DropdownIcon } from '@assets/images/select_arrow.svg'
import { OptionList, Text } from '@global/ui'
import useOutsideClick from '@global/hook/useOutsideClick'
import styles from './Select.module.scss'

const cx = classnames.bind(styles)

interface SelectProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  value?: React.SelectHTMLAttributes<HTMLSelectElement>['value']
  defaultValue?: React.SelectHTMLAttributes<HTMLSelectElement>['defaultValue']
  className?: string
  children?: React.ReactNode

  colorScheme?: 'dark' | 'charcoal' | 'light'
  widthOption?: 'fit-content' | 'fit-wrapper'
}

/**
 * select 컴포넌트
 *
 * OptionList 및 OptionItem 컴포넌트를 select option으로 사용
 */
const Select: React.ForwardRefExoticComponent<SelectProps & React.RefAttributes<HTMLButtonElement>> = React.forwardRef<
  HTMLButtonElement,
  SelectProps
>(({ value, className, children, defaultValue, colorScheme = 'charcoal', widthOption, ...props }, ref) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [isFocused, setIsFocused] = useState<boolean>(false)
  const { ref: selectListRef } = useOutsideClick<HTMLUListElement>({ onClickOutside: () => setIsFocused(false) })

  if (selectListRef.current) {
    console.log(selectListRef.current.offsetHeight)
  }

  return (
    <div ref={divRef} className={cx('relative', className)}>
      <button
        ref={ref}
        type="button"
        aria-label="select"
        className={cx('flex justify-between items-center border rounded-lg py-3 px-4 w-full transition-colors', {
          'bg-white': colorScheme === 'light',
          'border-light-grey': colorScheme === 'light',
          'bg-charcoal': colorScheme === 'charcoal',
          'border-light-charcoal': colorScheme === 'charcoal',
          'bg-light-black': colorScheme === 'dark',
          'border-charcoal': colorScheme === 'dark',
          'border-primary': isFocused && !props.disabled,
        })}
        onClick={(e) => {
          setIsFocused((prev) => !prev)
          props.onClick?.(e)
        }}
        {...props}
      >
        <Text weight="bold" colorScheme={colorScheme === 'light' ? 'dark' : 'light'}>
          {value || defaultValue}
        </Text>
        <DropdownIcon className={cx('w-3', colorScheme)} />
      </button>

      <OptionList
        ref={selectListRef}
        isVisible={isFocused}
        widthOption={widthOption}
        wrapperRef={divRef}
        onClick={() => setIsFocused(false)}
        colorScheme={colorScheme}
      >
        {children}
      </OptionList>
    </div>
  )
})

Select.displayName = 'Select'

export default Select
