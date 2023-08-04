import { KeyEvent } from '@page/ActionPage/types'
import React, { useEffect, useMemo, useState } from 'react'
import cx from 'classnames'
import ws from '@global/module/websocket'
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
  const dimension = useMemo(() => {
    if (!remoconRef.current) return null
    return {
      buttonTop: remoconRef.current.getBoundingClientRect().top,
      buttonLeft: remoconRef.current.getBoundingClientRect().left,
      buttonWidth: remoconRef.current.getBoundingClientRect().width,
      buttonHeight: remoconRef.current.getBoundingClientRect().height,
      remoconImageWidth: remoconRef.current.naturalWidth,
      remoconImageHeight: remoconRef.current.naturalHeight,
    }
  }, [])

  useEffect(() => {
    if (keyEvent?.altKey) {
      setIsSquareVisible(true)
    }
    if (!keyEvent?.altKey) {
      setIsSquareVisible(false)
    }
  }, [keyEvent])

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
              top: dimension.buttonTop + leftTop.top * (dimension.buttonHeight / dimension.remoconImageHeight),
              left: dimension.buttonLeft + leftTop.left * (dimension.buttonWidth / dimension.remoconImageWidth),
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
            }}
          />
        )
      })}
    </div>
  )
}

export default RemoconButtons
