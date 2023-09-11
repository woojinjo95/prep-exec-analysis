import React from 'react'
import { ReactComponent as DefaultSortIcon } from '@assets/images/icon_sort_default.svg'
import { ReactComponent as AscSortIcon } from '@assets/images/icon_sort_ascending.svg'
import { ReactComponent as DescSortIcon } from '@assets/images/icon_sort_descending.svg'
import { SimpleButton } from '..'

interface SortButtonProps<SortBy extends string, SortByValue extends SortBy> {
  value: SortByValue
  sortBy?: SortBy
  setSortBy: (value: React.SetStateAction<SortBy | undefined>) => void
  sortDesc: boolean
  setSortDesc: (value: React.SetStateAction<boolean>) => void
}

/**
 * 정렬 버튼 컴포넌트
 */
const SortButton = <SortBy extends string, SortByValue extends SortBy>({
  value,
  sortBy,
  setSortBy,
  sortDesc,
  setSortDesc,
}: SortButtonProps<SortBy, SortByValue>): React.ReactElement => {
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
