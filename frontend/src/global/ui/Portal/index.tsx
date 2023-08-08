import { useEffect } from 'react'
import ReactDOM from 'react-dom'

export default function Portal({ children }: { children: JSX.Element }): JSX.Element {
    const el = document.createElement('div')

    useEffect(() => {
        document.body.appendChild(el)

        return () => {
            document.body.removeChild(el)
        }
    }, [])

    return ReactDOM.createPortal(children, el)
}
