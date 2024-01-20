import { useState } from 'react'

import './Reveal.css'

import Status from '../Status/Status'
import Navigation from '../Navigation/Navigation'
import HeroDescription from '../HeroDescription/HeroDescription'
import UploadFile from '../UploadFile/UploadFile'

export default function Reveal() {
    const [progressBarValue, setProgressBarValue] = useState(0)
    const [fileDataURL, setFileDataURL] = useState(null)
    const [metaText, setMetaText] = useState('Please first upload your file 👉')

    return (
        <div id='reveal-wrapper'>
            <Status />
            <Navigation />
            <HeroDescription progressBarValue={progressBarValue} withTextInput={false} title={'Take a look into your image for any hidden message 👀'} meta={metaText} setProgressBarValue={null} fileDataURL={null} setSecretEmbeddedImage={null} setWithTextInput={null} />
            <UploadFile progressBarStepValue={100} setProgressBarValue={setProgressBarValue} fileDataURL={fileDataURL} setFileDataURL={setFileDataURL} secretEmbeddedImage={null} setMetaText={setMetaText} nextMetaText='Voilà, all the secrets are yours !' />
        </div>
    )
} 