import React, { useState } from "react";
import { Card, Dropdown, Image } from "react-bootstrap";
import { randomAvatar } from "../../utils";
import { format } from "timeago.js";
import { CommentOutlined, LikeFilled, MoreOutlined } from "@ant-design/icons";
import axiosService from "../../helpers/axios";
import Toaster from "../Toaster";
import { getUser } from "../../hooks/user.actions";
import { Link } from "react-router-dom";
import UpdatePost from "./UpdatePost";
import ReactLinkify from "react-linkify";
import MoreToggleIcon from "../menu/MoreToggleIcon";
const Post = (props) => {
  const { post, refresh, isSinglePost } = props;
  const [showToast, setShowToast] = useState(false);
  // const handleLikeClick = (acion) => {};
  const user = getUser();

  const handleDelete = () => {
    axiosService
      .delete(`/post/${post.id}/`)
      .then(() => {
        setShowToast(true); //
        refresh(); //
      })
      .catch((error) => console.log(error.message));
  };

  function openLinkInNewTab(href, text, key) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" key={key}>
        {text}
      </a>
    );
  }

  return (
    <>
      <Card className="rounded-3 my-4">
        <Card.Title className="d-flex flex-row justify-content-between">
          <div className="d-flex flex-row">
            <Image
              src={randomAvatar()}
              roundedCircle
              width={48}
              height={48}
              className="me-2 border border-primary border-2"
            />
            <div className="d-flex flex-column justify-content-start align-self-center mt-2">
              <p className="fs-6 m-0">{post.author.name}</p>
              <p className="fs-6 fw-lighter">
                <small>{format(post.created)}</small>
              </p>
            </div>
          </div>
          {user.id === post.author.id && (
            <div>
              <Dropdown>
                <Dropdown.Toggle as={MoreToggleIcon} />
                <Dropdown.Menu>
                  {/* <Dropdown.Item>Update</Dropdown.Item> */}
                  <UpdatePost post={post} refresh={refresh} />
                  <Dropdown.Item className="text-danger" onClick={handleDelete}>
                    Delete
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </div>
          )}
        </Card.Title>
        <Card.Text>
          <ReactLinkify componentDecorator={openLinkInNewTab}>
            {post.body}
          </ReactLinkify>
        </Card.Text>
        <div className="d-flex flex-row justify-content-between">
          <div className="d-flex flex-row">
            <LikeFilled
              style={{
                color: "#fff",
                backgroundColor: "#0D6EFD",
                borderRadius: "50%",
                width: "18px",
                height: "18px",
                fontSize: "75%",
                padding: "2px",
                margin: "3px",
              }}
            />
            <p className="ms-1 fs-6">
              <small>{post.likes_count} like</small>
            </p>
          </div>
          {!isSinglePost && (
            <p className="ms-1 fs-6">
              <small>
                <Link to={`/post/${post.id}/`}>
                  {post.comments_count} comments
                </Link>
              </small>
            </p>
          )}
        </div>
        <Card.Footer
          className="d-flex bg-white w-50
         justify-content-between border-0"
        >
          <div className="d-flex flex-row">
            <LikeFilled
              style={{
                color: "white",
                backgroundColor: "#0D6EFD",
                borderRadius: "50%",
                width: "18px",
                height: "18px",
                fontSize: "75%",
                padding: "2px",
                margin: "3px",
              }}
            />
            <p className="ms-1 fs-6">
              <small>{post.like_count} like</small>
            </p>
          </div>
          {!isSinglePost && (
            <div className="d-flex flex-row">
              <CommentOutlined
                style={{
                  width: "24px",
                  height: "24px",
                  padding: "2px",
                  fontSize: "20px",
                  color: "#C4C4C4",
                }}
              />
              <p className="ms-1 mb-0">
                <small>Comment</small>
              </p>
            </div>
          )}
        </Card.Footer>
      </Card>
      <Toaster
        showToast={showToast}
        title="Post !"
        message="Delete!"
        type="danger"
        onClose={() => setShowToast(false)}
      />
    </>
  );
};

export default Post;
