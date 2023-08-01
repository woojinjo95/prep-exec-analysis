import React, { useCallback, useState } from 'react'

/**
 * 스크롤바 높이 사이즈
 */
const SCROLL_BAR_HEIGHT = 12

interface HorizontalScrollBarProps {
  chartWidth: number | null
  scrollBarTwoPosX: [number, number] | null
  setScrollBarTwoPosX: React.Dispatch<React.SetStateAction<[number, number] | null>>
}

/**
 * 타임라인 차트 가로 스크롤바
 */
const HorizontalScrollBar: React.FC<HorizontalScrollBarProps> = ({
  chartWidth,
  scrollBarTwoPosX,
  setScrollBarTwoPosX,
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

  if (chartWidth === null || scrollBarTwoPosX === null) return <div style={{ height: SCROLL_BAR_HEIGHT }} />

  return (
    <div className="text-white">
      {/* 스크롤바 */}
      <div
        className="w-full h-3 min-w-3 bg-gray-600 rounded-full flex justify-between cursor-grab relative"
        style={{
          width: `${scrollBarTwoPosX[1] - scrollBarTwoPosX[0]}px`,
          height: SCROLL_BAR_HEIGHT,
          maxWidth: `${chartWidth}px`,
          transform: `translateX(${scrollBarTwoPosX[0]}px)`,
        }}
        onPointerDown={onPointerDownHandler}
        onPointerMove={(e) => {
          if (!isDragging) return

          if (scrollBarTwoPosX[0] + e.movementX < 0) {
            setScrollBarTwoPosX([0, scrollBarTwoPosX[1] - scrollBarTwoPosX[0]])
            return
          }
          if (scrollBarTwoPosX[1] + e.movementX > chartWidth) {
            setScrollBarTwoPosX([scrollBarTwoPosX[0] + (chartWidth - scrollBarTwoPosX[1]), chartWidth])
            return
          }

          setScrollBarTwoPosX([scrollBarTwoPosX[0] + e.movementX, scrollBarTwoPosX[1] + e.movementX])
        }}
        onPointerUp={onPointerUpHandler}
        onLostPointerCapture={onPointerUpHandler}
      >
        {/* 스크롤바 왼쪽 조절 버튼 */}
        <div
          className="w-3 h-3 rounded-full border-[3px] border-gray-400 cursor-ew-resize absolute top-0 left-0"
          onPointerDown={onPointerDownHandler}
          onPointerMove={(e) => {
            e.stopPropagation()
            if (!isDragging) return

            setScrollBarTwoPosX([
              Math.min(Math.max(0, scrollBarTwoPosX[0] + e.movementX), scrollBarTwoPosX[1] - SCROLL_BAR_HEIGHT),
              scrollBarTwoPosX[1],
            ])
          }}
          onPointerUp={onPointerUpHandler}
          onLostPointerCapture={onPointerUpHandler}
        />

        {/* 스크롤바 오른쪽 조절 버튼 */}
        <div
          className="w-3 h-3 rounded-full border-[3px] border-gray-400 cursor-ew-resize  absolute top-0 right-0"
          onPointerDown={onPointerDownHandler}
          onPointerMove={(e) => {
            e.stopPropagation()
            if (!isDragging) return

            setScrollBarTwoPosX([
              scrollBarTwoPosX[0],
              Math.max(
                scrollBarTwoPosX[0] + SCROLL_BAR_HEIGHT,
                Math.min(chartWidth, scrollBarTwoPosX[1] + e.movementX),
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
