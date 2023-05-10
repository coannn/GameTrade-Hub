import Footer from './pieces/Footer'
import Navigation from "./pieces/Navigation";
import Button from "./pieces/Button";
import {useNavigate} from 'react-router-dom'
import React, {useState, useEffect} from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import {Link} from 'react-router-dom';
import { useAuth } from "../authentication/AuthContext";

function ARTrade(){

    const navigate = useNavigate();

    const { currentUser } = useAuth();
    console.log(currentUser);

    //confirmation popup go back to main menu
    const[noitem_popup_state, set_noitem_popup_state] = useState(false);
    const[accept_popup_state, set_accept_popup_state] = useState(false);
    //const[acceptFail_popup_state, set_acceptFail_popup_state] = useState(false);
    const[reject_popup_state, set_reject_popup_state] = useState(false);
    const[Fail_popup_state, set_Fail_popup_state] = useState(false);


    //const
   
    const [myItemList, setList] = useState([]);
    const [fetch_success, setfetch_success]= useState(false);
    const [proposername, setproposername]= useState(null);
    const [proposeremail, setproposeremail]= useState(null);

    
    // fetch get to collect for get data
    const getList = async () => {
        const response = await fetch('http://localhost:8000/TradePlaza/artrade/getMyTradeList/' + currentUser.email);
        //console.log(response);
        const data = await response.json();
        setList(data); // probably a safer way to do this, but if you console.log(data) you'll see an object is being returned, not an array.  
        //console.log(myItemList);
        return myItemList;
    };

    //console.log(myItemList);
    
   
    // function for comfirm button, fetch post if click
    function artrade(desiredIN, proposedIN, decision){
        fetch("http://localhost:8000/TradePlaza/artrade/post/",
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                "desiredItemNum" : desiredIN,
                "proposedItemNum" : proposedIN,
                "decision" : decision
            })
        })
        .then(res => res.json())
        .then(data => {console.log(Object.values(data)); setfetch_success(true)})
        .catch(error => {console.log(Object.values(error)); set_Fail_popup_state(true)})
        
        //popup message and go main menu
        //set_popup_state(current => !current);
        
    }


    //call for fetch get at the beginning of loading page
    useEffect(() => {
        getList();
        },[])



    //click accept button popup -> go back to same page, check if list empty -> go to main menu
    function handleAccept(desiredIN, proposedIN, proposer_firstname, proposer_email){
        console.log(desiredIN, proposedIN, proposer_firstname, proposer_email);
        
        //setdesiredItemNum(desiredIN);
        //setproposedItemNum(proposedIN);
        setproposername(proposer_firstname);
        setproposeremail(proposer_email);
        artrade(desiredIN, proposedIN, 'accept');
        set_accept_popup_state(true);        
        
         //else{
            //set_acceptFail_popup_state(true);
         //}

    }
    
    //click accept button popup -> go back to same page, check if list empty -> go to main menu

    function handleRejected(desiredIN, proposedIN, proposer_firstname, proposer_email){
        
        //setdesiredItemNum(desiredIN);
        //setproposedItemNum(proposedIN);
        setproposername(proposer_firstname);
        setproposeremail(proposer_email);
        artrade(desiredIN, proposedIN, 'reject');
        
        set_reject_popup_state(true); 
        
         //else{
            //set_rejectFail_popup_state(true);
         //}

    }
    
    // go back to current page and refresh
    function handleClick(event){
        setfetch_success(false);
        set_accept_popup_state(false);
        set_Fail_popup_state(false);
        set_reject_popup_state(false);
        window.location.reload(false);
       // prevent default form post
        event.preventDefault();
        
    }
    

    function handleClick_noItem(event){
        navigate("/");
    }

    

    return (
        <div>
            <Navigation />
            {(myItemList.length > 0) ? (
            <React.Fragment>
               <TableContainer component={Paper}>
            
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                <TableRow>           
                            <TableCell align="left">Date</TableCell>
                            <TableCell align="left">Desired Item</TableCell>
                            <TableCell align="left">Proposer</TableCell>
                            <TableCell align="left">Rank</TableCell>
                            <TableCell align="left">Distance</TableCell>
                            <TableCell align="left">Proposed Item</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {myItemList.map((detailsRow) => (
                                <TableRow key={detailsRow.Date}>
                                <TableCell component="th" scope="row">
                                    {detailsRow.Date}
                                </TableCell>
                                    <TableCell align="left"><Link to={"/ViewItem"} state = {{'itemNumber': detailsRow.desiredItemNum}}>{detailsRow.Desired_Item}</Link></TableCell>
                                    <TableCell align="left">{detailsRow.Proposer}</TableCell>
                                    <TableCell align="left">{detailsRow.Rank}</TableCell>
                                    <TableCell align="left">{detailsRow.Distance} miles</TableCell>
                                    <TableCell align="left"><Link to={'/ViewItem'} state = {{'itemNumber': detailsRow.proposedItemNum}}>{detailsRow.Proposed_Item}</Link></TableCell>
                                    <TableCell align="left"><Button type= "submit" name="Accept"  onClick = {() => handleAccept(detailsRow.desiredItemNum, detailsRow.proposedItemNum, detailsRow.proposer_firstname, detailsRow.proposerEmail)}/>
                                                            <Button type= "submit" name="Reject" onClick = {() => handleRejected(detailsRow.desiredItemNum, detailsRow.proposedItemNum, detailsRow.proposer_firstname, detailsRow.proposerEmail)}/>
                                                            </TableCell>
                                </TableRow>
                ))}
                </TableBody>
            </Table>             
            </TableContainer> 
            </React.Fragment>
            )
            :  null}

            {(myItemList.length === 0) ?(
            <React.Fragment>
            <div style={{ marginTop: "40px" }}>
            <Dialog open = {myItemList.length === 0}>
            <DialogContent>You have no pending trade</DialogContent>
            <DialogContent><Button type= "submit" name="Go back to Main Menu"  onClick = {handleClick_noItem}/> </DialogContent>
            </Dialog>
            </div>
            </React.Fragment>
            ): null}
            
            
               
            <div style={{ marginTop: "40px" }}>
            <Dialog open = {fetch_success && accept_popup_state}>
            <DialogTitle>The Trade Has been Successfully <strong>Accepted</strong></DialogTitle>
            <DialogContent>Contact the proposer to trade items <br/>Email: {proposeremail} <br/> Name: {proposername}</DialogContent>
            <DialogContent><Button type= "submit" name="OK"  onClick = {handleClick}/> </DialogContent>
            </Dialog>
            </div>
            
            <div style={{ marginTop: "40px" }}>
            <Dialog open = {reject_popup_state && reject_popup_state}>
            <DialogTitle>The Trade Has been Successfully <strong>Rejected</strong></DialogTitle>
            <DialogContent><Button type= "submit" name="OK"  onClick = {handleClick}/> </DialogContent>
            </Dialog>
            </div>       
             
            

            

            <div style={{ marginTop: "40px" }}>
            <Dialog open = {Fail_popup_state}>
            <DialogTitle>Action Failed</DialogTitle>
            <DialogContent><Button type= "submit" name="OK"  onClick = {handleClick}/> </DialogContent>
            </Dialog>
            </div>
            
            <Footer />  
           
         
    </div>      
    );  
 
    
}
export default ARTrade;