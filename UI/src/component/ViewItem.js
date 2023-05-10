import TableViewItem from "./pieces/TableViewItem";
import Navigation from "./pieces/Navigation";
import Footer from "./pieces/Footer";
import {useNavigate, useLocation } from 'react-router-dom'
import React, { Component }  from 'react';


function ViewItem(){
    const location = useLocation();
    
    let id = location.state.itemNumber
    console.log(location.state.itemNumber)
    return(
        <div>
            <Navigation />  
            <div className="table">         
            <TableViewItem itemNumber={id}/>

            {/* <Button name ="Propose Trade" onClick ={proposeTrade}/> */}

            </div>
            
            <Footer />
        </div>
    );

}
export default ViewItem;
