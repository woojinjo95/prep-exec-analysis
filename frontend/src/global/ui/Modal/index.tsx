import React from 'react'
import cx from 'classnames'
import { Title } from '@global/ui'
import { useOutsideClick } from '@global/hook'

interface ModalProps {
  isOpen: boolean
  close: () => void
  children: React.ReactNode
  className?: string
  title?: string
}

/**
 * Modal Components
 *
 * @param isOpen: 모달 display 조절
 * @param close: 모달 close 시 실행 함수
 * @param className: 모달 style 조절
 * @param children: 모달 children
 * @param title: 모달 제목
 * @returns
 */

const Modal: React.FC<ModalProps> = ({ isOpen, close, children, className, title }) => {
  const { ref } = useOutsideClick<HTMLDivElement>({
    mode: 'position',
    onClickOutside: () => {
      close()
    },
  })

  return (
    <div className="fixed top-0 left-0 w-screen h-screen flex justify-center items-center z-20">
      <div
        ref={ref}
        className={cx(
          'flex flex-col fixed min-h-[200px] min-w-[200px] max-w-[90vw] max-h-[90vh] z-10 p-6 bg-light-black rounded-[10px] pb-7',
          className,
        )}
        style={{ display: !isOpen ? 'none' : '' }}
      >
        <Title as="h1" colorScheme="light" className="mb-5">
          {title}
        </Title>
        {children}
      </div>
      <div className="w-full h-full z-[5] bg-black opacity-[0.6]" style={{ display: isOpen ? 'block' : 'none' }} />
    </div>
  )
}

export default Modal
