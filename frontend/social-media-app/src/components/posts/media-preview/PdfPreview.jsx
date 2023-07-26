import React from "react";
import "./css/mediaPreviewStyles.css";

export default function PdfPreview({ url }) {
  return (
    <div className="media-box">
      <div className="pdf-icon">PDF</div>
      <a href={url} target="_blank" rel="noopener noreferrer">
        View PDF
      </a>
    </div>
  );
}
