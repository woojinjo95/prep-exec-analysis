import React, { useState } from 'react'
import classnames from 'classnames/bind'
import { ReactComponent as DropdownIcon } from '@assets/images/select_arrow.svg'
import styles from './Accordion.module.scss'

const cx = classnames.bind(styles)

interface AccordionProps {
  header: React.ReactNode
  children?: React.ReactNode
  colorScheme?: 'dark'
  onClick?: () => void
}

/**
 * 아코디언 컴포넌트
 *
 * TODO: 테두리 색 주입
 */
const Accordion: React.FC<AccordionProps> = ({ header, children, colorScheme = 'dark', onClick }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false)

  return (
    <div>
      <button
        className={cx('px-5 py-3 border w-full grid grid-rows-1 grid-cols-[auto_1fr] items-center gap-x-4 text-left', {
          'text-white': colorScheme === 'dark',
          'bg-light-black': colorScheme === 'dark',
          'border-charcoal': colorScheme === 'dark',
          'rounded-lg': !isOpen,
          'rounded-t-lg !border-b-0': isOpen,
        })}
        type="button"
        onClick={() => {
          if (!children) return
          setIsOpen((prev) => !prev)
          if (!isOpen) {
            onClick?.()
          }
        }}
      >
        <DropdownIcon
          className={cx(
            'w-3 transition-transform',
            {
              'rotate-180': isOpen,
              'not-openable': !children,
            },
            colorScheme,
          )}
        />
        <div>{header}</div>
      </button>

      {isOpen && (
        <div
          className={cx('border border-t-0 rounded-b-lg p-5 pt-0', {
            'bg-light-black': colorScheme === 'dark',
            'border-charcoal': colorScheme === 'dark',
          })}
        >
          <div className="w-full h-[0.5px] bg-light-charcoal mb-3" />
          <div className="px-1">{children}</div>
        </div>
      )}
    </div>
  )
}

export default Accordion
