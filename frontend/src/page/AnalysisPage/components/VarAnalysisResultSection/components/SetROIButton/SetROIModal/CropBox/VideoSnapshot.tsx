import React, { useCallback, useEffect, useRef, useState } from 'react'

const useCreateVideo = ({ src, currentTime }: { src: string; currentTime: number }) => {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [isLoadedVideo, setIsLoadedVideo] = useState<boolean>(false)

  const onLoadedVideo = useCallback(
    (video: HTMLVideoElement) => () => {
      videoRef.current = video
      setIsLoadedVideo(true)
    },
    [],
  )

  useEffect(() => {
    const video = document.createElement('video')
    video.src = src
    video.currentTime = currentTime
    video.muted = false
    video.addEventListener('loadeddata', onLoadedVideo(video))

    return () => {
      video.removeEventListener('loadeddata', onLoadedVideo(video))
    }
  }, [src])

  return { isLoadedVideo, videoRef }
}

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
  format: string
} => {
  const { isLoadedVideo, videoRef } = useCreateVideo({ src, currentTime })
  const [dataURI, setDataURI] = useState<string>('')

  useEffect(() => {
    if (!isLoadedVideo || !videoRef.current) return

    // canvas에 특정 시점의 video를 이미지로 draw
    const canvas = document.createElement('canvas')
    canvas.width = (100 * videoRef.current.videoWidth) / videoRef.current.videoHeight
    canvas.height = 100
    canvas.getContext('2d')?.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height)

    const newDataURI = canvas.toDataURL(`image/${format}`, quality)
    setDataURI(newDataURI)
  }, [isLoadedVideo])

  return { dataURI, format }
}

interface VideoSnapshotProps {
  src: string
  translateX: number
}

const VideoSnapshot: React.FC<VideoSnapshotProps> = ({ src, translateX }) => {
  const { dataURI } = useCaptureVideoFrame({ src, currentTime: 10 })

  if (!dataURI) return <div />
  return (
    <img
      src={dataURI}
      alt="snapshot"
      className="h-[100px] aspect-video absolute top-0"
      style={{
        transform: `translateX(${translateX}px)`,
      }}
    />
  )
}

export default VideoSnapshot
