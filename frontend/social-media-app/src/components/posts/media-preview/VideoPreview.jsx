import React from 'react'

export default function VideoPreview({file}) {
    return (
        <video controls style={{ width: '100%', height: '100%' }}>
          <source src={URL.createObjectURL(file)} type={file.type} />
          Your browser does not support the video tag.
        </video>
      );
}
