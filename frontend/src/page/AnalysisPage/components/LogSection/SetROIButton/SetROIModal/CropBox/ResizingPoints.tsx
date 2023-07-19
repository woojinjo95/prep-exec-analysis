import React, { useState } from 'react'
import cx from 'classnames'

interface ResizingPoint {
  horizontal: 'left' | 'center' | 'right'
  vertical: 'top' | 'center' | 'bottom'
  cursor: 'cursor-ew-resize' | 'cursor-ns-resize' | 'cursor-nesw-resize' | 'cursor-nwse-resize'
}

const ResizingPointList: readonly ResizingPoint[] = [
  { horizontal: 'left', vertical: 'top', cursor: 'cursor-nwse-resize' },
  { horizontal: 'center', vertical: 'top', cursor: 'cursor-ns-resize' },
  { horizontal: 'right', vertical: 'top', cursor: 'cursor-nesw-resize' },
  { horizontal: 'left', vertical: 'center', cursor: 'cursor-ew-resize' },
  { horizontal: 'right', vertical: 'center', cursor: 'cursor-ew-resize' },
  { horizontal: 'left', vertical: 'bottom', cursor: 'cursor-nesw-resize' },
  { horizontal: 'center', vertical: 'bottom', cursor: 'cursor-ns-resize' },
  { horizontal: 'right', vertical: 'bottom', cursor: 'cursor-nwse-resize' },
] as const

/**
 * 입력받는 x축 또는 y축의 두 좌표가 특정 영역 밖으로 벗어나지 않는 값을 계산하는 함수
 */
const demarcateTwoPosition = (
  twoPosition: [number, number],
  minWidthOrHeight: number,
  maxWidthOrHeight: number,
): [number, number] => {
  const minPosIndex = twoPosition[0] < twoPosition[1] ? 0 : 1
  const maxPosIndex = twoPosition[0] < twoPosition[1] ? 1 : 0

  if (twoPosition[minPosIndex] < minWidthOrHeight) {
    return twoPosition.map((x, index) => (index === minPosIndex ? minWidthOrHeight : x)) as [number, number]
  }
  if (twoPosition[maxPosIndex] > maxWidthOrHeight) {
    return twoPosition.map((x, index) => (index === maxPosIndex ? maxWidthOrHeight : x)) as [number, number]
  }

  return twoPosition as [number, number]
}

interface ResizingPointsProps {
  clientWidth: number
  clientHeight: number
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
const ResizingPoints: React.FC<ResizingPointsProps> = ({
  clientWidth,
  clientHeight,
  setCropTwoPosX,
  setCropTwoPosY,
}) => {
  const [isDragging, setIsDragging] = useState<boolean>(false)

  return (
    <>
      {ResizingPointList.map(({ horizontal, vertical, cursor }) => (
        <div
          key={`set-roi-resizing-point-${horizontal}-${vertical}`}
          // TODO: 모서리 커서 스타일 - 마우스 위치에 따라 동적으로 변경
          className={cx('absolute -translate-x-1/2 -translate-y-1/2 w-[7px] h-[7px] bg-red-500', cursor, {
            'left-0': horizontal === 'left',
            'left-1/2': horizontal === 'center',
            'left-full': horizontal === 'right',
            'top-0': vertical === 'top',
            'top-1/2': vertical === 'center',
            'top-full': vertical === 'bottom',
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
              setCropTwoPosX((prev) => demarcateTwoPosition([prev[0] + e.movementX, prev[1]], 0, clientWidth))
            }
            if (horizontal === 'right') {
              setCropTwoPosX((prev) => demarcateTwoPosition([prev[0], prev[1] + e.movementX], 0, clientWidth))
            }
            if (vertical === 'top') {
              setCropTwoPosY((prev) => demarcateTwoPosition([prev[0] + e.movementY, prev[1]], 0, clientHeight))
            }
            if (vertical === 'bottom') {
              setCropTwoPosY((prev) => demarcateTwoPosition([prev[0], prev[1] + e.movementY], 0, clientHeight))
            }
          }}
          onPointerUp={(e) => {
            e.currentTarget.releasePointerCapture(e.pointerId)
            setIsDragging(false)
            setCropTwoPosX((prev) => prev.sort())
            setCropTwoPosY((prev) => prev.sort())
          }}
          onLostPointerCapture={(e) => {
            e.currentTarget.releasePointerCapture(e.pointerId)
            setIsDragging(false)
            setCropTwoPosX((prev) => prev.sort())
            setCropTwoPosY((prev) => prev.sort())
          }}
        />
      ))}
    </>
  )
}

export default ResizingPoints
