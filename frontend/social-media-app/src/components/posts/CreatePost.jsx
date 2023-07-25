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
    const updatedMediaItems = form.mediaItems.map((mediaItem) =>{
      if (name === 'media-item-notes'){
        var updatedMeta = {...mediaItem.meta}
        updatedMeta['notes'] = value;
        var updatedMediaItem = {...mediaItem}
        updatedMediaItem.meta = updatedMeta
        return updatedMediaItem;
      }
      return mediaItem.index === index ? { ...mediaItem, [name]: value } : mediaItem
    }
      
    );
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
      media_items: form.mediaItems
    };
    axiosService
      .post("/post/", data)
      .then(() => {
        handleClose();
        setToaster({
          title: "Post!",
          type: "success",
          message: "Post created 🚀",
          show: true,
        });
        // setToastMessage("Post created 🚀");
        // setToastType("success");
        // setShowToast(true);
        setForm({
          body: "",
        mediaItems: [],});
        refresh();
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
