import React, { useEffect, useMemo, useState } from 'react'
import * as d3 from 'd3'
import { ReactComponent as CursorIcon } from '@assets/images/pentagon.svg'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'

interface VideoSnapshotsCursorProps {
  startDuration: number
  endDuration: number
  defaultCurrentTime?: number
  changeVideoTimeCallback: (sec: number) => void
}

/**
 * 비디오 스냅샷 위에서 시간을 조정하는 커서
 */
const VideoSnapshotsCursor: React.FC<VideoSnapshotsCursorProps> = ({
  startDuration,
  endDuration,
  defaultCurrentTime,
  changeVideoTimeCallback,
}) => {
  const [dimension, setDimension] = useState<{ left: number; width: number } | null>(null)
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const [posX, setPosX] = useState<number | null>(null)

  const scaleX: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (startDuration === null || endDuration === null || !dimension) return null
    return d3.scaleLinear().domain([startDuration, endDuration]).range([0, dimension.width])
  }, [startDuration, endDuration, dimension])

  useEffect(() => {
    if (!scaleX || posX !== null) return

    if (!defaultCurrentTime) {
      setPosX(0)
      return
    }

    setPosX(scaleX(defaultCurrentTime))
  }, [scaleX, posX, defaultCurrentTime])

  const updateVideoTime: React.PointerEventHandler<HTMLDivElement> = (e) => {
    if (!dimension || !scaleX) return

    const newPosX = Math.min(dimension.width, Math.max(0, e.clientX - dimension.left))
    changeVideoTimeCallback(scaleX.invert(newPosX))
    setPosX(newPosX)
  }

  return (
    <div
      className="absolute top-0 left-0 w-full cursor-pointer"
      style={{
        height: VIDEO_SNAPSHOT_HEIGHT,
      }}
      ref={(ref) => {
        if (!ref || dimension !== null) return
        const { left, width } = ref.getBoundingClientRect()
        setDimension({ left, width })
      }}
      onPointerDown={(e) => {
        e.stopPropagation()
        e.currentTarget.setPointerCapture(e.pointerId)
        updateVideoTime(e)
        setIsDragging(true)
      }}
      onPointerMove={(e) => {
        e.stopPropagation()
        e.preventDefault()
        if (!isDragging) return
        updateVideoTime(e)
      }}
      onPointerUp={(e) => {
        e.currentTarget.releasePointerCapture(e.pointerId)
        if (!isDragging) return
        updateVideoTime(e)
        setIsDragging(false)
      }}
      onPointerLeave={(e) => {
        e.currentTarget.releasePointerCapture(e.pointerId)
        if (!isDragging) return
        updateVideoTime(e)
        setIsDragging(false)
      }}
    >
      {/* background */}
      <div className="w-full h-full absolute top-0 left-0 bg-black opacity-30" />

      {/* cursor */}
      {!!scaleX && posX !== null && (
        <>
          <CursorIcon
            className="absolute w-3 h-3 fill-primary -top-3 -left-1.5"
            style={{
              transform: `translateX(${posX}px)`,
            }}
          />
          <div
            className="absolute top-0 -left-[0.5px] h-full w-px bg-primary"
            style={{
              transform: `translateX(${posX}px)`,
            }}
          />
        </>
      )}
    </div>
  )
}

export default VideoSnapshotsCursor
