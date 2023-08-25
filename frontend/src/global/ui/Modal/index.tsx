import React from 'react'
import cx from 'classnames'
import useOutSideRef from '@global/hook/useOutsideRef'

interface ModalProps {
  mode?: 'center' | 'normal'
  isOpen: boolean
  close: () => void
  children: React.ReactNode
  className?: string
}

/**
 * Modal Components
 *
 * @param mode 모달 모드 : center : 중앙에 위치하는 center 모달 | normal(기본) : className을 통해 직접 position을 조절해야 함
 * @param isOpen: 모달 display 조절
 * @param close: 모달 close 시 실행 함수
 * @param className: 모달 style 조절
 * @param children: 모달 children
 * @returns
 */

const Modal: React.FC<ModalProps> = ({ mode = 'normal', isOpen, close, children, className }) => {
  const { ref } = useOutSideRef({
    isOpen,
    closeHook: () => {
      close()
    },
  })

  return (
    <>
      <div
        ref={ref}
        className={cx(
          'fixed min-h-[200px] min-w-[200px] z-10',
          {
            'fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2': mode === 'center',
          },
          className,
        )}
        style={{ display: !isOpen ? 'none' : '' }}
      >
        {children}
      </div>
      <div
        className="fixed top-0 left-0 w-full h-full z-[5] bg-black opacity-[0.6]"
        style={{ display: isOpen ? 'block' : 'none' }}
      />
    </>
  )
}

export default Modal
