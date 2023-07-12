import React, { useContext, useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import {getUser} from "../../hooks/user.actions";
import axiosService from "../../helpers/axios";
import Toaster from "../Toaster";
import { Context } from "../Layout";

const CreatePost = (props) => {
  const {refresh} = props;
  const {setToaster} = useContext(Context);
  const [show, setShow] = useState(false);
  const [form, setForm] = useState({});
  const [validated, setValidated] = useState(false);
  // const [showToast, setShowToast] = useState(false);
  // const [toastMessage, setToastMessage] = useState("");
  // const [toastType, setToastType] = useState("");
  const user = getUser();

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
    };

    axiosService
      .post("/post/", data)
      .then(() => {
        handleClose();
        setToaster({
          title: "Post!",
          type: "success",
          message: "Post created 🚀",
          show: true
        })
        // setToastMessage("Post created 🚀");
        // setToastType("success");
        // setShowToast(true);
        setForm({});
        refresh()
      })
      .catch((err) => {
        setToaster({
          title: "Post!",
          type: "warning",
          message: `An error occurred. ${err.message}`,
          show: true
        })
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
        <Modal.Body className="borde-0">
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
              <Form.Control
                name="body"
                value={form.body}
                onChange={(e) => {
                  setForm({ ...e, body: e.target.value });
                }}
                as="textarea"
                rows={3}
              />
            </Form.Group>
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
