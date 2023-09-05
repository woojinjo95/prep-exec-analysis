import React, { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { ReactComponent as CursorIcon } from '@assets/images/pentagon.svg'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'

interface VideoSnapshotsCursorProps {
  startDuration: number
  endDuration: number
  changeVideoTimeCallback: (sec: number) => void
}

/**
 * 비디오 스냅샷 위에서 시간을 조정하는 커서
 */
const VideoSnapshotsCursor: React.FC<VideoSnapshotsCursorProps> = ({
  startDuration,
  endDuration,
  changeVideoTimeCallback,
}) => {
  const [dimension, setDimension] = useState<{ left: number; width: number } | null>(null)
  const [isDragging, setIsDragging] = useState<boolean>(false)
  const [posX, setPosX] = useState<number>(0)

  const scaleX: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (startDuration === null || endDuration === null || !dimension) return null
    return d3.scaleLinear().domain([startDuration, endDuration]).range([0, dimension.width])
  }, [startDuration, endDuration, dimension])

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
        if (!dimension || !scaleX) return
        e.currentTarget.setPointerCapture(e.pointerId)
        setIsDragging(true)

        const newPosX = Math.min(dimension.width, Math.max(0, e.clientX - dimension.left))
        changeVideoTimeCallback(scaleX.invert(newPosX))
        setPosX(newPosX)
      }}
      onPointerMove={(e) => {
        e.stopPropagation()
        e.preventDefault()
        if (!isDragging || !dimension || !scaleX) return
        const newPosX = Math.min(dimension.width, Math.max(0, e.clientX - dimension.left))
        changeVideoTimeCallback(scaleX.invert(newPosX))
        setPosX(newPosX)
      }}
      onPointerUp={(e) => {
        e.currentTarget.releasePointerCapture(e.pointerId)
        setIsDragging(false)
      }}
      onPointerLeave={(e) => {
        e.currentTarget.releasePointerCapture(e.pointerId)
        setIsDragging(false)
      }}
    >
      {/* background */}
      <div className="w-full h-full absolute top-0 left-0 bg-black opacity-30" />

      {/* cursor */}
      {!!scaleX && (
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
