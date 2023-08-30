import React, { useState } from 'react'
import classnames from 'classnames/bind'
import { Title } from '@global/ui'

import styles from './Tabs.module.scss'

const cx = classnames.bind(styles)

interface TabsProps {
  header: string[]
  children?: React.ReactNode | React.ReactNode[]
  className?: string
  colorScheme?: 'dark' | 'charcoal' | 'light'
}

/**
 * 탭 및 탭 패널 컴포넌트
 *
 * @param header 탭 이름들
 * @param children 단일 탭패널 컴포넌트 또는 탭패널 컴포넌트 리스트
 * @param colorScheme 탭 컬러 테마, 텍스트색 기준
 */
const Tabs: React.FC<TabsProps> = ({ header, children, className, colorScheme }) => {
  const [activeIndex, setActiveIndex] = useState<number>(0)

  return (
    <div
      className={cx(
        'grid grid-cols-1 grid-rows-[auto_1fr] gap-y-4 h-full',
        'tab-panel',
        {
          'bg-white': colorScheme === 'light',
          'bg-black': colorScheme === 'dark',
        },
        className,
      )}
    >
      <div>
        {header.map((name, index) => (
          <button
            key={`tab-header-name-${name}`}
            type="button"
            className={cx('p-2 mr-2', {
              'border-b-2 border-primary': index === activeIndex,
              'cursor-default': header.length < 2,
            })}
            onClick={() => setActiveIndex(index)}
          >
            <Title as="h2" colorScheme={colorScheme === 'light' ? 'dark' : 'light'} active={index === activeIndex}>
              {name}
            </Title>
          </button>
        ))}
      </div>

      {React.Children.toArray(children).map((c, index) => (
        <div
          key={`tab-panel-${index}`}
          className={cx(
            'tab-panel',
            'overflow-hidden',
            {
              hidden: index !== activeIndex,
            },
            colorScheme,
          )}
        >
          {c}
        </div>
      ))}
    </div>
  )
}

export default Tabs
