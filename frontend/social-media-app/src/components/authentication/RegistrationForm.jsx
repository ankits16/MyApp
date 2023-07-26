import axios from 'axios';
import React, { useState } from "react";
import { Button, Form } from "react-bootstrap"
import { useNavigate } from "react-router-dom";
import { BASE_URL_API } from "../../helpers/axios";

export default function RegistrationForm() {
    const navigate = useNavigate();
    const [validated, setValidated] = useState(false);
    const [form, setForm] = useState({});
    const [error, setError] = useState(null);

    const handleSubmit = (event) => {
        event.preventDefault();
        const registrationForm = event.currentTarget;

        if (registrationForm.checkValidity() === false){
            event.stopPropagation();
        }
        setValidated(true);
        const data = {
            username: form.username,
            password: form.password,
            email: form.email,
            first_name: form.first_name,
            last_name: form.last_name,
            bio: form.bio,
        }
        axios.post(`${BASE_URL_API}/auth/register/`, data)
        .then((response) => {
            localStorage.setItem("auth", JSON.stringify({
                accessToken: response.data.access,
                refresh: response.data.refresh,
                user: response.data.user
            }));
            navigate('/')
        })
        .catch((error)=>{
            if (error.message){
                setError(error.request.response)
            }
        })
    };
  return <div>
    <Form
    id='registration-form'
    className="border p-4 rounded"
    noValidate
    validated={validated}
    onSubmit={handleSubmit}
    >
        {/* First Name */}
        <Form.Group className="mb-3">
            <Form.Label>First Name</Form.Label>
            <Form.Control 
            value={form.first_name}
            onChange={(e) => setForm({...form, first_name: e.target.value})}
            required
            type = "text"
            placeholder="Enter first name"
            />
            <Form.Control.Feedback type="invalid">
                First Name is required
            </Form.Control.Feedback>
        </Form.Group>
        {/* Last Name */}
        <Form.Group className="mb-3">
            <Form.Label>Last Name</Form.Label>
            <Form.Control 
            value={form.last_name}
            onChange={(e) => setForm({...form, last_name: e.target.value})}
            required
            type = "text"
            placeholder="Enter last name"
            />
            <Form.Control.Feedback type="invalid">
                Last Name is required
            </Form.Control.Feedback>
        </Form.Group>
        {/* user name */}
        <Form.Group className="mb-3">
            <Form.Label>Username</Form.Label>
            <Form.Control 
            value={form.username}
            onChange={(e) => setForm({...form, username: e.target.value})}
            required
            type = "text"
            placeholder="Enter username"
            />
            <Form.Control.Feedback type="invalid">
                Username is required
            </Form.Control.Feedback>
        </Form.Group>
        {/* email */}
        <Form.Group className="mb-3">
            <Form.Label>Email address</Form.Label>
            <Form.Control 
            value={form.email}
            onChange={(e) => setForm({...form, email: e.target.value})}
            required
            type = "email"
            placeholder="Enter username"
            />
            <Form.Control.Feedback type="invalid">
                Email is required
            </Form.Control.Feedback>
        </Form.Group>
        {/* password */}
        <Form.Group className="mb-3">
            <Form.Label>Password</Form.Label>
            <Form.Control 
            value={form.password}
            onChange={(e) => setForm({...form, password: e.target.value})}
            required
            type = "password"
            placeholder="Enter username"
            />
            <Form.Control.Feedback type="invalid">
                Password is required
            </Form.Control.Feedback>
        </Form.Group>
        {/* bio */}
        <Form.Group className="mb-3">
            <Form.Label>Bio</Form.Label>
            <Form.Control 
            value={form.bio}
            onChange={(e) => setForm({...form, bio: e.target.value})}
            as = "textarea"
            rows={3}
            placeholder="User Bio... (Optional)"
            />
        </Form.Group>
        <div className="text-content text-danger">
            {error &&  <p>{error}</p>}
        </div>
        <Button variant="primary" type="submit">Register</Button>
    </Form>
  </div>;
}
