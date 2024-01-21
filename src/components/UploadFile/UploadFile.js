import './UploadFile.css'

import { useState, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import { triggerBase64Download } from 'react-base64-downloader'

export default function UploadFile({ progressBarStepValue, setProgressBarValue, fileDataURL, setFileDataURL, secretEmbeddedImage, setMetaText, nextMetaText }) {
    const [ fileLayers, setFileLayers ] = useState([])
    const [ isSpinnerVisible, setSpinnerVisibility ] = useState(false)

    const { getRootProps, getInputProps } = useDropzone({
        accept: {
            'image/jpeg': [],
            'image/png': []
        },
        onDrop: (acceptedFile) => {
            const fileReader = new FileReader()
            
            fileReader.onabort = () => console.log('File reading was aborted.')
            fileReader.onerror = () => console.log('File reading has failed.')
            fileReader.onload = (e) => {
                setFileDataURL(e?.target?.result)
            }
            
            fileReader.readAsDataURL(acceptedFile[0])
        }
    })

    const fetchImageLayers = async () => {
        setProgressBarValue(progressBarStepValue);
        setSpinnerVisibility(true)

        const response = await fetch("http://localhost:5000/extract_secret", {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "stego_image_path": fileDataURL.split(',')[1]
            })
        })
        
        const data = await response.json()

        setFileLayers(data.layers)
        setMetaText(nextMetaText)
        setSpinnerVisibility(false)
    }

    useEffect(() => {
        if (fileDataURL !== null) {
            fetchImageLayers()
        }
    }, [fileDataURL])

    return (
        <>
            {
                secretEmbeddedImage !== null ?
                <div id='secret-image-wrapper'>
                    <img id='secret-image' src={secretEmbeddedImage} alt='secret-embedded'></img>
                    <div id='download-button' onClick={() => triggerBase64Download(secretEmbeddedImage, "secret_embedded_image")}>Download</div>
                </div> :
                <div id='upload-file-wrapper' {...getRootProps()}>
                    <input {...getInputProps()} />

                    {
                        fileLayers.length === 0 ?
                        <>
                            <img id='upload-file-icon' alt='upload-file-icon' src='https://i.imgur.com/KFRAvbY.png'></img>
                            <div id='upload-file-text-wrapper'>
                                <h3 id='upload-file-text-title'>
                                    Drop your image here or browse.
                                </h3>
                                <h3 id='upload-file-text-meta'>
                                    Supports any image MIME sub-type.
                                </h3>
                            </div>
                        </>
                        :
                        <div id="upload-file-uploaded-wrapper">
                            <img id="upload-file-uploaded" src={fileDataURL} alt=''></img>
                            <div id="upload-file-uploaded-layers">
                                {
                                    isSpinnerVisible ? 
                                        <div id="upload-file-spinner">
                                            <div></div>
                                            <div></div>
                                            <div></div>
                                            <div></div>
                                        </div> : 
                                        fileLayers.map((layer, index) => {
                                            return (
                                                <div className="upload-file-uploaded-layers-wrapper" key={`layer ${index + 1}`}>
                                                    <img className="upload-file-uploaded-layer" key={`layer ${index + 1}`} src={`data:image/png;base64,${layer}`} alt={`layer ${index + 1}`}></img>
                                                    <p className="upload-file-uploaded-layer-label">{`Layer ${index + 1}`}</p>
                                                </div>
                                            )
                                        })
                                }
                            </div>
                        </div>
                    }
                </div>
            }
        </>
    )
}