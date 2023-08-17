import React from 'react'
import classnames from 'classnames/bind'
import styles from './IconButton.module.scss'

const cx = classnames.bind(styles)

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon?: React.ReactNode
  colorScheme?: 'charcoal' | 'light'
  className?: string
}

const IconButton: React.FC<IconButtonProps> = ({
  icon,
  colorScheme = 'light',
  type = 'button',
  className,
  ...props
}) => {
  return (
    <button
      // eslint-disable-next-line react/button-has-type
      type={type}
      className={cx(
        'w-[52px] h-10 rounded-full flex justify-center items-center border transition-all',
        {
          'bg-charcoal': colorScheme === 'charcoal',
          'border-light-charcoal': colorScheme === 'charcoal',
          'hover:brightness-110': colorScheme === 'charcoal',
          'active:brightness-95': colorScheme === 'charcoal',
          'bg-white': colorScheme === 'light',
          'border-light-grey': colorScheme === 'light',
        },
        className,
      )}
      {...props}
    >
      <div className={cx('icon-button-icon', colorScheme)}>{icon}</div>
    </button>
  )
}

export default IconButton