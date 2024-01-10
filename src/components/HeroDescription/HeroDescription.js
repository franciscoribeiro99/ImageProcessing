import { useState } from 'react'

import './HeroDescription.css'

export default function HeroDescription({ progressBarValue, withTextInput, title, meta }) {
    const [inputValue, setInputValue] = useState('')
    
    const handleInputChange = (e) => {
        setInputValue(e.target.value)
    }
    
    const handleClick = () => {
        console.log(inputValue)
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
                        <input id='hero-input' type='text' placeholder='My message..' onChange={e => handleInputChange(e)}></input>
                        <div id='hero-button' onClick={handleClick}>Embed</div>
                    </div>
                    : <></>
                }
            </div>
            <progress id='hero-progress-bar' value={progressBarValue} max={100}></progress>
        </>
    )
}