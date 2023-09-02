import { useCallback, useMemo, useState } from 'react'
import { useRecoilState } from 'recoil'
import { cursorDateTimeState } from '@global/atom'

/**
 * 커서 드래그 관련 hook
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
  }
}
