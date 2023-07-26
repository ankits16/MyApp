import React, { useRef, useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import DeleteIcon from "@mui/icons-material/Delete";
import PhotoIcon from "@mui/icons-material/Photo";
import VideoIcon from "@mui/icons-material/VideoLibrary";
import PdfIcon from "@mui/icons-material/PictureAsPdf";
import { MenuItem, Select } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import ImagePreview from "./media-preview/ImagePreview";
import VideoPreview from "./media-preview/VideoPreview";
import PdfPreview from "./media-preview/PdfPreview";

const MediaItemInput = ({ mediaItem, onChange, onDelete }) => {
  const inputElementRef = useRef(null); 
  const mediaTypeOptions = [
    { value: 'image', label: 'Image', icon: <PhotoIcon /> },
    { value: 'video', label: 'Video', icon: <VideoIcon /> },
    { value: 'pdf', label: 'PDF', icon: <PdfIcon /> },
  ];

  const getPreviewComponent = () => {
    switch (mediaItem.type) {
      case 'image':
        return <ImagePreview url={URL.createObjectURL(mediaItem.file)} />;
      case 'video':
        return <VideoPreview url={URL.createObjectURL(mediaItem.file)} />;
      case 'pdf':
        return <PdfPreview url={URL.createObjectURL(mediaItem.file)} />;
      default:
        return null;
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === 'type') {
      onChange(name, value, mediaItem.index);
    } else if (name === 'file') {
      const file = e.target.files[0];
      onChange('file', file, mediaItem.index);
    } else {
      onChange(name, value, mediaItem.index);
    }
  };

  return (
    <div className="mb-3">
      <Row>
        <Col xs={6}>
          <Form.Group controlId={`type-${mediaItem.index}`}>
            <Form.Label>Type</Form.Label>
            <Select
              name="type"
              value={mediaItem.type}
              onChange={handleInputChange}
              required
            >
              <MenuItem value="">
                Select type
              </MenuItem>
              {mediaTypeOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.icon} {option.label}
                </MenuItem>
              ))}
            </Select>
            <Form.Control.Feedback type="invalid">
              Please select a media type.
            </Form.Control.Feedback>
          </Form.Group>
        </Col>
        {mediaItem.type && (
          <>
            <Col xs={4}>
              <Form.Group controlId={`file-${mediaItem.index}`}>
                <Form.Label>
                  {mediaItem.type === 'image' ? 'Upload Image' : `Upload ${mediaItem.type.toUpperCase()}`}
                </Form.Label>
                <Form.Control
                  type="file"
                  name="file"
                  accept={`image/${mediaItem.type === 'image' ? '*' : ''}, video/${
                    mediaItem.type === 'video' ? '*' : ''
                  }, .pdf`}
                  onChange={handleInputChange}
                  required
                  style={{ display: 'none' }}
                  ref={(input) => {
                    // Ref to the hidden input element
                    inputElementRef.current = input;
                  }}
                />
                <Button variant="outlined" component="label" htmlFor={`file-${mediaItem.index}`} onClick={() => inputElementRef.current.click()}>
                  {mediaItem.file ? (
                    getPreviewComponent()
                  ) : (
                    <AddCircleOutlineIcon fontSize="large" />
                  )}
                </Button>
                <Form.Control.Feedback type="invalid">
                  Please choose a file.
                </Form.Control.Feedback>
              </Form.Group>
            </Col>
            <Col xs={2} className="d-flex align-items-end">
              <Button variant="danger" onClick={() => onDelete(mediaItem.index)}>
                <DeleteIcon />
              </Button>
            </Col>
          </>
        )}
      </Row>

      {mediaItem.type && (
        <Row>
          <Col xs={12}>
            <Form.Group controlId={`meta-${mediaItem.index}`}>
              <Form.Label>Additional Notes</Form.Label>
              <Form.Control
                type="text"
                name="media-item-notes"
                value={mediaItem.meta['media-item-notes']}
                onChange={handleInputChange}
                required
              />
              <Form.Control.Feedback type="invalid">
                Please provide media meta data.
              </Form.Control.Feedback>
            </Form.Group>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default MediaItemInput;
