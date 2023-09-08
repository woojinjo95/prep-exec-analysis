import React from 'react'
import { ReactComponent as DefaultSortIcon } from '@assets/images/icon_sort_default.svg'
import { ReactComponent as AscSortIcon } from '@assets/images/icon_sort_ascending.svg'
import { ReactComponent as DescSortIcon } from '@assets/images/icon_sort_descending.svg'
import { SimpleButton } from '..'

interface SortButtonProps<T extends string, D extends T> {
  value: D
  sortBy?: T
  setSortBy: (value: React.SetStateAction<T | undefined>) => void
  sortDesc: boolean
  setSortDesc: (value: React.SetStateAction<boolean>) => void
}

/**
 * 정렬 버튼 컴포넌트
 */
const SortButton = <T extends string, D extends T>({
  value,
  sortBy,
  setSortBy,
  sortDesc,
  setSortDesc,
}: SortButtonProps<T, D>): React.ReactElement => {
  return (
    <>
      {sortBy !== value && (
        <SimpleButton
          isIcon
          colorScheme="light-charcoal"
          className="p-1.5"
          onClick={() => {
            setSortBy(value)
            setSortDesc(false)
          }}
        >
          <DefaultSortIcon className="w-3 h-3" />
        </SimpleButton>
      )}
      {sortBy === value && !sortDesc && (
        <SimpleButton isIcon colorScheme="light-charcoal" className="p-1.5" onClick={() => setSortDesc(true)}>
          <AscSortIcon className="w-3 h-3" />
        </SimpleButton>
      )}
      {sortBy === value && sortDesc && (
        <SimpleButton isIcon colorScheme="light-charcoal" className="p-1.5" onClick={() => setSortDesc(false)}>
          <DescSortIcon className="w-3 h-3" />
        </SimpleButton>
      )}
    </>
  )
}

SortButton.displayName = 'SortButton'

export default SortButton
