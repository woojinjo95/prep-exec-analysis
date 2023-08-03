import { KeyEvent } from '@page/ActionPage/types'
import React, { forwardRef, useEffect, useState } from 'react'
import cx from 'classnames'

interface ButtonSquaresProps {
  keyEvent: KeyEvent | null
  keyboardCoors?: { leftTop: { left: number; top: number }; rightBottom: { right: number; bottom: number } }[]
  imageRef: React.RefObject<HTMLImageElement>
  remoconResolution: [number, number]
}

const ButtonSquares = forwardRef(
  ({ keyEvent, keyboardCoors, imageRef, remoconResolution }: ButtonSquaresProps): JSX.Element => {
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
          keyboardCoors &&
          keyboardCoors.map((coor) => {
            return (
              <div
                key={`button_square_${coor.leftTop.left}_${coor.leftTop.top}`}
                className={cx('absolute cursor-pointer', {
                  'border-orange-300 border-2': isSquareVisible,
                })}
                style={{
                  top:
                    imageRef.current!.getBoundingClientRect().top +
                    coor.leftTop.top * (imageRef.current!.getBoundingClientRect().height / remoconResolution[1]),
                  left:
                    imageRef.current!.getBoundingClientRect().left +
                    coor.leftTop.left * (imageRef.current!.getBoundingClientRect().width / remoconResolution[0]),
                  height:
                    coor.rightBottom.bottom *
                      (imageRef.current!.getBoundingClientRect().height / remoconResolution[1]) -
                    coor.leftTop.top * (imageRef.current!.getBoundingClientRect().height / remoconResolution[1]),
                  width:
                    coor.rightBottom.right * (imageRef.current!.getBoundingClientRect().width / remoconResolution[0]) -
                    coor.leftTop.left * (imageRef.current!.getBoundingClientRect().width / remoconResolution[0]),
                }}
              />
            )
          })}
      </div>
    )
  },
)

ButtonSquares.displayName = 'ButtonSquares'
export default ButtonSquares
