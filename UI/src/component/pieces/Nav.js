import React, {useState, useEffect} from "react";
import trade from '../../image/trade.png'; 
import Navigation from './Navigation';

function Nav(props){
    return (
        
        <div>
            <Navigation />

            <div class="row row-welcome">
                <div class="col-lg-6">
                    <h1 class="title">Welcome <br></br>{props.fname} {props.lname} ({props.nickName})!</h1>
                </div>
                
                <div class="col-lg-6">
                    <img class="tradeimg" src={trade} alt="tradepng"></img>
                </div>
            </div>
        </div>
       
    )
}

export default Nav;