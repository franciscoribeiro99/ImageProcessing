import { useState } from 'react'

import './Embed.css'

import HeroDescription from './HeroDescription/HeroDescription'
import UploadFile from './UploadFile/UploadFile'

export default function Embed() {
    const [progressBarValue, setProgressBarValue] = useState(0)

    return (
        <div id='embed-wrapper'>
            <HeroDescription progressBarValue={progressBarValue} />
            <UploadFile setProgressBarValue={setProgressBarValue} />
        </div>
    )
}