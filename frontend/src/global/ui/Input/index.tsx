import React, { useState } from 'react'
import cx from 'classnames'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  className?: string
  colorScheme?: 'dark' | 'charcoal' | 'light'
  warningMessage?: string
  errorMessage?: string
}

/**
 * 입력창
 */
const Input: React.ForwardRefExoticComponent<InputProps & React.RefAttributes<HTMLInputElement>> = React.forwardRef<
  HTMLInputElement,
  InputProps
>(({ className, colorScheme = 'charcoal', ...props }, ref) => {
  const [isFocused, setIsFocused] = useState<boolean>(false)
  return (
    <input
      ref={ref}
      className={cx(
        'outline-none w-full placeholder:text-grey text-white text-[15px] transition-all border py-3 px-4 rounded-lg',
        {
          '!text-black': colorScheme === 'light',

          'bg-light-black': colorScheme === 'dark',
          'bg-charcoal': colorScheme === 'charcoal',
          'bg-white': colorScheme === 'light',

          'border-charcoal': colorScheme === 'dark',
          'border-light-charcoal': colorScheme === 'charcoal',
          'border-light-grey': colorScheme === 'light',
          'border-primary': isFocused,
        },
        className,
      )}
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
  )
})

Input.displayName = 'Input'

export default Input
