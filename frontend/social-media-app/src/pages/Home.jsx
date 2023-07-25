import React from "react";
// import ParentComponent from "./TestComponents";
import Layout from "../components/Layout";
import { Col, Image, Row } from "react-bootstrap";
import { randomAvatar } from "../utils";
import CreatePost from "../components/posts/CreatePost";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import Post from "../components/posts/Post";
import ProfileCard from "../components/profile/ProfileCard";

export default function Home() {
  const posts = useSWR("/post/", fetcher, { refreshInerval: 1000 });
  const profiles = useSWR("/user/?limit=5", fetcher);
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
            <Col sm={20} className="flex-grow-1">
              <CreatePost refresh={posts.mutate}/>
            </Col>
          </Row>
          <Row className="my-4">
            {posts.data?.results.map((post, index) => {
              // <div>{post.body}</div>;
              return <Post key={index} post={post} refresh={posts.mutate} isSinglePost={false}/>
            })}
          </Row>
        </Col>
        <Col sm={3} className="border rounded py-4
           h-50">
         <h4 className="font-weight-bold text-center">
           Suggested people</h4>
         <div className="d-flex flex-column">
           {profiles.data &&
             profiles.data.results.map((profile,
                                        index) => (
               <ProfileCard key={index} user={profile}
               />
             ))}
         </div>
         </Col>
      </Row>
      <h1>Profile</h1>
      <p>Welcome Home !</p>
      {/* <ParentComponent /> */}
    </Layout>
  );
}
