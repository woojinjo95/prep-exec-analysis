import React, { useState } from 'react'
import cx from 'classnames'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string
}

/**
 * 입력창
 */
const Input: React.ForwardRefExoticComponent<InputProps & React.RefAttributes<HTMLInputElement>> = React.forwardRef<
  HTMLInputElement,
  InputProps
>(({ className, ...props }, ref) => {
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
        ref={ref}
        className="outline-none w-full bg-transparent placeholder:text-grey text-black text-[15px]"
        {...props}
        onFocus={(e) => {
          setIsFocused(true)
          props.onFocus?.(e)
        }}
        onBlur={(e) => {
          setIsFocused(false)
          props.onBlur?.(e)
        }}
        // TODO: esc key 누를 시 -> input blur
      />
    </div>
  )
})

Input.displayName = 'Input'

export default Input
