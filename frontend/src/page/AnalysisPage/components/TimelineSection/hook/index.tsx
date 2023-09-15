import { useCallback, useEffect, useMemo, useState } from 'react'
import { useRecoilState } from 'recoil'
import * as d3 from 'd3'
import { cursorDateTimeState } from '@global/atom'
import { DefaultChartDataType } from '@global/types'
import { findNearIndex } from '../usecase'
import { SCROLL_BAR_HEIGHT } from '../constant'

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

/**
 * 차트 가로스크롤 / 확대 / 축소 휠 이벤트 hook
 */
export const useHandleChartWheel = <T extends HTMLElement>({
  ref,
  isReadyRenderChart,
  setScrollBarTwoPosX,
  chartWidth,
}: {
  ref: T | null
  isReadyRenderChart: boolean
  setScrollBarTwoPosX: React.Dispatch<React.SetStateAction<[number, number] | null>>
  chartWidth?: number
}): void => {
  const [isPressAlt, setIsPressAlt] = useState<boolean>(false)
  const [isPressCtrl, setIsPressCtrl] = useState<boolean>(false)

  const handleWheel = (e: WheelEvent) => {
    if (!chartWidth) return

    if (isPressAlt && isPressCtrl) {
      // preventDefault <- 차트의 기본 세로스크롤 이벤트를 막기 위함
      e.preventDefault()

      setScrollBarTwoPosX((prev) => {
        if (!prev) return prev
        if (e.deltaY >= 0 && prev[1] - prev[0] === SCROLL_BAR_HEIGHT) return prev

        const posX1 = Math.min(Math.max(prev[0] + e.deltaY, 0), prev[1] - SCROLL_BAR_HEIGHT)
        const posX2 = Math.min(Math.max(prev[1] - e.deltaY, prev[0] + SCROLL_BAR_HEIGHT), chartWidth)
        return [posX1, posX2]
      })
      return
    }

    if (!e.deltaX) return
    // preventDefault <- mac에서 브라우저 뒤로가기 기능을 비활성화하기 위함
    e.preventDefault()

    // 왼쪽 -> 오른쪽 스크롤 시
    if (e.deltaX < 0) {
      setScrollBarTwoPosX((prev) => {
        if (!prev) return prev

        const scrollbarWidth = prev[1] - prev[0]
        const posX1 = Math.max(prev[0] + e.deltaX, 0)
        return [posX1, posX1 + scrollbarWidth]
      })
    }
    // 오른쪽 -> 왼쪽 스크롤 시
    else {
      setScrollBarTwoPosX((prev) => {
        if (!prev) return prev

        const scrollbarWidth = prev[1] - prev[0]
        const posX2 = Math.min(prev[1] + e.deltaX, chartWidth)
        return [posX2 - scrollbarWidth, posX2]
      })
    }
  }

  useEffect(() => {
    const keyDownHandler = (e: KeyboardEvent) => {
      if (e.repeat) return

      if (e.altKey) {
        e.preventDefault()
        setIsPressAlt(true)
      }
      if (e.ctrlKey) {
        e.preventDefault()
        setIsPressCtrl(true)
      }
    }

    const keyUpHandler = (e: KeyboardEvent) => {
      if (!e.altKey) {
        e.preventDefault()
        setIsPressAlt(false)
      }
      if (!e.ctrlKey) {
        e.preventDefault()
        setIsPressCtrl(false)
      }
    }

    window.addEventListener('keydown', keyDownHandler)
    window.addEventListener('keyup', keyUpHandler)
    return () => {
      window.removeEventListener('keydown', keyDownHandler)
      window.removeEventListener('keyup', keyUpHandler)
    }
  }, [])

  useEffect(() => {
    if (!ref) return undefined
    // passive: false <- handler에서 preventDefault를 사용하기 위함
    ref.addEventListener('wheel', handleWheel, { passive: false })

    return () => {
      ref?.removeEventListener('wheel', handleWheel)
    }
  }, [isReadyRenderChart, handleWheel])
}
