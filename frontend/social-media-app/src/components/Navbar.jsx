import React from 'react'
import { Container, Navbar, Nav, NavDropdown, Image } from 'react-bootstrap'
import { randomAvatar } from "../utils";
import { useUserActions } from '../hooks/user.actions';

const Navigationbar = () => {
    const userActions = useUserActions()
  return (
    <Navbar bg='primary' variant='dark'>
        <Container>
            <Navbar.Brand className='fw-bold' href='#home'>TDB App</Navbar.Brand>
            <Navbar.Collapse className='justify-content-end'>
                <Nav>
                    <NavDropdown
                    title ={
                        <Image 
                        src = {randomAvatar}
                        roundedCircle
                        width={36}
                        height={36}
                        />
                    }
                    >
                        <NavDropdown.Item href="#">Profile</NavDropdown.Item>
                        <NavDropdown.Item onClick={userActions.logout} >Logout</NavDropdown.Item>
                    </NavDropdown>
                </Nav>
            </Navbar.Collapse>
        </Container>

    </Navbar>
  )
}

export default Navigationbar
