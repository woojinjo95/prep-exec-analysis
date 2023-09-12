import { useCallback, useMemo, useState } from 'react'
import { useRecoilState } from 'recoil'
import * as d3 from 'd3'
import { cursorDateTimeState } from '@global/atom'
import { DefaultChartDataType } from '@global/types'
import { findNearIndex } from '../usecase'

/**
 * 커서 드래그 관련 hook
 */
export const useCursorEvent = ({
  scaleX,
  offsetLeft,
  width,
}: {
  scaleX: d3.ScaleTime<number, number, never> | null
  offsetLeft?: number
  width?: number
}) => {
  const [isCursorDragging, setIsCursorDragging] = useState<boolean>(false)
  const [cursorPosX, setCursorPosX] = useState<number>(0)
  const [cursorDateTime, setCursorDateTime] = useRecoilState(cursorDateTimeState)

  const cursorTranslateX = useMemo(() => {
    if (!scaleX || !cursorDateTime) return 0
    return isCursorDragging ? cursorPosX : scaleX(cursorDateTime)
  }, [isCursorDragging, scaleX, cursorPosX, cursorDateTime])

  const onCursorPointerDown: React.PointerEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      if (!width || !offsetLeft) return
      e.preventDefault()
      e.currentTarget.setPointerCapture(e.pointerId)
      setIsCursorDragging(true)
      setCursorPosX(Math.min(width, Math.max(0, e.clientX - offsetLeft)))
    },
    [width, offsetLeft],
  )

  const onCursorPointerMove: React.PointerEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      e.preventDefault()
      if (!isCursorDragging || !offsetLeft || !width) return
      setCursorPosX(Math.min(width, Math.max(0, e.clientX - offsetLeft)))
    },
    [isCursorDragging, offsetLeft, width],
  )

  const onCursorPointerUp: React.PointerEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      e.currentTarget.releasePointerCapture(e.pointerId)
      setIsCursorDragging(false)
      if (!scaleX) return
      setCursorDateTime(scaleX.invert(cursorPosX))
    },
    [scaleX, cursorPosX],
  )

  return {
    onCursorPointerDown,
    onCursorPointerMove,
    onCursorPointerUp,
    cursorTranslateX,
    isCursorDragging,
  }
}

/**
 * 툴팁 표현 관련 hook
 *
 * @return 툴팁 event handler, 툴팁에 표현할 데이터, 툴팁을 표시할 x좌표
 */
export const useTooltipEvent = <T extends DefaultChartDataType>({
  scaleX,
  offsetLeft,
  width,
}: {
  scaleX: d3.ScaleTime<number, number, never> | null
  offsetLeft?: number | null
  width?: number | null
}) => {
  const [posX, setPosX] = useState<number | null>(null)
  const [tooltipData, setTooltipData] = useState<T | null>(null)

  const onMouseMove = useCallback(
    (data: T[]): React.MouseEventHandler<HTMLDivElement> =>
      (e) => {
        if (!data || !scaleX || !width || !offsetLeft) return

        const posX = Math.min(width, Math.max(0, e.clientX - offsetLeft))
        setPosX(posX)
        const nearIndex = findNearIndex(data, scaleX.invert(posX).getTime())
        if (nearIndex === -1) return
        const findedData = data[nearIndex]

        // 가장 가까운 데이터가 마우스 기준 4px 이상 떨어져 있다면 -> 데이터를 표시하지 않음
        if (findedData.duration === undefined && Math.abs(scaleX(new Date(findedData.datetime)) - posX) > 4) {
          setTooltipData(null)
          return
        }

        // 지속시간이 있는(duration) 데이터이고 마우스가 지속시간 양옆으로 4px 이상 떨어져 있다면 -> 데이터를 표시하지 않음
        if (
          findedData.duration !== undefined &&
          (posX + 4 < scaleX(new Date(findedData.datetime)) ||
            scaleX(new Date(findedData.datetime + findedData.duration)) + 4 < posX)
        ) {
          setTooltipData(null)
          return
        }

        setTooltipData(findedData)
      },
    [scaleX, width, offsetLeft],
  )

  const onMouseLeave: React.MouseEventHandler<HTMLDivElement> = useCallback(() => {
    setPosX(null)
    setTooltipData(null)
  }, [])

  return {
    posX,
    tooltipData,
    onMouseMove,
    onMouseLeave,
  }
}
