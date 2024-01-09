import './HeroDescription.css'

export default function HeroDescription({ progressBarValue }) {
    return (
        <>
            <div id='hero-description-wrapper'>
                <h1 id='hero-description-title'>Embed and hide any text into your image.</h1>
                <h2 id='hero-description-meta'>Please first upload your file.</h2>
            </div>
            <progress id='hero-progress-bar' value={progressBarValue} max={100}></progress>
        </>
    )
}