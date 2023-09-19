import React, { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'
import { AppURL } from '@global/constant'
import { useVideoSnapshots } from './api/hook'
import { Skeleton } from '..'

interface VideoSnapshotsProps {
  startTime: Date | null
  endTime: Date | null
  tickCount?: number
  scaleX?: d3.ScaleTime<number, number, never> | null
  isVisible?: boolean
}

/**
 * 비디오 스냅샷 리스트 컴포넌트
 *
 * @param scaleX 스냅샷이 위치할 x좌표를 계산하는 scale
 */
const VideoSnapshots: React.FC<VideoSnapshotsProps> = ({
  startTime,
  endTime,
  tickCount = 10,
  scaleX,
  isVisible = true,
}) => {
  const [clientWidth, setClientWidth] = useState<number | null>(null)
  const { videoSnapshots, isLoading } = useVideoSnapshots()

  const snapshotScaleX: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (!videoSnapshots || !clientWidth || !startTime || !endTime) return null

    const indexedVideoSnapshots = videoSnapshots.map((d, snapshotIndex) => ({ snapshotIndex, ...d }))
    const scaledVideoSnapshots = indexedVideoSnapshots.filter(
      ({ timestamp }) =>
        new Date(timestamp).getTime() >= startTime.getTime() && new Date(timestamp).getTime() < endTime.getTime(),
    )

    if (scaledVideoSnapshots.length < 2) return null

    const startIndex = scaledVideoSnapshots[0].snapshotIndex
    const endIndex = scaledVideoSnapshots[scaledVideoSnapshots.length - 1].snapshotIndex

    return d3.scaleLinear().domain([startIndex, endIndex]).range([0, clientWidth])
  }, [videoSnapshots, clientWidth, startTime, endTime])

  // 스냅샷 리스트 앞부분이 비는 것을 방지하기 위한 index
  const firstSnapshotIndex = useMemo(() => {
    if (!snapshotScaleX) return null
    const ticks = snapshotScaleX.ticks(tickCount)

    if (!Number.isInteger(ticks[1] - ticks[0])) {
      return ticks[0] - (ticks[2] - ticks[0])
    }

    return ticks[0] - (ticks[1] - ticks[0])
  }, [snapshotScaleX, tickCount])

  const snapshots = useMemo(() => {
    if (!snapshotScaleX || !videoSnapshots) return []
    return [
      ...(firstSnapshotIndex !== null && !!videoSnapshots[firstSnapshotIndex] ? [firstSnapshotIndex] : []),
      ...snapshotScaleX.ticks(tickCount).filter((index) => Number.isInteger(index)),
    ]
  }, [snapshotScaleX, videoSnapshots, firstSnapshotIndex])

  if (!isVisible) return null
  if (isLoading) {
    return (
      <Skeleton
        className="w-full"
        style={{ height: VIDEO_SNAPSHOT_HEIGHT }}
        colorScheme={scaleX ? 'dark' : 'charcoal'}
      />
    )
  }
  return (
    <div
      ref={(ref) => {
        if (!ref || clientWidth !== null) return
        setClientWidth(ref.clientWidth)
      }}
      className="relative overflow-hidden"
      style={{ height: VIDEO_SNAPSHOT_HEIGHT }}
    >
      {videoSnapshots &&
        snapshotScaleX &&
        snapshots?.map((index) => (
          <img
            key={`snapshot-${index}`}
            src={`${AppURL.backendURL}/api/v1/file/download?path=${encodeURIComponent(videoSnapshots[index].path)}`}
            alt="snapshot"
            className="aspect-video absolute top-0 h-full"
            style={{
              transform: `translateX(${
                scaleX ? scaleX(new Date(videoSnapshots[index].timestamp)) : snapshotScaleX(index)
              }px)`,
            }}
          />
        ))}
    </div>
  )
}

export default VideoSnapshots
