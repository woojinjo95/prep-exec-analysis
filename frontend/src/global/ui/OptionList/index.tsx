import React, { useCallback } from 'react'
import cx from 'classnames'
import { Portal } from '..'

/**
 * 리스트와 Select 버튼 사이의 간격
 */
const SPACE = 8

interface OptionListProps extends React.HTMLAttributes<HTMLUListElement> {
  children: React.ReactNode

  colorScheme?: 'dark' | 'charcoal' | 'light'
  isVisible?: boolean
  wrapperRef: React.MutableRefObject<HTMLDivElement | null>
}

/**
 * 옵션 리스트 컴포넌트
 *
 * OptionItem 컴포넌트와 같이 사용
 */
const OptionList: React.ForwardRefExoticComponent<OptionListProps & React.RefAttributes<HTMLUListElement>> =
  React.forwardRef<HTMLUListElement, OptionListProps>(
    ({ children, colorScheme = 'charcoal', isVisible, wrapperRef, ...props }, ref) => {
      const createDefaultStyle = useCallback((ref: React.MutableRefObject<HTMLDivElement | null>) => {
        if (!ref.current) return {}

        const styles: React.CSSProperties = {}
        const dimensions = ref.current.getBoundingClientRect()

        styles.left = dimensions.left
        styles.width = dimensions.width

        if (dimensions.top < window.innerHeight / 2) {
          styles.top = dimensions.top + dimensions.height + SPACE
        } else {
          styles.bottom = window.innerHeight - dimensions.top + SPACE
        }

        return styles
      }, [])

      if (!isVisible) return null
      return (
        <Portal>
          <ul
            ref={ref}
            className={cx(
              'fixed border rounded-lg p-[3px] grid grid-cols-1 gap-y-1',
              {
                'bg-white': colorScheme === 'light',
                'border-light-grey': colorScheme === 'light',
                'bg-charcoal': colorScheme === 'charcoal',
                'border-light-charcoal': colorScheme === 'charcoal',
                'bg-light-black': colorScheme === 'dark',
                'border-charcoal': colorScheme === 'dark',
              },
              props.className,
            )}
            style={createDefaultStyle(wrapperRef)}
            {...props}
          >
            {children}
          </ul>
        </Portal>
      )
    },
  )

OptionList.displayName = 'OptionList'

export default OptionList
