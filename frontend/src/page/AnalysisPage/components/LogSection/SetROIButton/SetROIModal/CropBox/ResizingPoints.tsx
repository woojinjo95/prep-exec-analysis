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
  setCropPosX: React.Dispatch<React.SetStateAction<number>>
  setCropPosY: React.Dispatch<React.SetStateAction<number>>
  setCropWidth: React.Dispatch<React.SetStateAction<number | null>>
  setCropHeight: React.Dispatch<React.SetStateAction<number | null>>
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
const ResizingPoints: React.FC<ResizingPointsProps> = ({ setCropPosX, setCropPosY, setCropWidth, setCropHeight }) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)

  return (
    <>
      {ResizingPointList.map(({ horizontal, vertical }) => (
        <div
          key={`set-roi-resizing-point-${horizontal}-${vertical}`}
          className={cx('absolute -translate-x-1/2 -translate-y-1/2 w-2 h-2 bg-red-500 ', {
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
            e.currentTarget.setPointerCapture(e.pointerId)
            setIsDragging(true)
          }}
          onPointerMove={(e) => {
            e.stopPropagation()
            if (!isDragging) return

            if (horizontal === 'left') {
              setCropPosX((prev) => prev + e.movementX)
              setCropWidth((prev) => (prev === null ? prev : prev - e.movementX))
            }
            if (horizontal === 'right') {
              setCropWidth((prev) => (prev === null ? prev : prev + e.movementX))
            }
            if (vertical === 'top') {
              setCropPosY((prev) => prev + e.movementY)
              setCropHeight((prev) => (prev === null ? prev : prev - e.movementY))
            }
            if (vertical === 'bottom') {
              setCropHeight((prev) => (prev === null ? prev : prev + e.movementY))
            }
          }}
          onPointerUp={(e) => {
            e.stopPropagation()
            e.currentTarget.releasePointerCapture(e.pointerId)
            setIsDragging(false)
          }}
        />
      ))}
    </>
  )
}

export default React.memo(ResizingPoints)
