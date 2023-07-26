import React from "react";
import "./css/mediaPreviewStyles.css";
export default function ImagePreview({ url }) {
  return (
    <div className="media-box">
      <img
        className="media-image"
        src={url}
        alt="File preview"
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
    </div>
  );
}
