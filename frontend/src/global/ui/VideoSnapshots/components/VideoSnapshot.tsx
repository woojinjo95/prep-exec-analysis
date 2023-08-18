/* eslint-disable no-param-reassign */
import React, { useEffect, useState } from 'react'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'

const useCaptureVideoFrame = ({
  videoElement,
  currentTime = 0,
  format = 'jpeg',
  quality = 0.92,
}: {
  videoElement: HTMLVideoElement | null
  currentTime: number
  format?: 'png' | 'jpeg'
  quality?: number
}): {
  dataURI: string
} => {
  const [dataURI, setDataURI] = useState<string>('')

  useEffect(() => {
    if (!videoElement) return

    videoElement.currentTime = currentTime
    videoElement.muted = false
    videoElement.crossOrigin = 'Anonymous'

    // canvas에 특정 시점의 video를 이미지로 draw
    const canvas = document.createElement('canvas')
    canvas.width = (VIDEO_SNAPSHOT_HEIGHT * videoElement.videoWidth) / videoElement.videoHeight
    canvas.height = VIDEO_SNAPSHOT_HEIGHT
    canvas.getContext('2d')?.drawImage(videoElement, 0, 0, canvas.width, canvas.height)

    const newDataURI = canvas.toDataURL(`image/${format}`, quality)
    setDataURI(newDataURI)
  }, [videoElement])

  return { dataURI }
}

interface VideoSnapshotProps {
  currentTime: number
  translateX: number
  videoRef: React.MutableRefObject<HTMLVideoElement | null>
}

/**
 * 비디오 스냅샷 컴포넌트
 *
 * @param videoRef 원본 비디오 엘리먼트
 * @param currentTime 스냅샷으로 따고싶은 비디오 시간
 * @param translateX 스냅샷 표시 위치
 */
const VideoSnapshot: React.FC<VideoSnapshotProps> = ({ videoRef, currentTime, translateX }) => {
  const { dataURI } = useCaptureVideoFrame({ videoElement: videoRef.current, currentTime })

  if (!dataURI) return <div />
  return (
    <img
      src={dataURI}
      alt="snapshot"
      className="aspect-video absolute top-0"
      style={{
        transform: `translateX(${translateX}px)`,
      }}
    />
  )
}

export default VideoSnapshot
