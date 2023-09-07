import React from 'react'
import cx from 'classnames'
import { ReactComponent as CloseIcon } from '@assets/images/x.svg'
import { Title, Text, SimpleButton } from '@global/ui'

interface CardModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  subtitle: string
  className?: string
  children: React.ReactNode | React.ReactNode[]
}

/**
 * 원본데이터를 표시할 때 사용하는 카드 모달
 */
const CardModal: React.FC<CardModalProps> = ({ isOpen, onClose, title, subtitle, className, children }) => {
  if (!isOpen) return null
  return (
    <div
      className={cx(
        'z-20 fixed bottom-0 left-0 h-[36vh] w-[calc(65vw+1px)] py-3 px-6 bg-light-black border border-charcoal rounded-t-[10px]',
        className,
      )}
    >
      <div className="pb-2 flex items-center gap-x-5">
        <Title as="h3" colorScheme="light">
          {title}
        </Title>
        <Text weight="medium">{subtitle}</Text>

        <SimpleButton isIcon colorScheme="charcoal" onClick={onClose}>
          <CloseIcon className="fill-white w-3 h-3" />
        </SimpleButton>
      </div>

      <div className="h-[calc(100%-44px)]">{children}</div>
    </div>
  )
}

export default CardModal
