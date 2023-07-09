import React from 'react'
import RegistrationForm from '../components/authentication/RegistrationForm'
import { Link } from 'react-router-dom'

export default function Registration() {
    console.log('Registration')
  return (
    <div className='container'>
        <div className='row'>
            <div className='col-md-6 d-flex align-items-center'>
                <div className='content text-center px-4'>
                    <h1 className='text-primary'>
                        Welcome to TBD
                    </h1>
                    <p className='content'>
                        This a TBD app <br/>
                        This will  do is TBD<br/>
                        experience is TBD<br/>
                        what it tries to solve is TBD.<br/>
                        <Link to="/login/">login</Link>.
                    </p>
                </div>
            </div>
            <div className='col-md-6 p-5'>
                <RegistrationForm/>
            </div>
        </div>
      
    </div>
  )
}
