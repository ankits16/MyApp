import React from 'react'
import ParentComponent from './TestComponents'
import Layout from '../components/Layout'

export default function Home() {
  console.log('Home');
  return (
    <Layout>
      <h1>Profile</h1>
        <p>Welcome Home !</p>
        <ParentComponent/>
    </Layout>
  )
}
