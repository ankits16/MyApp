import React from 'react'
import Navigationbar from './Navbar'

const Layout = (props) => {
  return (
    <div>
      <Navigationbar/>
      <div className='container m-5'>{props.children}</div>
    </div>
  )
}

export default Layout
