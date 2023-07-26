import React, { useState } from 'react'
import cx from 'classnames'

interface InputProps extends React.HTMLAttributes<HTMLInputElement> {
  className?: string
}

/**
 * 입력창
 */
const Input: React.FC<InputProps> = ({ className, ...props }) => {
  const [isFocused, setIsFocused] = useState<boolean>(false)
  return (
    <div
      className={cx(
        'bg-gray-200 px-4 py-2 rounded-md transition-all',
        {
          'outline outline-2 outline-blue-300': isFocused,
        },
        className,
      )}
    >
      <input
        style={{
          fontFamily: 'Noto-sans',
        }}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className="outline-none w-full bg-transparent placeholder:text-gray-400 text-black"
        {...props}
        placeholder="*7899#"
      />
    </div>
  )
}

export default Input
