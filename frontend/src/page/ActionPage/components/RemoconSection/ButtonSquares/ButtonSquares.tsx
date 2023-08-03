import { KeyEvent } from '@page/ActionPage/types'
import React, { forwardRef, useEffect, useState } from 'react'
import cx from 'classnames'
import ws from '@global/module/websocket'
import { Remocon } from '../api/entity'

interface ButtonSquaresProps {
  keyEvent: KeyEvent | null
  imageRef: React.RefObject<HTMLImageElement>
  selectedRemocon: Remocon | null
}

const ButtonSquares = forwardRef(({ keyEvent, imageRef, selectedRemocon }: ButtonSquaresProps): JSX.Element => {
  const [isSquareVisible, setIsSquareVisible] = useState<boolean>(false)

  useEffect(() => {
    if (keyEvent?.altKey) {
      setIsSquareVisible(true)
    }
    if (!keyEvent?.altKey) {
      setIsSquareVisible(false)
    }
  }, [keyEvent])

  return (
    <div>
      {imageRef.current &&
        selectedRemocon?.remocon_codes.map((code) => {
          const leftTop = { left: code.coordinate[0], top: code.coordinate[1] }
          const rightBottom = { right: code.coordinate[2], bottom: code.coordinate[3] }
          return (
            <div
              key={`button_square_${leftTop.left}_${leftTop.top}`}
              className={cx('absolute cursor-pointer', {
                'border-orange-300 border-2': isSquareVisible,
              })}
              style={{
                top:
                  imageRef.current!.getBoundingClientRect().top +
                  leftTop.top *
                    (imageRef.current!.getBoundingClientRect().height / selectedRemocon.image_resolution[1]),
                left:
                  imageRef.current!.getBoundingClientRect().left +
                  leftTop.left *
                    (imageRef.current!.getBoundingClientRect().width / selectedRemocon.image_resolution[0]),
                height:
                  rightBottom.bottom *
                    (imageRef.current!.getBoundingClientRect().height / selectedRemocon.image_resolution[1]) -
                  leftTop.top *
                    (imageRef.current!.getBoundingClientRect().height / selectedRemocon.image_resolution[1]),
                width:
                  rightBottom.right *
                    (imageRef.current!.getBoundingClientRect().width / selectedRemocon.image_resolution[0]) -
                  leftTop.left *
                    (imageRef.current!.getBoundingClientRect().width / selectedRemocon.image_resolution[0]),
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
})

ButtonSquares.displayName = 'ButtonSquares'
export default ButtonSquares
