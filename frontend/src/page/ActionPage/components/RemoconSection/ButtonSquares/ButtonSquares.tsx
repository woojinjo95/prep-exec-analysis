import { KeyEvent } from '@page/ActionPage/constants'
import React, { useEffect, useState } from 'react'

interface ButtonSquaresProps {
  event: KeyEvent | null
  keyboardCoors?: { leftTop: { left: number; top: number }; rightBottom: { right: number; bottom: number } }[]
}

const ButtonSquares = ({ event, keyboardCoors }: ButtonSquaresProps): JSX.Element => {
  const [isSquareVisible, setIsSquareVisible] = useState<boolean>(false)

  useEffect(() => {
    if (event?.altKey && event.code === 'KeyR') {
      setIsSquareVisible(true)
    }
    if (!event?.altKey) {
      setIsSquareVisible(false)
    }
  }, [event])

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
