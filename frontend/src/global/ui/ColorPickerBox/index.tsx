import React, { useCallback, useRef, useState } from 'react'
import { SketchPicker } from 'react-color'
import cx from 'classnames'
import { createPortal } from 'react-dom'
import { useOutsideClick } from '@global/hook'

const SPACE = 4

interface ColorPickerBoxProps {
  color: string
  className?: string
  onChange?: (color: string) => void
}

/**
 * 색상 선택 박스
 */
const ColorPickerBox: React.FC<ColorPickerBoxProps> = ({ color, className, onChange }) => {
  const [isOpenColorPicker, setIsOpenColorPicker] = useState<boolean>(false)
  const wrapperRef = useRef<HTMLDivElement | null>(null)
  const { ref } = useOutsideClick<HTMLDivElement>({
    mode: 'position',
    onClickOutside: () => {
      setIsOpenColorPicker(false)
    },
  })

  const createDefaultStyle = useCallback((_wrapperRef: React.MutableRefObject<HTMLDivElement | null>) => {
    if (!_wrapperRef.current) return {}

    const styles: React.CSSProperties = {}
    const dimensions = _wrapperRef.current.getBoundingClientRect()

    styles.left = dimensions.left
    if (dimensions.top < window.innerHeight / 2) {
      styles.top = dimensions.top + dimensions.height + SPACE
    } else {
      styles.bottom = window.innerHeight - dimensions.top + SPACE
    }

    return styles
  }, [])

  return (
    <div ref={wrapperRef} className="relative" onClick={(e) => e.stopPropagation()}>
      <div
        className={cx('w-4 h-4 cursor-pointer', className)}
        style={{
          backgroundColor: color,
        }}
        onClick={(e) => {
          e.stopPropagation()
          setIsOpenColorPicker((prev) => !prev)
        }}
      />
      {isOpenColorPicker &&
        createPortal(
          <div
            ref={ref}
            style={createDefaultStyle(wrapperRef)}
            className="fixed z-50"
            onClick={(e) => e.stopPropagation()}
          >
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
          </div>,
          document.body,
        )}
    </div>
  )
}

export default ColorPickerBox
