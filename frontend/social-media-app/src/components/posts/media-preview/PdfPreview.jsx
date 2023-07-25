import React from 'react'

export default function PdfPreview({file}) {
    return (
        <iframe
          title="File preview"
          src={URL.createObjectURL(file)}
          style={{ width: '100%', height: '100%', border: 'none' }}
        />
      );
}
