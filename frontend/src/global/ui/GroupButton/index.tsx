import React from 'react'
import classnames from 'classnames/bind'
import { Text } from '@global/ui'
import style from './GroupButton.module.scss'

const cx = classnames.bind(style)

interface GroupButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isActive?: boolean
  icon?: React.ReactNode
  children: React.ReactNode
}

/**
 * ButtonGroup 하위에서 사용하는 컴포넌트
 */
const GroupButton: React.FC<GroupButtonProps> = ({ isActive = false, icon, children, ...props }) => {
  return (
    <button
      type="button"
      className={cx('flex items-center gap-x-2 py-2 px-7 rounded-lg', {
        'bg-primary': isActive,
      })}
      {...props}
    >
      {icon && (
        <div
          className={cx('group-button-icon', {
            active: isActive,
            deactive: !isActive,
          })}
        >
          {icon}
        </div>
      )}
      <Text colorScheme="light" size="sm" weight="medium" isActive={isActive}>
        {children}
      </Text>
    </button>
  )
}

export default GroupButton
