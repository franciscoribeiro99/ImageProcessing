import { useState } from 'react'

import './Reveal.css'

import Status from '../Status/Status'
import Navigation from '../Navigation/Navigation'
import HeroDescription from '../HeroDescription/HeroDescription'
import UploadFile from '../UploadFile/UploadFile'

export default function Reveal() {
    const [progressBarValue, setProgressBarValue] = useState(0)

    return (
        <div id='reveal-wrapper'>
            <Status />
            <Navigation />
            <HeroDescription progressBarValue={progressBarValue} withTextInput={false} title={'Take a look into your image for any hidden message 👀'} meta={'Please first upload your file 👉'} />
            <UploadFile setProgressBarValue={setProgressBarValue} />
        </div>
    )
} 