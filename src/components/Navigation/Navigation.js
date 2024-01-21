import { Link } from 'react-router-dom'

import './Navigation.css'

export default function Navigation() {
    const handleTipClick = () => {
        window.open('https://www.buymeacoffee.com/dionosmani', "_blank", "noreferrer")
    }
    
    return (
        <nav id='navigation-wrapper'>
            <Link to='/'>Home</Link>
            <Link to='/embed'>Embed</Link>
            <Link to='/reveal'>Reveal</Link>
            <div id='navigation-tip' onClick={handleTipClick}></div>
        </nav>
    )
}