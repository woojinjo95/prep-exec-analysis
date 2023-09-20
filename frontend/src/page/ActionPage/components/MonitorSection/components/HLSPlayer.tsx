import React, { useEffect, useState } from 'react'
import Hls from 'hls.js'

export interface HlsPlayerProps extends React.VideoHTMLAttributes<HTMLVideoElement> {
  src: string
}

const pullCurrentPlayTime = (videoElement: HTMLVideoElement | null, diffTime = 0) => {
  if (videoElement && videoElement.currentTime) {
    // 불러온 영상의 마지막 시간 1초전으로 현재 재생시간을 맞춤
    // eslint-disable-next-line no-param-reassign
    videoElement.currentTime = videoElement.duration + diffTime
    videoElement.play().catch(() => {
      console.log('error')
    })
  }
}

const HLSPlayer: React.FC<HlsPlayerProps> = ({ src, autoPlay, ...props }) => {
  const playerRef = React.useRef<HTMLVideoElement | null>(null)
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

  useEffect(() => {
    let hls: Hls

    function initPlayer() {
      if (hls != null) {
        hls.destroy()
      }

      const newHls = new Hls({
        enableWorker: false,
        maxLiveSyncPlaybackRate: 1.5,
        backBufferLength: 0,
        xhrSetup: (xhr: XMLHttpRequest) => {
          xhr.setRequestHeader('Authorization', `Basic ${btoa('heliodor:ffdf00')}`)
        },
      })

      if (playerRef.current != null) {
        newHls.attachMedia(playerRef.current)
      }

      newHls.on(Hls.Events.MEDIA_ATTACHED, () => {
        newHls.loadSource(`${src}/index.m3u8`)

        newHls.on(Hls.Events.MANIFEST_PARSED, () => {
          if (autoPlay && playerRef.current) {
            playerRef.current.muted = true
            playerRef.current
              .play()
              .then(() => {
                setIsConnectHLS(true)
                pullCurrentPlayTime(playerRef.current)
              })
              .catch((err) => {
                setIsConnectHLS(false)
                console.error(err)
              })
          }
        })
      })

      newHls.on(Hls.Events.ERROR, (_, data) => {
        if (data.fatal && playerRef.current != null) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              // network err가 발생했을 경우 1초 후 hls 재설정
              newHls.destroy()
              setTimeout(initPlayer, 1000)
              break
            case Hls.ErrorTypes.MEDIA_ERROR:
              newHls.recoverMediaError()
              break
            default:
              // initPlayer 재 실행
              newHls.destroy()
              setTimeout(initPlayer, 2000)
              break
          }
        }
      })

      hls = newHls
    }

    // Check for Media Source support
    if (Hls.isSupported()) {
      initPlayer()
    }

    return () => {
      if (hls != null) {
        hls.stopLoad()
        hls.detachMedia()
        hls.destroy()
      }
    }
  }, [autoPlay, src])

  // If Media Source is supported, use HLS.js to play video
  if (Hls.isSupported()) return <video ref={playerRef} {...props} />

  // Fallback to using a regular video player if HLS is supported by default in the user's browser
  return <video ref={playerRef} playsInline autoPlay={autoPlay} muted src={src} {...props} />
}

export default HLSPlayer
