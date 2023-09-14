import React, { useCallback, useState } from 'react'
import cx from 'classnames'

/**
 * 스크롤바 높이 사이즈
 */
const SCROLL_BAR_HEIGHT = 12

interface HorizontalScrollBarProps {
  scrollBarTwoPosX: [number, number] | null
  setScrollBarTwoPosX: React.Dispatch<React.SetStateAction<[number, number] | null>>
  dimension: { left: number; width: number } | null
}

/**
 * 타임라인 차트 가로 스크롤바
 */
const HorizontalScrollBar: React.FC<HorizontalScrollBarProps> = ({
  scrollBarTwoPosX,
  setScrollBarTwoPosX,
  dimension,
}) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)

  const onPointerDownHandler: React.PointerEventHandler<HTMLDivElement> = useCallback((e) => {
    e.stopPropagation()
    e.currentTarget.setPointerCapture(e.pointerId)
    setIsDragging(true)
  }, [])
  const onPointerUpHandler: React.PointerEventHandler<HTMLDivElement> = useCallback((e) => {
    e.currentTarget.releasePointerCapture(e.pointerId)
    setIsDragging(false)
  }, [])

  if (dimension === null || scrollBarTwoPosX === null) return <div style={{ height: SCROLL_BAR_HEIGHT }} />

  return (
    <div className="text-white">
      {/* 스크롤바 */}
      <div
        className="w-full bg-gray-600 rounded-full flex justify-between cursor-grab relative"
        style={{
          width: `${scrollBarTwoPosX[1] - scrollBarTwoPosX[0]}px`,
          minWidth: SCROLL_BAR_HEIGHT,
          height: SCROLL_BAR_HEIGHT,
          maxWidth: `${dimension.width}px`,
          transform: `translateX(${scrollBarTwoPosX[0]}px)`,
        }}
        onPointerDown={onPointerDownHandler}
        onPointerMove={(e) => {
          e.preventDefault()
          if (!isDragging) return

          // FIXME: clientX 기반으로 대체
          if (scrollBarTwoPosX[0] + e.movementX < 0) {
            setScrollBarTwoPosX([0, scrollBarTwoPosX[1] - scrollBarTwoPosX[0]])
            return
          }
          if (scrollBarTwoPosX[1] + e.movementX > dimension.width) {
            setScrollBarTwoPosX([scrollBarTwoPosX[0] + (dimension.width - scrollBarTwoPosX[1]), dimension.width])
            return
          }

          setScrollBarTwoPosX([scrollBarTwoPosX[0] + e.movementX, scrollBarTwoPosX[1] + e.movementX])
        }}
        onPointerUp={onPointerUpHandler}
        onLostPointerCapture={onPointerUpHandler}
      >
        {/* 스크롤바 왼쪽 조절 버튼 */}
        <div
          className={cx('rounded-full border-[3px] border-gray-400 cursor-ew-resize absolute top-0 left-0', {
            'z-[5]': scrollBarTwoPosX[0] === scrollBarTwoPosX[1] - SCROLL_BAR_HEIGHT,
          })}
          style={{
            width: SCROLL_BAR_HEIGHT,
            height: SCROLL_BAR_HEIGHT,
          }}
          onPointerDown={onPointerDownHandler}
          onPointerMove={(e) => {
            e.preventDefault()
            e.stopPropagation()
            if (!isDragging || !dimension.left) return

            setScrollBarTwoPosX([
              Math.min(
                Math.max(0, e.clientX - dimension.left - SCROLL_BAR_HEIGHT / 2),
                scrollBarTwoPosX[1] - SCROLL_BAR_HEIGHT,
              ),
              scrollBarTwoPosX[1],
            ])
          }}
          onPointerUp={onPointerUpHandler}
          onLostPointerCapture={onPointerUpHandler}
        />

        {/* 스크롤바 오른쪽 조절 버튼 */}
        <div
          className={cx('rounded-full border-[3px] border-gray-400 cursor-ew-resize  absolute top-0 right-0', {
            'z-[5]': scrollBarTwoPosX[1] === SCROLL_BAR_HEIGHT,
          })}
          style={{
            width: SCROLL_BAR_HEIGHT,
            height: SCROLL_BAR_HEIGHT,
          }}
          onPointerDown={onPointerDownHandler}
          onPointerMove={(e) => {
            e.preventDefault()
            e.stopPropagation()
            if (!isDragging || !dimension.left) return

            setScrollBarTwoPosX([
              scrollBarTwoPosX[0],
              Math.max(
                scrollBarTwoPosX[0] + SCROLL_BAR_HEIGHT,
                Math.min(dimension.width, e.clientX - dimension.left + SCROLL_BAR_HEIGHT / 2),
              ),
            ])
          }}
          onPointerUp={onPointerUpHandler}
          onLostPointerCapture={onPointerUpHandler}
        />
      </div>
    </div>
  )
}

export default HorizontalScrollBar
