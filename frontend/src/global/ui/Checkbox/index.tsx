import React from 'react'
import classnames from 'classnames/bind'
import { ReactComponent as CheckIcon } from '@assets/images/check.svg'
import styles from './Checkbox.module.scss'
import { Text } from '..'

const cx = classnames.bind(styles)

interface CheckboxProps {
  colorScheme: 'dark' | 'light'
  isChecked: boolean
  label?: string
}

/**
 * 체크 박스
 *
 * @param label 체크박스 오른쪽에 표시될 라벨
 */
const Checkbox: React.FC<CheckboxProps> = ({ colorScheme, isChecked, label }) => {
  return (
    <button type="button" aria-label="checkbox" className={cx('flex items-center')}>
      <div
        className={cx('rounded-[3px] w-4 h-4 p-0.5 flex justify-center items-center', {
          'bg-primary': isChecked,
          'bg-light-black border border-grey': !isChecked && colorScheme === 'light',
          'bg-white border border-light-grey': !isChecked && colorScheme === 'dark',
        })}
      >
        {isChecked && <CheckIcon className={cx('icon')} />}
      </div>

      {label && (
        <Text size="xs" weight="medium" className="pl-2" colorScheme={colorScheme}>
          {label}
        </Text>
      )}
    </button>
  )
}

export default Checkbox
