import React, { useState } from 'react'
import cx from 'classnames'

interface ResizingPoint {
  horizontal: 'left' | 'center' | 'right'
  vertical: 'top' | 'center' | 'bottom'
}

const ResizingPointList: readonly ResizingPoint[] = [
  { horizontal: 'left', vertical: 'top' },
  { horizontal: 'center', vertical: 'top' },
  { horizontal: 'right', vertical: 'top' },
  { horizontal: 'left', vertical: 'center' },
  { horizontal: 'right', vertical: 'center' },
  { horizontal: 'left', vertical: 'bottom' },
  { horizontal: 'center', vertical: 'bottom' },
  { horizontal: 'right', vertical: 'bottom' },
] as const

interface ResizingPointsProps {
  setCropTwoPosX: React.Dispatch<React.SetStateAction<[number, number]>>
  setCropTwoPosY: React.Dispatch<React.SetStateAction<[number, number]>>
}

/**
 * 크롭 영역 크기 조절하는 포인트들 컴포넌트
 *
 * 총 8개의 점
 * @example
 * // ㅁ-------ㅁ-------ㅁ
 * // |                |
 * // ㅁ               ㅁ
 * // |                |
 * // ㅁ-------ㅁ-------ㅁ
 */
const ResizingPoints: React.FC<ResizingPointsProps> = ({ setCropTwoPosX, setCropTwoPosY }) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)

  return (
    <>
      {ResizingPointList.map(({ horizontal, vertical }) => (
        <div
          key={`set-roi-resizing-point-${horizontal}-${vertical}`}
          className={cx('absolute -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-red-500', {
            'left-0': horizontal === 'left',
            'left-1/2': horizontal === 'center',
            'left-full': horizontal === 'right',
            'top-0': vertical === 'top',
            'top-1/2': vertical === 'center',
            'top-full': vertical === 'bottom',
            'cursor-grabbing': isDragging,
          })}
          draggable={false}
          onPointerDown={(e) => {
            e.stopPropagation()
            e.preventDefault()
            e.currentTarget.setPointerCapture(e.pointerId)
            setIsDragging(true)
          }}
          onPointerMove={(e) => {
            e.stopPropagation()
            e.preventDefault()
            if (!isDragging) return

            if (horizontal === 'left') {
              setCropTwoPosX((prev) => [prev[0] + e.movementX, prev[1]])
            }
            if (horizontal === 'right') {
              setCropTwoPosX((prev) => [prev[0], prev[1] + e.movementX])
            }
            if (vertical === 'top') {
              setCropTwoPosY((prev) => [prev[0] + e.movementY, prev[1]])
            }
            if (vertical === 'bottom') {
              setCropTwoPosY((prev) => [prev[0], prev[1] + e.movementY])
            }
          }}
          onPointerUp={(e) => {
            e.stopPropagation()
            e.preventDefault()
            e.currentTarget.releasePointerCapture(e.pointerId)
            setIsDragging(false)
            setCropTwoPosX((prev) => [Math.min(...prev), Math.max(...prev)])
            setCropTwoPosY((prev) => [Math.min(...prev), Math.max(...prev)])
          }}
        />
      ))}
    </>
  )
}

export default ResizingPoints
