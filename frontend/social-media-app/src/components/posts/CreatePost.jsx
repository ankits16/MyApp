import React, { useContext, useState } from "react";
import { Button, Card, Form, Modal } from "react-bootstrap";
import { getUser } from "../../hooks/user.actions";
import axiosService from "../../helpers/axios";
import Toaster from "../Toaster";
import { Context } from "../Layout";
import MediaItemInput from "./MediaItemInput";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import { v4 as uuidv4 } from "uuid";

const CreatePost = (props) => {
  const { refresh } = props;
  const { setToaster } = useContext(Context);
  const [show, setShow] = useState(false);
  const [form, setForm] = useState({
    body: "",
    mediaItems: [],
  });
  const [validated, setValidated] = useState(false);
  // const [showToast, setShowToast] = useState(false);
  // const [toastMessage, setToastMessage] = useState("");
  // const [toastType, setToastType] = useState("");
  const user = getUser();
  // const [mediaItems, setMediaItems] = useState([]);

  const handleAddMediaItem = () => {
    setForm({
      ...form,
      mediaItems: [
        ...form.mediaItems,
        {
          type: "",
          meta: {},
          file: null,
          index: uuidv4(), // Generate a unique identifier for each media item
        },
      ],
    });
    console.log("Add media item");
  };

  const handleMediaItemChange = (name, value, index) => {
    const updatedMediaItems = form.mediaItems.map((mediaItem) => {
      if (mediaItem.index === index){
        //update existing 
        var updatedMeta = { ...mediaItem.meta };
        var updatedMediaItem = { ...mediaItem };
        if (name === "media-item-notes") {
          updatedMeta["notes"] = value;
          updatedMediaItem.meta = updatedMeta;
          return updatedMediaItem;
        }
        if (name  === "file"){
          updatedMeta["local_identifier"] = index;
          updatedMediaItem.meta = updatedMeta;
          updatedMediaItem.file = value;
          updatedMediaItem.file_name = value.name;
          return updatedMediaItem;
        }
        return { ...mediaItem, [name]: value }
      }else{
        return mediaItem
      }
    });
    setForm({ ...form, mediaItems: updatedMediaItems });
  };

  const handleDeleteMediaItem = (index) => {
    const updatedMediaItems = form.mediaItems.filter(
      (mediaItem) => mediaItem.index !== index
    );
    setForm({ ...form, mediaItems: updatedMediaItems });
  };

  // const handleMediaInputChange = (index, name, value) => {
  //   setMediaItems((prevMediaItems) => {
  //     const updatedMediaItems = [...prevMediaItems];
  //     updatedMediaItems[index] = { ...updatedMediaItems[index], [name]: value };
  //     return updatedMediaItems;
  //   });
  // };

  const handleClose = () => {
    setShow(false);
  };

  const handleShow = () => {
    setShow(true);
  };

  const callAfterPostCreation = () => {
    handleClose();
    setToaster({
      title: "Post!",
      type: "success",
      message: "Post created 🚀",
      show: true,
    });
    setForm({
      body: "",
      mediaItems: [],
    });
    refresh();
  };

  const uploadFileForMediaItem = async (filePath, file) => {
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("path", filePath);
      const uploadResponse = await axiosService.post("media/upload/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set the correct content type for file upload
        }
      });

      if (uploadResponse.status >= 200 && uploadResponse.status < 300) {
        return true; // File uploaded successfully
      } else {
        console.error("Failed to upload file:", uploadResponse);
        return false; // File upload failed
      }
    } catch (error) {
      // Handle network or other errors
      console.error("Error occurred during file upload:", error);
      return false;
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const createPostForm = event.currentTarget;
    if (createPostForm.checkValidity() === false) {
      event.stopPropagation();
      return;
    }
    setValidated(true);
    const data = {
      author: user.id,
      body: form.body,
      media_items: form.mediaItems,
    };
    axiosService
      .post("/post/", data)
      .then(async (response) => {
        // After the post is created, handle media item uploads
        if (response.status === 201) {
          const responseData = response.data;
          // Handle media item uploads after post creation
          const postMediaItems = responseData.post.media_items;
          const uploadPromises = postMediaItems.map((mediaItem) => {
            // Check if the media item exists in the form with a file
            const formMediaItem = data.media_items.find(
              (item) => mediaItem.meta.local_identifier === item.index
            );
            if (
              formMediaItem &&
              formMediaItem.file &&
              mediaItem.url &&
              mediaItem.url.file_path
            ) {
              return uploadFileForMediaItem(
                mediaItem.url.file_path,
                formMediaItem.file
              );
            }
            return Promise.resolve(false);
          });

          // Wait for all media item uploads to complete
          const uploadResults = await Promise.all(uploadPromises);

          // Check if any uploads failed
          const allUploadsSuccessful = uploadResults.every(
            (result) => result === true
          );

          if (allUploadsSuccessful) {
            console.log("All media items uploaded successfully");

            // Optionally, handle any further actions after the media items are uploaded
            // Call the callback function here
            callAfterPostCreation();
          } else {
            console.error("One or more media item uploads failed.");
            // Optionally, handle the error or display an error message
            setToaster({
              title: "Post!",
              type: "warning",
              message: `Media items upload failed`,
              show: true,
            });
          }
        } else {
          setToaster({
            title: "Post!",
            type: "warning",
            message: `An error occurred. ${response.status}`,
            show: true,
          });
        }

        // callAfterPostCreation();
      })
      .catch((err) => {
        setToaster({
          title: "Post!",
          type: "warning",
          message: `An error occurred. ${err.message}`,
          show: true,
        });
      });
  };
  return (
    <>
      <Form.Group className="my-3 w-75">
        <Form.Control
          className="py-2 rounded-pill border-primary text-primary"
          type="text"
          placeholder="Write a post..."
          onClick={handleShow}
        ></Form.Control>
      </Form.Group>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton className="border-0">
          <Modal.Title>Create Post</Modal.Title>
        </Modal.Header>
        <Modal.Body className="border-0">
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Control
                name="body"
                value={form.body}
                onChange={(e) => {
                  setForm({ ...form, body: e.target.value });
                }}
                as="textarea"
                rows={3}
              />
            </Form.Group>
            <h4>Media Items</h4>
            {form.mediaItems.map((mediaItem, index) => (
              <Card key={index} className="mb-3">
                <Card.Body>
                  <MediaItemInput
                    key={mediaItem.index}
                    mediaItem={mediaItem}
                    onChange={handleMediaItemChange}
                    onDelete={() => handleDeleteMediaItem(index)}
                  />
                </Card.Body>
              </Card>
            ))}
            <Button variant="primary" onClick={handleAddMediaItem}>
              <AddCircleOutlineIcon />
            </Button>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button
            variant="primary"
            onClick={handleSubmit}
            disabled={form.body === undefined}
          >
            Post
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default CreatePost;
