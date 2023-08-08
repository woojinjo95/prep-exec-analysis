import React from 'react'
import cx from 'classnames'

interface ToggleButtonProps {
  isOn: boolean
  colorScheme?: 'charcoal' | 'light'
  onClick?: (isOn: boolean) => void
}

/**
 * on / off 토글 버튼
 *
 * @example
 * <ToggleButton isOn={isOn} onClick={(_isOn) => setIsOn(_isOn)} />
 *
 * @param isOn on / off 여부
 * @param colorScheme 컬러 테마
 *
 */
const ToggleButton: React.FC<ToggleButtonProps> = ({ isOn, colorScheme = 'charcoal', onClick }) => {
  return (
    <button
      type="button"
      className={cx('w-[52px] rounded-full flex items-center', {
        'bg-primary p-0.5': isOn,
        'border p-px': !isOn,
        'bg-charcoal': !isOn && colorScheme === 'charcoal',
        'border-light-charcoal': !isOn && colorScheme === 'charcoal',
      })}
      onClick={() => onClick?.(!isOn)}
    >
      <div
        className="w-6 h-6 bg-white rounded-full transition-all"
        style={{
          transform: `translateX(${isOn ? '100%' : '0%'})`,
        }}
      />
    </button>
  )
}

export default ToggleButton
