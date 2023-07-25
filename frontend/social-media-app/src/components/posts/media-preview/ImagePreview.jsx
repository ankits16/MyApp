import React from "react";

export default function ImagePreview({ file }) {
  return (
    <img
      src={URL.createObjectURL(file)}
      alt="File preview"
      style={{ width: "100%", height: "100%", objectFit: "cover" }}
    />
  );
}
