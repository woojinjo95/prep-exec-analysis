import { KeyEvent } from '@page/ActionPage/types'
import React, { useEffect, useMemo, useState } from 'react'
import cx from 'classnames'
import ws from '@global/module/websocket'
import { remoconService } from '@global/service/RemoconService'
import { Remocon } from '../../api/entity'

interface RemoconButtonsProps {
  keyEvent: KeyEvent | null
  remoconRef: React.MutableRefObject<HTMLImageElement | null>
  remocon: Remocon | null
}

const RemoconButtons: React.FC<RemoconButtonsProps> = ({
  keyEvent,
  remoconRef,
  remocon,
}: RemoconButtonsProps): JSX.Element => {
  const [isSquareVisible, setIsSquareVisible] = useState<boolean>(false)
  const [windowSize, setWindowSize] = useState<{ width: number; height: number }>({
    width: window.innerWidth,
    height: window.innerHeight,
  })

  const dimension = useMemo(() => {
    if (!remoconRef.current) return null

    return {
      buttonWidth: remoconRef.current.getBoundingClientRect().width,
      buttonHeight: remoconRef.current.getBoundingClientRect().height,
      remoconImageWidth: remoconRef.current.naturalWidth,
      remoconImageHeight: remoconRef.current.naturalHeight,
    }
  }, [windowSize, remocon])

  useEffect(() => {
    if (keyEvent?.altKey) {
      setIsSquareVisible(true)
    }
    if (!keyEvent?.altKey) {
      setIsSquareVisible(false)
    }
  }, [keyEvent])

  useEffect(() => {
    const handleResize = () => {
      setWindowSize({ width: window.innerWidth, height: window.innerHeight })
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  if (!dimension || !remocon) return <div />
  return (
    <div>
      {remocon.remocon_codes.map((code) => {
        const leftTop = { left: code.coordinate[0], top: code.coordinate[1] }
        const rightBottom = { right: code.coordinate[2], bottom: code.coordinate[3] }

        return (
          <div
            key={`button_square_${leftTop.left}_${leftTop.top}`}
            className={cx('absolute cursor-pointer', {
              'border-orange-300 border-2': isSquareVisible,
            })}
            style={{
              top: leftTop.top * (dimension.buttonHeight / dimension.remoconImageHeight),
              left: leftTop.left * (dimension.buttonWidth / dimension.remoconImageWidth),
              height:
                rightBottom.bottom * (dimension.buttonHeight / dimension.remoconImageHeight) -
                leftTop.top * (dimension.buttonHeight / dimension.remoconImageHeight),
              width:
                rightBottom.right * (dimension.buttonWidth / dimension.remoconImageWidth) -
                leftTop.left * (dimension.buttonWidth / dimension.remoconImageWidth),
            }}
            onClick={() => {
              console.log(`{"remocon": {"key": "${code.code_name}"}}`)
              ws.send(`{"remocon": {"key": "${code.code_name}"}}`)
              remoconService.buttonClick(code.code_name)
            }}
          />
        )
      })}
    </div>
  )
}

export default RemoconButtons
