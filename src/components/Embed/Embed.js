import { useState } from 'react'

import './Embed.css'

import Status from '../Status/Status'
import Navigation from '../Navigation/Navigation'
import HeroDescription from '../HeroDescription/HeroDescription'
import UploadFile from '../UploadFile/UploadFile'

export default function Embed() {
    const [progressBarValue, setProgressBarValue] = useState(0)

    return (
        <div id='embed-wrapper'>
            <Status />
            <Navigation />
            <HeroDescription progressBarValue={progressBarValue} withTextInput={true} title={'Embed and hide any text into your image'} meta={'Please first upload your file 👉'} />
            <UploadFile setProgressBarValue={setProgressBarValue} />
        </div>
    )
}