import Footer from './pieces/Footer'
import TableViewItem from "./pieces/TableViewItem";
import Navigation from "./pieces/Navigation";
import Button from "./pieces/Button";
import {useNavigate, useLocation} from 'react-router-dom'
import React, {useState, useEffect} from "react";
import Radio from '@mui/material/Radio';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { RadioGroup } from '@mui/material';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import { gridColumnsTotalWidthSelector } from '@mui/x-data-grid';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import Grid from '@mui/material/Grid';
import { useAuth } from "../authentication/AuthContext";


function ProposeTrade(){

    const navigate = useNavigate();
    const location = useLocation();

    const { currentUser } = useAuth();
    console.log(currentUser);


    //click confirm button go back to main menu
    function handleClick(event){
        navigate("/")
    }
    // (edge case) click confirm button go back to propose trade if user has not choosen a item
    function handleClickNoChoose(event){
        //change popup state to false
        set_nochoose_popup_state(false);
    }
    //confirmation popup go back to main menu
    const[popup_state, set_popup_state] = useState(false);
    const[noitem_popup_state, set_noitem_popup_state] = useState(false);
    const[nochoose_popup_state, set_nochoose_popup_state] = useState(false);


    //const
    const [desiredItemNum, setdesiredItem] = useState(location.state.itemNumber);
    const [desiredItemTitle, setdesiredItemTitle] = useState(location.state.title);
    const [distance, setdistance] = useState(location.state.distance);
    const [email, setEmail]= useState('');
    const [myItemList, setList] = useState([]);
    const [proposeItemNum, setValue] = useState(null);
    const [fetchmessage, setfetch]= useState(null);

    const handleChange = (event) => {
        setValue(event.target.value);
      };
    
    // fetch get to collect for get data
    const getList = async () => {
        const response = await fetch("http://localhost:8000/TradePlaza/proposeTrade/getMyItemList/?desiredItemNum="+ desiredItemNum +"&email=" + currentUser.email);
        //console.log(response);
        const data = await response.json();
        setList(data); // probably a safer way to do this, but if you console.log(data) you'll see an object is being returned, not an array.  
        //console.log(myItemList);
        return myItemList;
    };

    //console.log(myItemList);
    
    // function for comfirm button, fetch post if click
    function propose(event){
        fetch("http://localhost:8000/TradePlaza/proposeTrade/proposed/",
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                "desiredItemNum" : desiredItemNum,
                "proposedItemNum" : parseInt(proposeItemNum)
            })
        })
        .then(res => res.json())
        .then(data => {console.log(Object.values(data)); setfetch(Object.values(data.data))})
        .catch(error => {console.log(Object.values(error)); setfetch("Proposal Failed")})
        
        //popup message and go main menu
        set_popup_state(current => !current);
        
        // prevent default form post
        event.preventDefault();
    }


    //call for fetch get at the beginning of loading page
    useEffect(() => {
        getList();
        },[])
    
    // confirm if myItemList is empty (User has no item) or user does not choose anything
    function check_propose(event){
        //check if the user has no item
       if (myItemList.length == 0){
        set_noitem_popup_state(true);
        // prevent default form post
        event.preventDefault();
        //check if the user does not choose
    }else if(proposeItemNum == null){
        set_nochoose_popup_state(true);
        // prevent default form post
        event.preventDefault();
    }else{
        //go to fetch post add trade entry
        propose(event);
        // prevent default form post
        event.preventDefault();
    }
    }


    return (
        <div>
            <Navigation />
            
           <div style={{ marginTop: "40px", justifyContent:'center', alignItems:'center'}}>
            {distance >= 100 ? (<React.Fragment><Grid container justifyContent="center"><Alert severity = 'error' variant="filled" justifyContent='center' alignItems='center'> <strong>The other user is {distance} miles away !!! </strong></Alert></Grid> </React.Fragment>):null}
            {/* {distance < 100 ? (<React.Fragment> <Box sx={{ bgcolor: 'white' }}> The other user is {distance} miles away</Box></React.Fragment>):null} */}
            You are proposing a trade for: <br/><strong>{desiredItemTitle} </strong>
            </div> 
            <div style={{ marginTop: "40px", justifyContent:'center', alignItems:'center'}}>
            Please choose your proposed item:
            </div>
            <TableContainer component={Paper}>
            <RadioGroup name = 'Radio' onChange = {handleChange}>
                 <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                <TableRow>           
                            <TableCell align="left">itemNum</TableCell>
                            <TableCell align="left">gameType</TableCell>
                            <TableCell align="left">title</TableCell>
                            <TableCell align="left">condition</TableCell>
                            <TableCell align="left">Select</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {myItemList.map((detailsRow) => (
                                <TableRow key={detailsRow.itemNumber}>
                                <TableCell component="th" scope="row">
                                    {detailsRow.itemNumber}
                                </TableCell>
                                    <TableCell align="left">{detailsRow.game_type}</TableCell>
                                    <TableCell align="left">{detailsRow.title}</TableCell>
                                    <TableCell align="left">{detailsRow.condition}</TableCell>
                                    <TableCell align="left">
                                                            <Radio value={detailsRow.itemNumber}
                                                                onChange={handleChange}
                                                                size="small" name = 'Radio'>Select</Radio></TableCell>
                                </TableRow>
                ))}
                </TableBody>
            </Table>
            </RadioGroup>
            </TableContainer>

            <form action="" method="post" onSubmit={check_propose}>
                {myItemList.length !== 0 && <Button type= "submit" name="Comfirm"  />}
            </form>

            <div style={{ marginTop: "40px" }}>
            <Dialog open = {popup_state}>
            <DialogTitle>Confirmation Information</DialogTitle>
            <DialogContent>{fetchmessage}</DialogContent>
            <DialogContent><Button type= "submit" name="Go back to Main Menu"  onClick = {handleClick}/> </DialogContent>
            </Dialog>
            </div>

            <div style={{ marginTop: "40px" }}>
            <Dialog open = {noitem_popup_state}>
            <DialogTitle>Confirmation Information</DialogTitle>
            <DialogContent>You have no available item for trading</DialogContent>
            <DialogContent><Button type= "submit" name="Go back to Main Menu"  onClick = {handleClick}/> </DialogContent>
            </Dialog>
            </div>

            <div style={{ marginTop: "40px" }}>
            <Dialog open = {nochoose_popup_state}>
            <DialogTitle>Confirmation Information</DialogTitle>
            <DialogContent>You did NOT choose any item</DialogContent>
            <DialogContent><Button type= "submit" name="Go back to choose an item"  onClick = {handleClickNoChoose}/> </DialogContent>
            </Dialog>
            </div>        
            <Footer />  
           
         
    </div>      
    );  
 
    
}
export default ProposeTrade;