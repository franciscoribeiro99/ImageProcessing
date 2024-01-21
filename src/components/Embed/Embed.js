import { useState } from 'react'

import './Embed.css'

import Status from '../Status/Status'
import Navigation from '../Navigation/Navigation'
import HeroDescription from '../HeroDescription/HeroDescription'
import UploadFile from '../UploadFile/UploadFile'

export default function Embed() {
    // the different states that shall be shared between
    // the children of this component are all defined here
    // they enable the animation-like transitions between
    // the different states
    
    const [ progressBarValue, setProgressBarValue ] = useState(0)
    const [ fileDataURL, setFileDataURL ] = useState(null)
    const [ secretEmbeddedImage, setSecretEmbeddedImage ] = useState(null)
    const [ withTextInput, setWithTextInput ] = useState(true)
    const [ metaText, setMetaText ] = useState('Please first upload your file 👉')

    return (
        <div id='embed-wrapper'>
            <Status />
            <Navigation />
            <HeroDescription progressBarValue={progressBarValue} setProgressBarValue={setProgressBarValue} fileDataURL={fileDataURL} setSecretEmbeddedImage={setSecretEmbeddedImage} withTextInput={withTextInput} setWithTextInput={setWithTextInput} title={'Embed and hide any text into your image'} meta={metaText} setMetaText={setMetaText} />
            <UploadFile progressBarStepValue={50} setProgressBarValue={setProgressBarValue} fileDataURL={fileDataURL} setFileDataURL={setFileDataURL} secretEmbeddedImage={secretEmbeddedImage} setMetaText={setMetaText} nextMetaText='Please input the secret that shall be hidden into the image.' />
        </div>
    )
}