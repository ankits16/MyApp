import React from 'react'
import userSWR from "swr";
import Layout from '../components/Layout'
import { useParams } from 'react-router-dom'
import { fetcher } from '../helpers/axios';
import { Col, Row } from 'react-bootstrap';
import Post from '../components/posts/Post';
import CreateComment from '../components/comments/CreateComment';
import Comment from '../components/comments/Comment';

const PostDetail = () => {
    console.log(useParams())
    let {postId} = useParams();
    const post = userSWR(`/post/${postId}/`, fetcher)
    const comments = userSWR(`/post/${postId}/comment/`, fetcher)
  return (
    <Layout hasNavigationBack = {true}>
        {post.data ? (
            <Row className='justify-content-center '>
                <Col sm={8}>
                <Post post={post.data} refresh={post.mutate} isSinglePost={true}/>
                <CreateComment postId={postId} refresh={comments.mutate}/>
                {comments.data &&
              comments.data.results.map((comment, index) => (
                // <div>Comment</div>
                <Comment
                  key={index}
                  postId={post.data.id}
                  comment={comment}
                  refresh={comments.mutate}
                />
              ))}
                </Col>
            </Row>
        ) 
        : 
        (
            <div>Loading...</div>
        )}

    </Layout>
  )
}

export default PostDetail
