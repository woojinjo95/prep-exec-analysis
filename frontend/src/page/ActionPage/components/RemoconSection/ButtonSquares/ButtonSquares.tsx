import { KeyEvent } from '@page/ActionPage/types'
import React, { useEffect, useState } from 'react'

interface ButtonSquaresProps {
  keyEvent: KeyEvent | null
  keyboardCoors?: { leftTop: { left: number; top: number }; rightBottom: { right: number; bottom: number } }[]
}

const ButtonSquares = ({ keyEvent, keyboardCoors }: ButtonSquaresProps): JSX.Element => {
  const [isSquareVisible, setIsSquareVisible] = useState<boolean>(false)

  useEffect(() => {
    if (keyEvent?.altKey && keyEvent.code === 'KeyR') {
      setIsSquareVisible(true)
    }
    if (!keyEvent?.altKey) {
      setIsSquareVisible(false)
    }
  }, [keyEvent])

  return (
    <div className="relative">
      {keyboardCoors &&
        isSquareVisible &&
        keyboardCoors.map((coor) => {
          return (
            <div
              key={`button_square_${coor.leftTop.left}_${coor.leftTop.top}`}
              className="absolute border-orange-300 border-2"
              style={{
                display: isSquareVisible ? '' : 'none',
                top: coor.leftTop.top,
                left: coor.leftTop.left,
                height: coor.rightBottom.bottom - coor.leftTop.top,
                width: coor.rightBottom.right - coor.leftTop.left,
              }}
            />
          )
        })}
    </div>
  )
}

export default ButtonSquares
