import useOutsideClick from '@global/hook/useOutsideClick'
import React, { useState } from 'react'
import { SketchPicker } from 'react-color'

interface ColorPickerBoxProps {
  color: string
  onChange?: (color: string) => void
}

/**
 * 색상 선택 박스
 */
const ColorPickerBox: React.FC<ColorPickerBoxProps> = ({ color, onChange }) => {
  const [isOpenColorPicker, setIsOpenColorPicker] = useState<boolean>(false)
  const { ref } = useOutsideClick<HTMLDivElement>({
    mode: 'position',
    onClickOutside: () => {
      setIsOpenColorPicker(false)
    },
  })

  return (
    <div className="relative" onClick={(e) => e.stopPropagation()}>
      <div
        className="w-4 h-4"
        style={{
          backgroundColor: color,
        }}
        onClick={(e) => {
          e.stopPropagation()
          setIsOpenColorPicker((prev) => !prev)
        }}
      />
      {isOpenColorPicker && (
        <div ref={ref} className="absolute top-0 left-0 mt-6" onClick={(e) => e.stopPropagation()}>
          {/* FIXME: preset 컬러 선택안됨 */}
          <SketchPicker
            disableAlpha
            className="text-black"
            color={color}
            onChange={(color, e) => {
              e.stopPropagation()

              const red = color.rgb.r.toString(16).padStart(2, '0')
              const green = color.rgb.g.toString(16).padStart(2, '0')
              const blue = color.rgb.b.toString(16).padStart(2, '0')

              onChange?.(`#${red}${green}${blue}`)
            }}
          />
        </div>
      )}
    </div>
  )
}

export default ColorPickerBox
