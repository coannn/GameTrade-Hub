import React from "react";

function Button(props) {
    return (
        <div>
           { !props.disabled ? 
            <button type={props.type} class="btn btn-outline-dark btn-lg usebtn" onClick ={props.onClick} >{props.name}</button>: 
            <button type={props.type} class="btn btn-outline-dark btn-lg usebtn disabled" onClick ={props.onClick} >{props.name}</button>
           }
        </div>
    )

}

export default Button;