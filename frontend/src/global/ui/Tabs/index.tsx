import React, { useState } from 'react'
import classnames from 'classnames/bind'
import { Text } from '@global/ui'

import styles from './Tabs.module.scss'

const cx = classnames.bind(styles)

interface TabsProps {
  header: string[]
  children?: React.ReactNode | React.ReactNode[]
  className?: string
  theme?: 'dark' | 'light'
}

/**
 * 탭 및 탭 패널 컴포넌트
 *
 * @param header 탭 이름들
 * @param children 단일 탭패널 컴포넌트 또는 탭패널 컴포넌트 리스트
 * @param theme 탭 테마(다크모드 또는 라이트모드)
 */
const Tabs: React.FC<TabsProps> = ({ header, children, className, theme = 'light' }) => {
  const [activeIndex, setActiveIndex] = useState<number>(0)

  return (
    <div
      className={cx(
        'grid grid-cols-1 grid-rows-[auto_1fr] gap-y-2 h-full',
        'tab-panel',
        {
          'bg-black': theme === 'dark',
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
              'border-b-2 border-blue-300': index === activeIndex,
              'cursor-default': header.length < 2,
            })}
            onClick={() => setActiveIndex(index)}
          >
            <Text
              weight="medium"
              theme={theme}
              className={cx({
                'text-gray-500': index !== activeIndex,
              })}
            >
              {name}
            </Text>
          </button>
        ))}
      </div>

      {React.Children.toArray(children).map((c, index) =>
        index === activeIndex ? (
          <div key={`tab-panel-${index}`} className={cx('tab-panel', theme)}>
            {c}
          </div>
        ) : null,
      )}
    </div>
  )
}

export default Tabs
