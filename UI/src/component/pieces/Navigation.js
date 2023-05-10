import React from "react"; 
import "@popperjs/core";
import { useNavigate } from 'react-router-dom';
import Button from "./Button";
import { useAuth } from "../../authentication/AuthContext";

function Navigation(){
    const navigate = useNavigate();
    const { setCurrentUser } = useAuth();

    function log_out(){
        setCurrentUser(null);
        localStorage.removeItem('currentUser');
        navigate('/Login');
    }

    return (
        <div className="navbartop">
        <nav class="navbar navbar-expand-lg navbar-dark bg" >
            <a class="navbar-brand" href="/">TradePlaza</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-target="#navbarTogglerDemo01">
                <span class="navbar-toggler-icon"></span>
            </button>
                <div class="collapse navbar-collapse" id="navbarTogglerDemo01">            
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/ListItem" >List Item</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/MyItem" >My Item</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/SearchItem" >Search</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/ARTrade" >Accept/Reject Trade</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/TradeHistory" >Trade History</a>
                    </li>
                    {/* <li class="nav-item">
                        <a class="nav-link" href="/" >Logout</a>
                    </li> */}
                    <Button name='Logout' onClick={log_out} />
                </ul>
                </div>
        </nav>
        </div>

    )
    }

export default Navigation;