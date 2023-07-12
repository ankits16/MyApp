import React, { useContext, useState } from "react";
import { Button, Form, Image } from "react-bootstrap";
import { randomAvatar } from "../../utils";
import { Context } from "../../components/Layout";
import { getUser } from "../../hooks/user.actions";
import axiosService from "../../helpers/axios";

const CreateComment = (props) => {
  const { postId, refresh } = props;
  const [avatar, setAvatar] = useState(randomAvatar());
  const [validated, setValidated] = useState(false);
  const [form, setForm] = useState({});
  const {setToaster } = useContext(Context);
  const user = getUser();
  const handleSubmit = (event) => {
    event.preventDefault();
    const createCommentForm = event.currentTarget;
    if (createCommentForm.checkValidity() === false) {
      event.stopPropagation();
      return;
    }
    const data = {
      author: user.id,
      body: form.body,
      post: postId,
    };

    axiosService
      .post(`/post/${postId}/comment/`, data)
      .then(() => {
        // console.log(`toaster is ${toaster}`)
        setForm({ ...form, body: "" });
        setToaster({
          type: "success",
          message: "Comment posted successfully🚀",
          show: true,
          title: "Comment!",
        });
        refresh();
      })
      .catch((error) => {
        setToaster({
            type: "danger",
            message: `Comment poste failed. ${error.message}`,
            show: true,
            title: "Comment!",
          });
      });
  };
  return (
    <Form
      className="d-flex flex-row  justify-content-between"
      noValidate
      validated={validated}
      onSubmit={handleSubmit}
    >
      <Image
        src={avatar}
        roundedCircle
        width={48}
        height={48}
        className="my-2"
      />
      <Form.Group>
        <Form.Control
          className="py-2 rounded-pill border-primary"
          type="text"
          placeholder="Write a comment.."
          value={form.body}
          name="body"
          onChange={(e) => setForm({ ...form, body: e.target.value })}
        />
      </Form.Group>
      <div className="m-auto">
        <Button
          variant="primary"
          onClick={handleSubmit}
          disabled={form.body === undefined}
          size="small"
        >
          Comment
        </Button>
      </div>
    </Form>
  );
};

export default CreateComment;
