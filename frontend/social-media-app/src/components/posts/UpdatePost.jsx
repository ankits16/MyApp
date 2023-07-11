import React, { useState } from "react";
import { Dropdown, Form, Modal, Button } from "react-bootstrap";
import Toaster from "../Toaster";
import axiosService from "../../helpers/axios";

const UpdatePost = (props) => {
    const {post, refresh} = props;
    const [error, setError] = useState(null);
    const [form, setForm] = useState({
        body: post.body,
        author: post.author.id
    });
  const [show, setShow] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [validated, setValidated] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleSubmit = (event) =>{
    event.preventDefault();
    const updateForm = event.currentTarget;

    if(updateForm.checkValidity() === false){
        event.stopPropagation()
        return
    }
    setValidated(true);
    const data ={
        body: form.body,
        author: form.author
    }
    axiosService.put(`/post/${post.id}/`, data)
    .then(() =>{
        handleClose();
        setShowToast(true);
        refresh();
    })
    .catch(error =>{
        setError(`Post update Failed : ${error.message}`)
        setShowToast(true);
    });
  }

  return( <>
  <Dropdown.Item onClick={handleShow}>Modify</Dropdown.Item>
  <Modal show={show} onHide={handleClose}>
    <Modal.Header closeButton className="border-0">
        <Modal.Title>Update Post</Modal.Title>
    </Modal.Header>
    <Modal.Body className="border-0">
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
                <Form.Control
                name="body"
                value={form.body}
                onChange={(e)=> setForm({...form, body: e.target.value})}
                as='textarea'
                rows={3}
                />
            </Form.Group>
        </Form>
    </Modal.Body>
    <Modal.Footer>
        <Button variant='primary' onClick={handleSubmit}>Update</Button>
    </Modal.Footer>
  </Modal>
  <Toaster
  title='Success!!'
  message={error ? error : 'Post updated successfully'}
  type= {error ? 'danger': 'success'}
  showToast = {showToast}
  onClose = {()=>{setShowToast(false)}}
  />
  </>);
};

export default UpdatePost;
