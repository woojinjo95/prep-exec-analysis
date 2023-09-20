import React, { useCallback } from 'react'
import cx from 'classnames'
import { createPortal } from 'react-dom'

/**
 * 리스트와 상위컴포넌트 사이의 간격
 */
const SPACE = 4

interface OptionListProps extends React.HTMLAttributes<HTMLUListElement> {
  children: React.ReactNode

  colorScheme?: 'dark' | 'charcoal' | 'light'
  isVisible?: boolean
  wrapperRef: React.MutableRefObject<HTMLDivElement | null>
  widthOption?: 'fit-content' | 'fit-wrapper'
  className?: string
  positionX?: 'left' | 'right'
}

/**
 * 옵션 리스트 컴포넌트
 *
 * OptionItem 컴포넌트와 같이 사용
 *
 * @param colorScheme 컬러 테마
 * @param isVisible OptionList 컴포넌트 표시여부
 * @param wrapperRef OptionList의 상위 엘리먼트 ref. 위치를 잡기위해 사용
 * @param widthOption 넓이 옵션. fit-wrapper: wrapperRef의 넓이를 사용 / fit-content: OptionList의 하위 엘리먼트 넓이 사용
 * @param positionX 위치 옵션. widthOption이 fit-content일 경우에만 사용가능. left: wrapperRef의 왼쪽으로 붙음 / right: wrapperRef의 오른쪽으로 붙음
 *
 *
 * FIXME: 스크롤 시 닫히도록
 *
 * FIXME: 위아래 고정 옵션
 *
 * FIXME: 화면을 벗어났을 경우 -> overflow-y-auto
 */
const OptionList: React.ForwardRefExoticComponent<OptionListProps & React.RefAttributes<HTMLUListElement>> =
  React.forwardRef<HTMLUListElement, OptionListProps>(
    (
      {
        children,
        colorScheme = 'charcoal',
        isVisible,
        widthOption = 'fit-wrapper',
        wrapperRef,
        positionX = 'left',
        className,
        ...props
      },
      ref,
    ) => {
      const createDefaultStyle = useCallback(
        (_wrapperRef: React.MutableRefObject<HTMLDivElement | null>) => {
          if (!_wrapperRef.current) return {}

          const styles: React.CSSProperties = {}
          const dimensions = _wrapperRef.current.getBoundingClientRect()

          if (widthOption === 'fit-content' && positionX === 'left') {
            styles.left = dimensions.left
          }
          if (widthOption === 'fit-content' && positionX === 'right') {
            styles.right = window.innerWidth - dimensions.left - dimensions.width
          }

          if (widthOption === 'fit-wrapper') {
            styles.left = dimensions.left
            styles.width = dimensions.width
          }

          if (dimensions.top < window.innerHeight / 2) {
            styles.top = dimensions.top + dimensions.height + SPACE
          } else {
            styles.bottom = window.innerHeight - dimensions.top + SPACE
          }

          return styles
        },
        [positionX, widthOption],
      )

      if (!isVisible) return null

      return createPortal(
        <ul
          ref={ref}
          className={cx(
            'fixed border rounded-lg p-[3px] grid grid-cols-1 gap-y-1 z-20 overflow-y-auto',
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
          style={createDefaultStyle(wrapperRef)}
          {...props}
        >
          {children}
        </ul>,
        document.body,
      )
    },
  )

OptionList.displayName = 'OptionList'

export default OptionList
