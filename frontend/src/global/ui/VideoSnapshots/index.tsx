import React, { useMemo, useState } from 'react'
import * as d3 from 'd3'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'
import { AppURL } from '@global/constant'
import { useVideoSnapshots } from './api/hook'

interface VideoSnapshotsProps {
  startTime: Date | null
  endTime: Date | null
  tickCount?: number
  scaleX?: d3.ScaleTime<number, number, never> | null
}

/**
 * 비디오 스냅샷 리스트 컴포넌트
 *
 * @param scaleX 스냅샷이 위치할 x좌표를 계산하는 scale
 */
const VideoSnapshots: React.FC<VideoSnapshotsProps> = ({ startTime, endTime, tickCount = 10, scaleX }) => {
  const [clientWidth, setClientWidth] = useState<number | null>(null)
  const { videoSnapshots } = useVideoSnapshots()

  const snapshotScaleX: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (!videoSnapshots || !clientWidth || !startTime || !endTime) return null

    const indexedVideoSnapshots = videoSnapshots.map((d, index) => ({ index, ...d }))
    const scaledVideoSnapshots = indexedVideoSnapshots.filter(
      ({ timestamp }) =>
        new Date(timestamp).getTime() >= startTime.getTime() && new Date(timestamp).getTime() < endTime.getTime(),
    )

    if (scaledVideoSnapshots.length < 2) return null

    // 스냅샷 리스트 앞부분이 비는 것을 방지
    const startIndex = Math.max(scaledVideoSnapshots[0].index - 1, 0)
    const endIndex = scaledVideoSnapshots[scaledVideoSnapshots.length - 1].index

    return d3.scaleLinear().domain([startIndex, endIndex]).range([0, clientWidth])
  }, [videoSnapshots, clientWidth, startTime, endTime])

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
        snapshotScaleX
          ?.ticks(tickCount)
          .filter((index) => Number.isInteger(index))
          .map((index) => (
            <img
              key={`snapshot-${index}`}
              src={`${AppURL.backendURL}/api/v1/file/download?path=${encodeURIComponent(videoSnapshots[index].path)}`}
              alt="snapshot"
              className="aspect-video absolute top-0 h-full"
              style={{
                transform: scaleX
                  ? `translateX(${scaleX(new Date(videoSnapshots[index].timestamp))}px)`
                  : `translateX(${snapshotScaleX(index)}px)`,
              }}
            />
          ))}
    </div>
  )
}

export default VideoSnapshots
