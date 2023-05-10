import React, { useRef, useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom'
import Button from "./pieces/Button";
import Footer from "./pieces/Footer";
import { useAuth } from "../authentication/AuthContext";
import { Alert } from "react-bootstrap";

function Register(){

    const navigate = useNavigate();
    const { setCurrentUser } = useAuth();
    const [loading, setLoading] = useState(true);

    const emailRef = useRef();
    const passwordRef = useRef();
    const nicknameRef = useRef();
    const firstnameRef = useRef();
    const lastnameRef = useRef();
    const postalcodeRef = useRef();
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        // setErrMsg('');
    });

    async function sign_up(event) {
        event.preventDefault();
        console.log("Registering---------1");
        try {
            setLoading(true);
            console.log("Registering---------2");
            // const response = await fetch('http://localhost:8000/TradePlaza/login/' + 'alwp@gmail.com');
            const response = await fetch('http://localhost:8000/TradePlaza/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({
                    'email': emailRef.current.value,
                    'nickname': nicknameRef.current.value,
                    'first_name': firstnameRef.current.value,
                    'last_name': lastnameRef.current.value,
                    'password': passwordRef.current.value,
                    'postal_code': postalcodeRef.current.value
                })
            });
            console.log("Registering---------3");
            const data = await response.json();
            console.log(data.data);
            if (data.data) {
                if (data.data === 'completed.') {
                    const user = { 
                        'email': emailRef.current.value,
                        'nickname': nicknameRef.current.value,
                    };
                    setCurrentUser(user);
                    localStorage.setItem('currentUser', JSON.stringify(user));
                    emailRef.current.value = '';
                    nicknameRef.current.value = '';
                    passwordRef.current.value = '';
                    firstnameRef.current.value = '';
                    lastnameRef.current.value = '';
                    postalcodeRef.current.value = '';
                    console.log("Register successfully!");
                    navigate("/");
                } else if (data.data === 'User email already exists.'){
                    setErrMsg('Register failed! User email already exists!');
                } else if (data.data === 'User nickname already exists.'){
                    setErrMsg('Register failed! User nickname already exists!');
                } else if (data.data === 'Invalid postal code.'){
                    setErrMsg('Register failed! Invalid postal code!');
                } else {
                    setErrMsg('Register failed!');
                }
            } else {
                setErrMsg('Register failed!');
            }
        } catch {
            setErrMsg('Register failed!');
        }
        setLoading(false);
    }

    return (
        <div class ="backcolor">
            <div className="navbartop">
                <nav class="navbar navbar-expand-lg navbar-dark bg" >
                    <a class="navbar-brand">TradePlaza</a>
                </nav>
            </div>
            <form onSubmit={sign_up}>
                <div className="rgstr_form">
                    <h2>Registration</h2>
                    <label htmlFor='email'>Email</label> <br />
                    <input type='email' id='rgstr_email' name='email' ref={emailRef} required/><br />
                    <label htmlFor='password'>Password</label> <br />
                    <input type='password' id='rgstr_password' name='password' ref={passwordRef} required /> <br />
                    <label htmlFor='Nickname'>Nickname</label> <br />
                    <input type='text' id='rgstr_nickname' name='nickname' ref={nicknameRef} required /> <br />
                    <label htmlFor='firstname'>First Name</label> <br />
                    <input type='text' id='rgstr_firstname' name='firstname' ref={firstnameRef} required /> <br />
                    <label htmlFor='lastname'>Last Name</label> <br />
                    <input type='text' id='rgstr_lastname' name='lastname' ref={lastnameRef} required /> <br />
                    <label htmlFor='postalcode'>Postcal Code</label> <br />
                    <input type='text' id='rgstr_postcode' name='postal_code' ref={postalcodeRef} required /> <br />
                    <p className='errorMes' > {errMsg && <Alert variant='danger'> {errMsg}</Alert>} </p>
                    <Button type= "submit" name="Register" /><br />
                </div>
            </form>
            <Footer />
        </div>
        )
        
}

export default Register;