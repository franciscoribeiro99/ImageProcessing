import { useState, useEffect } from 'react'

import './Status.css'

export default function Status() {
    const [isServiceUp, setServiceStatus] = useState(null)
    useEffect(() => {
        const checkStatus = setInterval(async () => {
            try {
                const response = await fetch('http://localhost:5000/status')
                setServiceStatus(response?.ok)
            } catch (_) {
                setServiceStatus(false)
            }
        }, 2000)

        return () => { clearInterval(checkStatus) }
    }, [])
    
    return (
        <div id='landing-status'>
            {
                isServiceUp === null ? "Aucune information disponible" : isServiceUp ? "Le service est actif ✅" : "Le service est inactif ❌"
            }
        </div>
    )
}