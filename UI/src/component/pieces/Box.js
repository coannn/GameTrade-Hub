import React, {useState} from "react"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBell, faClock, faRankingStar} from '@fortawesome/free-solid-svg-icons'

function Box(props){

    let trade; 
    if (props.unacceptedTrades >0){
        trade = <a class ="boxItem" style={ (props.unacceptedTrades>=2) ? {color: "red", fontWeight: 'bold'} : null } href ={ (props.unacceptedTrades>=1) && '/ARTrade'}>{props.unacceptedTrades}</a>
    } else {
        trade = <p class ="boxItem" >{props.unacceptedTrades}</p>
    }

    let time;
    if(props.responseTime==='None'){
        time = <p class ="boxItem" style={{color: "black"}}>{props.responseTime}</p>
    } else if (props.responseTime>=0 && props.responseTime<7.1){
        time = <p class ="boxItem" style={{color: "green"}}>{props.responseTime} days</p>
    } else if (props.responseTime>=7.1 && props.responseTime<=14.0){
        time = <p class ="boxItem" style={{color: "yellow"}}>{props.responseTime} days</p>
    } else if (props.responseTime>14.0 && props.responseTime<=20.9){
        time = <p class ="boxItem" style={{color: "orange"}}>{props.responseTime} days</p>
    } else if (props.responseTime>=21.0 && props.responseTime<=27.9){
        time = <p class ="boxItem" style={{color: "red"}}>{props.responseTime} days</p>
    } else {
        time = <p class ="boxItem" style={{color: "red", fontWeight: "bold"}}>{props.responseTime} days</p>
    }

    
    
    return (
        <section class="container">
            <div class="row">
                <div class="col p-3">
                    <div class="custom-card-gray"><FontAwesomeIcon className ="icon" icon={faBell} />
                        <h4>Unaccepted Trades</h4>
                        {trade}
                    </div>
                </div>
                <div class="col p-3">
                    <div class="custom-card-gray"><FontAwesomeIcon className ="icon" icon={faClock} />
                        <h4>Response Time</h4>
                        {time}
                    </div>
                </div>
                <div class="col p-3">
                    <div class="custom-card-gray"><FontAwesomeIcon className="icon" icon={faRankingStar} />
                        <h4>My Rank</h4>
                        <p class ="boxItem">{props.myRank}</p>
                    </div>
                </div>
            </div>
        </section>   
    )
}

export default Box;