import * as React from 'react';

// import { ossOriginal } from '../style/IconsStyle';
import logoOriginalPNG from '../../style/OSS_original.png'

interface IAboutDialog {
    aboutBody: JSX.Element;
    aboutTitle: JSX.Element
}

export function aboutVoiceAtlasDialog(): IAboutDialog {
    const versionInfo = (
        <span className="jp-About-version-info">
            <span className="jp-About-version">v1.0</span>
        </span>
    );
    const aboutTitle = (
        <span className="jp-About-header">
            <div className="jp-About-header-info">
                <img src={logoOriginalPNG} height="auto" width="196px" />
                {versionInfo}
            </div>
        </span>
    );

    const externalLinks = (
        <span className="jp-About-externalLinks">
            <a
                href='https://navteca.com'
                target="_blank"
                rel="noopener noreferrer"
                className="jp-Button-flat"
            >
                {"About Navteca"}
            </a>
            <br />
            <a
                href='https://voiceatlas.com'
                target="_blank"
                rel="noopener noreferrer"
                className="jp-Button-flat"
            >
                {"About Voice Atlas"}
            </a>
            <br />
            <a
                href='https://opensciencestudio.com'
                target="_blank"
                rel="noopener noreferrer"
                className="jp-Button-flat"
            >
                {"About Open Science Studio"}
            </a>
        </span>
    );
    const copyright = (
        <span className="jp-About-copyright">
            {'© 2024 Voice Atlas by Navteca LLC'}
            <br />
            {'© 2024 Open Science Studio by Navteca LLC'}
        </span>
    );
    const aboutBody = (
        <div className="jp-About-body">
            OSS support is an extension that has been built for the Open Science Studio platform (OSS).
            <br />
            OSS support is powered by NLP provided by Voice Atlas a Navteca AI product.
            {externalLinks}
            {copyright}
        </div>
    );

    return { aboutBody, aboutTitle }
}
