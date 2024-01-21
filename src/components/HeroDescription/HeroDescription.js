import { useState } from 'react'

import './HeroDescription.css'

export default function HeroDescription({ progressBarValue, setProgressBarValue, fileDataURL, setSecretEmbeddedImage, withTextInput, setWithTextInput, title, meta, setMetaText }) {
    const [inputValue, setInputValue] = useState('')
    
    const handleInputChange = (e) => {
        setInputValue(e.target.value)
    }
    
    const handleClick = async () => {
        const response = await fetch("http://localhost:5000/embed_secret", {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "cover_image_path": fileDataURL.split(',')[1],
                "secret_text": inputValue
            })
        })
        
        const data = await response.json()

        setSecretEmbeddedImage(`data:image/png;base64,${data["extracted_image"]}`)
        setProgressBarValue(100)
        setWithTextInput(false)
        setMetaText('Congratulations, you can now download your highly-confidential image 🙊')
    }
    
    return (
        <>
            <div id='hero-wrapper'>
                <div id='hero-description-wrapper'>
                    <h1 id='hero-description-title'>{title}</h1>
                    <h2 id='hero-description-meta'>{meta}</h2>
                </div>

                {
                    withTextInput && progressBarValue !== 0 ?
                    <div id='hero-input-wrapper'>
                        <input id='hero-input' type='text' placeholder='Secret.. 🤫' onChange={e => handleInputChange(e)}></input>
                        <div id='hero-button' onClick={handleClick}>Embed</div>
                    </div>
                    : <></>
                }
            </div>
            <progress id='hero-progress-bar' value={progressBarValue} max={100}></progress>
        </>
    )
}