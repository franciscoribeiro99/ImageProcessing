import './UploadFile.css'

import { useState, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'

export default function UploadFile({ setProgressBarValue }) {
    const [ fileDataURL, setFileDataURL ] = useState(null)
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

    useEffect(() => {
        if (fileDataURL !== null) {
            setProgressBarValue(50);
            // fetch("http://localhost:8000/layers", {
            //     method: 'post',
            //     headers: {
            //         'Content-Type': 'application/json'
            //     },
            //     mode: 'cors',
            //     body: JSON.stringify({
            //         "image": fileDataURL
            //     })
            // })
        }
    }, [fileDataURL])

    return (
        <div id='upload-file-wrapper' {...getRootProps()}>
            <input {...getInputProps()} />

            { 
                fileDataURL === null ?
                <>
                    <img id='upload-file-icon' alt='upload-file-icon' src='https://i.imgur.com/KFRAvbY.png'></img>
                    <div id='upload-file-text-wrapper'>
                        <h3 id='upload-file-text-title'>
                            Drop your image here or browse.
                        </h3>
                        <h3 id='upload-file-text-meta'>
                            Supports PNG, JPG and JPEG.
                        </h3>
                    </div>
                </>
                :
                <div id="upload-file-uploaded-wrapper">
                    <img id="upload-file-uploaded" src={fileDataURL} alt=''></img>
                    <div id="upload-file-uploaded-layers">
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                        <img className="upload-file-uploaded-layer" src={fileDataURL} alt=''></img>
                    </div>
                </div>
            }
        </div>
    )
}