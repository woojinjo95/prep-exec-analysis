import { useCallback, useEffect, useRef, useState } from 'react'

export const useCreateVideo = ({ src, currentTime }: { src: string; currentTime: number }) => {
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
    video.crossOrigin = 'Anonymous'
    video.addEventListener('loadeddata', onLoadedVideo(video))

    return () => {
      video.removeEventListener('loadeddata', onLoadedVideo(video))
    }
  }, [src, currentTime])

  return { isLoadedVideo, videoRef }
}
