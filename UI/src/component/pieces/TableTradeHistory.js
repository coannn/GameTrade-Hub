import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {useState, useEffect} from "react";
import {Link} from 'react-router-dom';
import { useAuth } from "../../authentication/AuthContext";


function createData(
     proposedDate      : string, 
     decisionDate    : string, 
     status       : string,
     response_time : number,
     role: string,
     proposed_item: string,
     desired_item: string,
     other_user: string

){
  return { proposedDate, decisionDate, status, response_time, role,proposed_item, desired_item,other_user};
}

const rows = [
    createData("06/01/2021","06/02/2021","Accepted",1,"Proposer","Mastermind",'Skip-Bo', 'PrincessZ'),
    createData("05/15/2021","05/25/2021","Accepted",10,"Counterparty","Connect Four","Doom 3", "KingRhoam"),
  ];

export default function TableTradeHistory() {

  const { currentUser } = useAuth();
  console.log(currentUser);

  const [myItemList, setList] = useState([]);
  // fetch get to collect for get data
  const getList = async () => {
    const response = await fetch("http://localhost:8000/TradePlaza/display_tradehistory/" + currentUser.email);
    const data = await response.json();
    console.log(data)
    setList(data); // probably a safer way to do this, but if you console.log(data) you'll see an object is being returned, not an array.  
  return myItemList;
};
  //call for fetch get at the beginning of loading page
    useEffect(() => {
      getList();
        },[])
    
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>           
                    <TableCell align="left">Proposed Date</TableCell>
                    <TableCell align="left">Accepted/Rejected Date</TableCell>
                    <TableCell align="left">Trade Status</TableCell>
                    <TableCell align="left">Response time(days)</TableCell>
                    <TableCell align="left">My role</TableCell>
                    <TableCell align="left">Proposed Item</TableCell>
                    <TableCell align="left">Desired Item</TableCell>
                    <TableCell align="left">Other User</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {myItemList.map((detailsRow) => (
                        <TableRow key={detailsRow.proposedDate}>
                        <TableCell component="th" scope="row">
                            {detailsRow.proposedDate}
                        </TableCell>
                            <TableCell align="left">{detailsRow.decisionDate}</TableCell>
                            <TableCell align="left">{detailsRow.status}</TableCell>
                            <TableCell align="left">{detailsRow.response_time}</TableCell>
                            <TableCell align="left">{detailsRow.role}</TableCell>
                            <TableCell align="left">{detailsRow.proposed_item}</TableCell>
                            <TableCell align="left">{detailsRow.desired_item}</TableCell>
                            <TableCell align="left">{detailsRow.other_user}</TableCell>
                            <TableCell align="left"><Link to={"/TradeDetail"} state={{'proposedItemNum':detailsRow.proposedItemNum,'desiredItemNum':detailsRow.desiredItemNum,'proposedDate':detailsRow.proposedDate,'decisionDate':detailsRow.decisionDate,'status':detailsRow.status,'response_time':detailsRow.response_time,'role':detailsRow.role,'other_email':detailsRow.other_email}}>Detail</Link></TableCell>
                        </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

