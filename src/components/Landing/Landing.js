import { Outlet, Link } from 'react-router-dom'

import './Landing.css'

export default function Landing() {
    return (
        <>
            <div id='landing-wrapper'>
                <div id='landing-wrapper-inner'>
                    <h1 id='landing-wrapper-title'>
                        Mon message caché.. 🤫
                    </h1>
                    <p id='landing-wrapper-meta'>
                        Explorez la magie de la confidentialité visuelle avec notre service web innovant ! Notre plateforme vous permet de dissimuler habilement des messages confidentiels à l'intérieur d'images ordinaires. En utilisant notre technique unique de superposition de couches, vous pouvez diviser ces images en strates distinctes, révélant ainsi le contenu caché. Protégez vos informations sensibles de manière ludique et ingénieuse tout en garantissant une sécurité visuelle incomparable. Avec notre outil convivial, sécurisez vos données de manière créative et confidentielle.
                    </p>
                    <div id='landing-buttons-wrapper'>
                        <div className='landing-button-wrapper'>
                            <Link to='/embed'>Embed</Link>
                        </div>
                        <div className='landing-button-wrapper'>
                            <Link to='/reveal'>Reveal</Link>
                        </div>
                    </div>
                </div>
            </div>
            <Outlet />
        </>
    )
}