import { useCallback, useMemo, useState } from 'react'
import { useRecoilState, useSetRecoilState } from 'recoil'
import { cursorDateTimeState, tooltipDateTimeState } from '@global/atom'

/**
 * 커서 드래그, 호버 툴팁 관련 hook
 */
export const useCursorEvent = ({
  scaleX,
  offsetLeft,
  width,
}: {
  scaleX: d3.ScaleTime<number, number, never> | null
  offsetLeft: number | null
  width: number | null
}) => {
  const [isCursorDragging, setIsCursorDragging] = useState<boolean>(false)
  const [cursorPosX, setCursorPosX] = useState<number>(0)
  const [cursorDateTime, setCursorDateTime] = useRecoilState(cursorDateTimeState)
  const [tooltipPosX, setTooltipPosX] = useState<number | null>(null)
  const setTooltipDateTime = useSetRecoilState(tooltipDateTimeState)

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
      setTooltipPosX(null)
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

  const onTooltipMouseMove: React.MouseEventHandler<HTMLDivElement> = useCallback(
    (e) => {
      e.preventDefault()
      if (isCursorDragging || !offsetLeft || !width || !scaleX) return
      const newPosX = Math.min(width, Math.max(0, e.clientX - offsetLeft))
      setTooltipPosX(newPosX)
      setTooltipDateTime(scaleX.invert(newPosX))
    },
    [isCursorDragging, offsetLeft, width, scaleX],
  )

  const onTooltipMouseLeave: React.MouseEventHandler<HTMLDivElement> = useCallback(() => {
    setTooltipDateTime(null)
    setTooltipPosX(null)
  }, [])

  return {
    onCursorPointerDown,
    onCursorPointerMove,
    onCursorPointerUp,
    onTooltipMouseMove,
    onTooltipMouseLeave,
    cursorTranslateX,
    tooltipPosX,
  }
}
