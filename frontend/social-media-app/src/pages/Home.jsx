import React from "react";
import ParentComponent from "./TestComponents";
import Layout from "../components/Layout";
import { Col, Image, Row } from "react-bootstrap";
import { randomAvatar } from "../utils";
import CreatePost from "../components/posts/CreatePost";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import Post from "../components/posts/Post";

export default function Home() {
  const posts = useSWR("/post/", fetcher, { refreshInerval: 1000 });
  return (
    <Layout>
      <Row className="justify-content-evenly">
        <Col sm={7}>
          <Row className="border rounded align-items-center">
            <Col className="flex-shrink-1">
              <Image
                src={randomAvatar()}
                roundedCircle
                width={52}
                height={52}
                className="my-2"
              />
            </Col>
            <Col sm={10} className="flex-grow-1">
              <CreatePost />
            </Col>
          </Row>
          <Row className="my-4">
            {posts.data?.results.map((post, index) => {
              // <div>{post.body}</div>;
              return <Post key={index} post={post} refresh={posts.mutate}/>
            })}
          </Row>
        </Col>
      </Row>
      <h1>Profile</h1>
      <p>Welcome Home !</p>
      <ParentComponent />
    </Layout>
  );
}
