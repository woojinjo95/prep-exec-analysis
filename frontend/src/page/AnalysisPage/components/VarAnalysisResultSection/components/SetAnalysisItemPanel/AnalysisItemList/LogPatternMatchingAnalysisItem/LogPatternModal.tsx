import React, { useState } from 'react'
import { Button, ColorPickerBox, Input, Modal, Select, Title, Text, OptionItem, CodeEditor } from '@global/ui'
import { LogLevel } from '@global/constant'
import { useMutation } from 'react-query'
import { postValidateRegex } from '@page/AnalysisPage/components/VarAnalysisResultSection/api/func'
import { UnsavedAnalysisConfig } from '@page/AnalysisPage/components/VarAnalysisResultSection/types'

interface LogPatternModalProps {
  isOpen: boolean
  close: () => void
  pattern?: NonNullable<UnsavedAnalysisConfig['log_pattern_matching']>['items'][number]
  patterns: NonNullable<UnsavedAnalysisConfig['log_pattern_matching']>['items']
  setUnsavedAnalysisConfig: React.Dispatch<React.SetStateAction<UnsavedAnalysisConfig>>
}

/**
 * 로그 패턴 추가 및 수정 모달
 *
 * TODO:
 */
const LogPatternModal: React.FC<LogPatternModalProps> = ({
  isOpen,
  close,
  pattern,
  patterns,
  setUnsavedAnalysisConfig,
}) => {
  const [name, setName] = useState<string>(pattern?.name || '')
  const [logLevel, setLogLevel] = useState<keyof typeof LogLevel>(pattern?.level || 'V')
  const [regex, setRegex] = useState<string>(pattern?.regular_expression || '')
  const [isValidRegex, setIsValidRegex] = useState<boolean | null>(null)
  const [color, setColor] = useState<string>(pattern?.color || 'red')
  const [warningMessage, setWarningMessage] = useState<{ name: string | null; regex: string | null }>({
    name: null,
    regex: null,
  })
  const { mutate: validateRegex } = useMutation(postValidateRegex, {
    onSuccess: (data) => {
      if (data.is_valid) {
        setIsValidRegex(true)
        setWarningMessage((prev) => ({ ...prev, regex: '' }))
      } else {
        setIsValidRegex(false)
        setWarningMessage((prev) => ({ ...prev, regex: 'Is not valid regular expression.' }))
      }
    },
    onError: () => {
      setIsValidRegex(false)
      setWarningMessage((prev) => ({ ...prev, regex: 'An error has occurred. please try again.' }))
    },
  })

  const onSubmit = () => {
    let isNotValid = false

    // 이름이 비어있을 경우
    if (!name) {
      setWarningMessage((prev) => ({ ...prev, name: 'Enter name.' }))
      isNotValid = true
    } else {
      setWarningMessage((prev) => ({ ...prev, name: '' }))
    }

    // 이름이 중복될 경우
    if (pattern?.name !== name && patterns.filter(({ name: _name }) => _name === name).length) {
      setWarningMessage((prev) => ({ ...prev, name: 'Duplicate name. Please use a different name.' }))
      isNotValid = true
    } else {
      setWarningMessage((prev) => ({ ...prev, name: '' }))
    }

    // 정규표현식이 유효하지 않을 경우
    if (!regex) {
      setWarningMessage((prev) => ({ ...prev, regex: 'Please enter a regular expression.' }))
      setIsValidRegex(false)
      isNotValid = true
    } else {
      setWarningMessage((prev) => ({ ...prev, regex: '' }))
    }

    // 정규표현식 체크를 통과하지 않은 경우
    if (!isValidRegex) {
      setWarningMessage((prev) => ({ ...prev, regex: 'Checking regular expressions is essential.' }))
      setIsValidRegex(false)
      isNotValid = true
    } else {
      setWarningMessage((prev) => ({ ...prev, regex: '' }))
    }

    if (isNotValid) return

    // modify
    if (pattern) {
      setUnsavedAnalysisConfig((prev) => ({
        ...prev,
        log_pattern_matching: {
          ...prev.log_pattern_matching!,
          items: [
            ...prev.log_pattern_matching!.items.filter((p) => p.name !== pattern.name),
            {
              color,
              name,
              level: logLevel,
              regular_expression: regex,
            },
          ],
        },
      }))
      close()
      return
    }

    // add
    setUnsavedAnalysisConfig((prev) => ({
      ...prev,
      log_pattern_matching: {
        ...prev.log_pattern_matching!,
        items: [
          ...prev.log_pattern_matching!.items,
          {
            color,
            name,
            level: logLevel,
            regular_expression: regex,
          },
        ],
      },
    }))
    close()
  }

  return (
    <Modal
      isOpen={isOpen}
      close={close}
      title={pattern ? 'Modify Log Pattern' : 'Add Log Pattern'}
      className="w-[60vw] h-[60vh] min-h-[600px] min-w-[960px]"
    >
      <div className="w-full h-full grid grid-cols-[auto_1fr] grid-rows-[auto_auto_1fr_auto_auto] gap-x-10 gap-y-3">
        <Title as="h3" colorScheme="light" className="pt-3">
          Log Pattern Name
        </Title>
        <div className="flex">
          <Input
            placeholder="Untitled Log Pattern"
            className="w-80"
            value={name}
            onChange={(e) => setName(e.target.value)}
            warningMessage={warningMessage.name || ''}
          />
        </div>

        <Title as="h3" colorScheme="light" className="pt-3">
          Log Level
        </Title>
        <div className="flex">
          <Select
            colorScheme="charcoal"
            className="w-32"
            widthOption="fit-wrapper"
            header={
              <Text weight="bold" colorScheme="light">
                {logLevel}
              </Text>
            }
          >
            {Object.keys(LogLevel).map((_level) => {
              const level = _level as keyof typeof LogLevel

              return (
                <OptionItem
                  key={`add-log-pattern-modal-log-level-list-${level}`}
                  colorScheme="charcoal"
                  onClick={() => {
                    setLogLevel(level)
                  }}
                  isActive={level === logLevel}
                >
                  {level}
                </OptionItem>
              )
            })}
          </Select>
        </div>

        <Title as="h3" colorScheme="light" className="pt-3">
          Regular Expression
        </Title>
        <div className="grid grid-cols-1 grid-rows-[1fr_auto] gap-y-2">
          <CodeEditor code={regex} setCode={setRegex} />

          <div>
            <Button
              className="charcoal"
              onClick={() => {
                if (!regex.length) {
                  setWarningMessage((prev) => ({ ...prev, regex: 'Please enter a regular expression.' }))
                  setIsValidRegex(false)
                  return
                }

                validateRegex({ regex })
              }}
            >
              Check Validation
            </Button>
            {isValidRegex === true && (
              <Text className="ml-7" colorScheme="light">
                Is valid regular expression.
              </Text>
            )}
            {isValidRegex === false && (
              <Text className="ml-7" colorScheme="orange">
                {warningMessage.regex || 'Is not valid regular expression.'}
              </Text>
            )}
          </div>
        </div>

        <div>
          <Title as="h3" colorScheme="light">
            Color
          </Title>
        </div>
        <div className="flex items-center">
          <ColorPickerBox color={color} className="!w-12 h-5" onChange={(color) => setColor(color)} />
        </div>

        <div className="col-span-2 flex justify-end items-center gap-x-3">
          <Button colorScheme="primary" onClick={onSubmit}>
            Save
          </Button>
          <Button colorScheme="grey" onClick={close}>
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default LogPatternModal
