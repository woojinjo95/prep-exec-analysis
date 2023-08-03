import React, { useCallback, useEffect, useRef, useState } from 'react'
import Hls from 'hls.js'

const pullCurrentPlayTime = (videoElement: HTMLVideoElement | null, diffTime = 0) => {
  if (videoElement && videoElement.currentTime) {
    // 불러온 영상의 마지막 시간 1초전으로 현재 재생시간을 맞춤
    // eslint-disable-next-line no-param-reassign
    videoElement.currentTime = videoElement.duration + diffTime
    videoElement.play().catch((err) => {
      console.log('error', err)
    })
  }
}

interface HLSPlayerProps {
  src: string
}

const HLSPlayer: React.FC<HLSPlayerProps> = ({ src }) => {
  const playerRef = useRef<HTMLVideoElement | null>(null)
  const [isConnectHLS, setIsConnectHLS] = useState<boolean>(false)

  useEffect(() => {
    window.addEventListener('focus', () => {
      pullCurrentPlayTime(playerRef.current)
    })
  }, [])

  useEffect(() => {
    const timerId = setInterval(() => {
      if (isConnectHLS) {
        pullCurrentPlayTime(playerRef.current, -1)
      }
    }, 1000 * 60)

    return () => {
      clearInterval(timerId)
    }
  }, [isConnectHLS])

  let hlsInstance: Hls | null = null

  const create = useCallback(() => {
    const video = playerRef.current

    if (video) {
      // always prefer hls.js over native HLS.
      // this is because some Android versions support native HLS
      // but doesn't support fMP4s.
      if (Hls.isSupported()) {
        console.log('isSupported')
        const hls = new Hls({
          maxLiveSyncPlaybackRate: 1.5,
        })
        hlsInstance = hls

        hls.on(Hls.Events.ERROR, (_, data) => {
          if (data.fatal) {
            hls.destroy()
            setTimeout(create, 2000)
          }
        })
        hls.config.xhrSetup = (xhr: XMLHttpRequest) => {
          xhr.setRequestHeader('Authorization', `Basic ${btoa('heliodor:ffdf00')}`)
        }
        hls.config.backBufferLength = 0 // before(default) Infinity -> after 0(최소한의 재생가능한 세그먼트를 유지)

        hls.loadSource(`${src}/index.m3u8`)
        hls.attachMedia(video)

        const playPromise = video.play()
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              setIsConnectHLS(true)
              pullCurrentPlayTime(video)
            })
            .catch((err) => {
              setIsConnectHLS(false)
              console.log('error', err)
            })
        }
      } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        // since it's not possible to detect timeout errors in iOS,
        // wait for the playlist to be available before starting the stream
        fetch('stream.m3u8')
          .then(() => {
            video.src = 'index.m3u8'
            video.play().catch((err) => {
              console.log('error', err)
            })
          })
          .catch((err) => {
            console.log('error', err)
          })
      }
    }
  }, [src])

  useEffect(() => {
    create()

    return () => {
      if (hlsInstance) {
        console.log('destory')
        hlsInstance.stopLoad()
        hlsInstance.destroy()
      }
    }
  }, [])

  return (
    <video ref={playerRef} className="h-full aspect-video bg-black" muted controls autoPlay playsInline src={src} />
  )
}

export default HLSPlayer
