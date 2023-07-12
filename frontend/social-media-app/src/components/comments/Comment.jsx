import React, { useContext } from "react";
import { Context } from "../Layout";
import { getUser } from "../../hooks/user.actions";
import { Card, Dropdown, Image } from "react-bootstrap";
import { randomAvatar } from "../../utils";
import { format } from "timeago.js";
import MoreToggleIcon from "../menu/MoreToggleIcon";
import axiosService from "../../helpers/axios";

const Comment = (props) => {
  const { postId, comment, refresh } = props;
  const { toaster, setToaster } = useContext(Context);
  const user = getUser();
  const handleDelete = () => {
    axiosService.delete(`/post/${postId}/comment/${comment.id}`)
    .then((response) =>{
        setToaster({
            type: 'danger',
            message: `Comment deleted.`,
            show: true,
            title: 'Delete comment'
        })
        refresh();
    })
    .catch((error) => {
        setToaster({
            type: 'warning',
            message: `Delete comment failed: ${error.message}`,
            show: true,
            title: 'Delete comment'
        })
    })
    ;
  };
  return (
    <Card className="rounded-3 my-2">
      <Card.Body>
        <Card.Title className="d-flex flex-row justify-content-center">
          <div className="d-flex flex-row">
            <Image
              src={randomAvatar()}
              roundedCircle
              width={48}
              height={48}
              className="me-2 border border-primary border-2"
            />
            <div className="d-flex flex-column justify-content-start align-self-center mt-2">
              <p className="fs-6 m-0">{comment.author.name}</p>
              <p className="fs-6 fw-lighter">
                <small>{format(comment.created)}</small>
              </p>
            </div>
          </div>
          {user.username === comment.author.username && (
            <div>
              <Dropdown>
                <Dropdown.Toggle as={MoreToggleIcon}></Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item>Modify</Dropdown.Item>
                  <Dropdown.Item onClick={handleDelete} className="text-danger">
                    Delete
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </div>
          )}
        </Card.Title>
        <Card.Text>{comment.body}</Card.Text>
      </Card.Body>
    </Card>
  );
};

export default Comment;
