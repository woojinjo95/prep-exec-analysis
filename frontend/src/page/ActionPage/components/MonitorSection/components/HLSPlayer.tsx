import React, { useEffect } from 'react'
import Hls from 'hls.js'

export interface HlsPlayerProps extends React.VideoHTMLAttributes<HTMLVideoElement> {
  src: string
}

const HLSPlayer: React.FC<HlsPlayerProps> = ({ src, autoPlay, ...props }) => {
  const playerRef = React.useRef<HTMLVideoElement | null>(null)

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
            playerRef.current.play().catch((err) => console.log(err))
          }
        })
      })

      newHls.on(Hls.Events.ERROR, (_, data) => {
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              newHls.startLoad()
              break
            case Hls.ErrorTypes.MEDIA_ERROR:
              newHls.recoverMediaError()
              break
            default:
              initPlayer()
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
  return <video ref={playerRef} playsInline autoPlay={autoPlay} muted {...props} />
}

export default HLSPlayer
