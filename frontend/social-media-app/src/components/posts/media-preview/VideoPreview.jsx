import React from "react";
import "./css/mediaPreviewStyles.css";

export default function VideoPreview({ url }) {
  return (
    <div className="media-box">
      <video controls style={{ width: "100%", height: "100%" }}>
        <source src={url} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
}
