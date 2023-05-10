import React from "react";
import { useNavigate } from 'react-router-dom';
import Button from "./pieces/Button";
import Footer from "./pieces/Footer";
import { useRef, useState, useEffect } from "react";
import { Alert } from "react-bootstrap";
import { useAuth } from "../authentication/AuthContext";

function Login(){
    const navigate = useNavigate();

    const { setCurrentUser } = useAuth();
    const [loading, setLoading] = useState(true);

    const usernameRef = useRef();
    const passwordRef = useRef();
    const [errMsg, setErrMsg] = useState('');
    
    useEffect(() => {
        // setErrMsg('');
    });

    async function authenticate(event) {
        event.preventDefault();
        try {
            // setLoading(true);
            const response = await fetch('http://localhost:8000/TradePlaza/login/' + usernameRef.current.value);
            const data = await response.json();
            console.log(data.data)
            if (data && data.data.length !== 0) {
                const emailReturn = data.data[0].email;
                const nicknameReturn = data.data[0].nickname;
                const passwordReturn = data.data[0].password;
                const user = { 
                    'email': emailReturn,
                    'nickname': nicknameReturn,
                };
                if (passwordReturn === passwordRef.current.value) {
                    setCurrentUser(user);
                    localStorage.setItem('currentUser', JSON.stringify(user));
                    usernameRef.current.value = '';
                    passwordRef.current.value = '';
                    console.log('Login successfully!');
                    navigate('/');
                } else {
                    setErrMsg('Login failed! Password does not match!');
                }
            } else {
                setErrMsg('Login failed! Username does not exist!');
            }
        } catch (err) {
            setErrMsg('Login failed!');
        }
        // setLoading(false);
    }

    function goRegister(){
        navigate('/Register');
    }
    
    return (
        <div class ='backcolor'>
            <div className='navbartop'>
                <nav class='navbar navbar-expand-lg navbar-dark bg' >
                    <a class='navbar-brand'>TradePlaza</a>
                </nav>
            </div>
           
            <h2>Sign In</h2>
            <form onSubmit={authenticate}>
                <label htmlFor  = 'email'>Email/nickname</label> <br/>
                <input type = 'text' id = 'email' name='email' ref={usernameRef} required/><br/>
                <label htmlFor  = 'password'>Password</label> <br/>
                <input type = 'password' id = 'password' name='password' ref={passwordRef} required/> <br/>
                <p className='errorMes' > {errMsg && <Alert variant='danger'> {errMsg}</Alert>} </p>
                <Button type= "submit" name="Login" /><br />
            </form>
            <br></br>

            <h3>New User</h3>
            {/* <form> */}
                <Button name='Register' onClick={goRegister} />
                <br/>
            {/* </form> */}
            <Footer />
        </div>
    )
}


export default Login;