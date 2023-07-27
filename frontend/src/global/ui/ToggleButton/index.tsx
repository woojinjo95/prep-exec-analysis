import React from 'react'
import cx from 'classnames'

interface ToggleButtonProps {
  isOn: boolean
  onClick?: (isOn: boolean) => void
}

/**
 * on / off 토글 버튼
 *
 * @example
 * <ToggleButton isOn={isOn} onClick={(_isOn) => setIsOn(_isOn)} />
 *
 * @param isOn on / off 여부
 *
 */
const ToggleButton: React.FC<ToggleButtonProps> = ({ isOn, onClick }) => {
  return (
    <button
      type="button"
      className={cx('w-11 h-6 rounded-full flex items-center px-0.5', {
        'bg-gray-300': !isOn,
        'bg-blue-300': isOn,
      })}
      onClick={() => onClick?.(!isOn)}
    >
      <div
        className="w-5 h-5 bg-white rounded-full transition-all"
        style={{
          transform: `translateX(${isOn ? '100%' : '0%'})`,
        }}
      />
    </button>
  )
}

export default ToggleButton
