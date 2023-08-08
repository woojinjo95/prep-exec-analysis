import React, { useCallback, useRef, useState } from 'react'
import classnames from 'classnames/bind'

import { ReactComponent as DropdownIcon } from '@assets/images/select_arrow.svg'
import { Portal, Text } from '@global/ui'
import useOutsideClick from '@global/hook/useOutsideClick'
import styles from './Select.module.scss'

/**
 * 리스트와 Select 버튼 사이의 간격
 */
const SPACE = 8

const cx = classnames.bind(styles)

interface SelectProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  value?: React.SelectHTMLAttributes<HTMLSelectElement>['value']
  defaultValue?: React.SelectHTMLAttributes<HTMLSelectElement>['defaultValue']
  className?: string
  children?: React.ReactNode

  colorScheme?: 'dark' | 'charcoal' | 'light'
}

/**
 * select 컴포넌트
 *
 * SelectOption 컴포넌트를 select option으로 사용
 */
const Select: React.ForwardRefExoticComponent<SelectProps & React.RefAttributes<HTMLButtonElement>> = React.forwardRef<
  HTMLButtonElement,
  SelectProps
>(({ value, className, children, defaultValue, colorScheme = 'charcoal', ...props }, ref) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const [isFocused, setIsFocused] = useState<boolean>(false)
  const { ref: selectListRef } = useOutsideClick<HTMLUListElement>({ onClickOutside: () => setIsFocused(false) })

  const createDefaultStyle = useCallback(
    (ref: React.MutableRefObject<HTMLDivElement | null>) => {
      if (!ref.current || !isFocused) return {}

      const styles: React.CSSProperties = {}
      const dimensions = ref.current.getBoundingClientRect()

      styles.left = dimensions.left

      if (dimensions.top < window.innerHeight / 2) {
        styles.top = dimensions.top + dimensions.height + SPACE
      } else {
        styles.bottom = window.innerHeight - dimensions.top + SPACE
      }

      return styles
    },
    [isFocused],
  )

  return (
    <div ref={divRef} className="relative">
      <button
        ref={ref}
        type="button"
        aria-label="select"
        className={cx(
          'flex justify-between items-center border rounded-lg py-3 px-4 w-full',
          {
            'bg-white': colorScheme === 'light',
            'border-light-grey': colorScheme === 'light',
            'bg-charcoal': colorScheme === 'charcoal',
            'border-light-charcoal': colorScheme === 'charcoal',
            'bg-light-black': colorScheme === 'dark',
            'border-charcoal': colorScheme === 'dark',
            'border-primary': isFocused,
          },
          className,
        )}
        onClick={(e) => {
          setIsFocused((prev) => !prev)
          props.onClick?.(e)
        }}
        {...props}
      >
        <Text size="sm" weight="bold" colorScheme={colorScheme === 'light' ? 'dark' : 'light'}>
          {value || defaultValue}
        </Text>
        <DropdownIcon className={cx('w-[10px]', colorScheme)} />
      </button>

      {isFocused && (
        <Portal>
          <ul
            ref={selectListRef}
            className="fixed bg-white"
            style={createDefaultStyle(divRef)}
            onClick={() => setIsFocused(false)}
          >
            {children}
          </ul>
        </Portal>
      )}
    </div>
  )
})

Select.displayName = 'Select'

export default Select
