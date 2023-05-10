import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {useState, useEffect} from "react";
import { data } from 'jquery';
import Button from "./Button";
import {useNavigate, Link} from 'react-router-dom';
import { useAuth } from "../../authentication/AuthContext";


// const itemNumber = 28; //itemNumber = 18 owned by augr@gmail.com


export default function TableViewItem(props) {

    const { currentUser } = useAuth();
    console.log(currentUser);

    const [item, setItem] = React.useState({});
    const navigate = useNavigate();
    function proposeTrade(){
        navigate("/ProposeTrade")
    }
    const getItem = async() =>{
        const response = await fetch('http://localhost:8000/tradeplaza/display_item_details/?email='+ currentUser.email + '&itemNumber=' + props.itemNumber);
        const data = await response.json();
        console.log(data.data);
        setItem(data.data); 
        
        //return item;
    }
    useEffect(() => {
        getItem();
    }, {});

    let style;
    if(0<item.distance && item.distance<25) {
        style = {backgroundColor: "green"}
    }
    if(25<=item.distance && item.distance< 50) {
        style = {backgroundColor: "yellow"}
    }
    if(50<=item.distance && item.distance<100) {
        style = {backgroundColor: "orange"}
    }
    if(item.distance >= 100) {
        style = {backgroundColor: "red"}
    }

    let Timestyle;
    if(item.response_time==='None'){
        Timestyle = {color: "black"}
    } else if (item.response_time>=0 && item.response_time<7.1){
        Timestyle = {color: "green"}
    } else if (item.response_time>=7.1 && item.response_time<=14.0){
        Timestyle = {color: "yellow"}
    } else if (item.response_time>14.0 && item.response_time<=20.9){
        Timestyle = {color: "orange"}
    } else if (item.response_time>=21.0 && item.response_time<=27.9){
        Timestyle = {color: "red"}
    } else {
        Timestyle = {color: 'red', fontWeight: 'bold'}
    }
    
    return(
        <div>
        <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
            <TableRow>           
                    <TableCell align="left">Item #</TableCell>
                    <TableCell align="left">Title</TableCell>
                    <TableCell align="left">Game type</TableCell>
                    {(item.game_type==='CollectiveCardGame') && <TableCell align="left">Card #</TableCell>}
                    {(item.game_type === 'VideoGame' || item.game_type === 'ComputerGame') && <TableCell align="left">Platform</TableCell>}
                    {(item.game_type === 'VideoGame') && <TableCell align="left">Media</TableCell>}
                    <TableCell align="left">Condition</TableCell>
                    {(item.description !== null && item.description !== '' && item.description !== '\r') && <TableCell align="left">Description </TableCell>}
                    {(item.fk_email!==currentUser.email) && <TableCell align="left">Offered By</TableCell>}
                    {(item.fk_email!==currentUser.email) &&<TableCell align="left">Location</TableCell>}
                    {(item.fk_email!==currentUser.email) &&<TableCell align="left">Response time (days)</TableCell>}
                    {(item.fk_email!==currentUser.email) &&<TableCell align="left">Rank</TableCell>}
                    {(item.fk_email!==currentUser.email) && (item.distance !== 0) &&<TableCell align="left">Distance (miles)</TableCell>}
            </TableRow>
        </TableHead>
        <TableBody>
            {
            <TableRow>
            <TableCell component="th" scope="row">
                {item.itemNumber}
            </TableCell>
                <TableCell align="left">{item.title}</TableCell>
                <TableCell align="left">{item.game_type}</TableCell>
                {(item.game_type==='CollectiveCardGame') &&<TableCell align="left">{item.cardsOffered}</TableCell>}
                {(item.game_type === 'VideoGame' || item.game_type === 'ComputerGame') && <TableCell align="left">{item.platform}</TableCell> }                    
                {(item.game_type === 'VideoGame') &&<TableCell align="left">{item.media}</TableCell>}
                <TableCell align="left">{item.condition}</TableCell>
                {(item.description !== null && item.description !== '' && item.description !== '\r') && <TableCell align="left">{item.description} </TableCell>}
                {(item.fk_email!==currentUser.email) &&<TableCell align="left">{item.nickname}</TableCell>}
                {(item.fk_email!==currentUser.email) &&<TableCell align="left">{item.city}, {item.state} {item.postal_code}</TableCell>}
                {(item.fk_email!==currentUser.email) &&<TableCell sx={Timestyle} align="left">{item.response_time}</TableCell>}
                {(item.fk_email!==currentUser.email) &&<TableCell align="left">{item.rank}</TableCell>}
                {(item.fk_email!==currentUser.email) && (item.distance !== 0) &&<TableCell sx={style} align="left">{item.distance} </TableCell>}
            </TableRow>
            }
        </TableBody>
        </Table>
    </TableContainer>

    {(item.fk_email!==currentUser.email) && (item.isTradable ==='true') && (item.pendingItemNum < 2) &&<Link to={"/ProposeTrade"} state = {{'itemNumber': item.itemNumber, 'title': item.title, 'distance': item.distance}}><Button name ="Propose Trade" onClick ={proposeTrade}/></Link>}
    </div>
    )
}