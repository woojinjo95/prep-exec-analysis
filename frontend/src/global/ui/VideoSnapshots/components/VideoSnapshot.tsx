import React, { useEffect, useState } from 'react'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'
import { useCreateVideo } from '@global/ui/VideoSnapshots/hook'

const useCaptureVideoFrame = ({
  src,
  currentTime = 0,
  format = 'jpeg',
  quality = 0.92,
}: {
  src: string
  currentTime: number
  format?: 'png' | 'jpeg'
  quality?: number
}): {
  dataURI: string
} => {
  const { isLoadedVideo, videoRef } = useCreateVideo({ src, currentTime })
  const [dataURI, setDataURI] = useState<string>('')

  useEffect(() => {
    if (!isLoadedVideo || !videoRef.current) return

    // canvas에 특정 시점의 video를 이미지로 draw
    const canvas = document.createElement('canvas')
    canvas.width = (VIDEO_SNAPSHOT_HEIGHT * videoRef.current.videoWidth) / videoRef.current.videoHeight
    canvas.height = VIDEO_SNAPSHOT_HEIGHT
    canvas.getContext('2d')?.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height)

    const newDataURI = canvas.toDataURL(`image/${format}`, quality)
    setDataURI(newDataURI)
  }, [isLoadedVideo])

  return { dataURI }
}

interface VideoSnapshotProps {
  src: string
  currentTime: number
  translateX: number
}

/**
 * 비디오 스냅샷 컴포넌트
 *
 * @param src 비디오 주소
 * @param currentTime 스냅샷으로 따고싶은 비디오 시간
 * @param translateX 스냅샷 표시 위치
 */
const VideoSnapshot: React.FC<VideoSnapshotProps> = ({ src, currentTime, translateX }) => {
  const { dataURI } = useCaptureVideoFrame({ src, currentTime })

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
