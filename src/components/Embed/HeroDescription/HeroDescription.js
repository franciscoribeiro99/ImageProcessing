import './HeroDescription.css'

export default function HeroDescription() {
    return (
        <div id='hero-description-wrapper'>
            <h1 id='hero-description-title'>Embed and hide any text into your image.</h1>
            <h2 id='hero-description-meta'>Please first upload your file.</h2>
            <progress id='hero-progress-bar' max={100}></progress>
        </div>
    )
}