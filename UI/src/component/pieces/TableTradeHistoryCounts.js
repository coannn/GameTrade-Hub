import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {useState, useEffect} from "react";
import { useAuth } from "../../authentication/AuthContext";


function createData(
  role      : string, 
  Total    : number, 
  Accepted       : number,
  Rejected : number,
  rejected_percentage: string
){
return { role, Total, Accepted, Rejected, rejected_percentage };
}

const rows = [
 createData("Proposer", 2,1,1,'50.0%'),
 createData("Counterparty", 2,2,0,'0.0%'),
];

export default function TableTradeHistoryCounts() {

  const { currentUser } = useAuth();
  console.log(currentUser);

  const [myItemList, setList] = useState([]);
  // fetch get to collect for get data
  const getList = async () => {
    const response = await fetch("http://localhost:8000/TradePlaza/display_tradehistory_count/" + currentUser.email);
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
                 <TableCell align="left">My role</TableCell>
                 <TableCell align="left">Total</TableCell>
                 <TableCell align="left">Accepted</TableCell>
                 <TableCell align="left">Rejected</TableCell>
                 <TableCell align="left">Rejected %</TableCell>
       </TableRow>
     </TableHead>
     <TableBody>
       {myItemList.map(function(detailsRow, index){
          let style;
          let percentage = parseFloat(detailsRow.rejected_percentage.replace("%",""))
          if(percentage>=50){
            style={backgroundColor:"red"}
          }
       return (
    
                     <TableRow key={detailsRow.role}>
                     <TableCell component="th" scope="row">
                         {detailsRow.role}
                     </TableCell>
                         <TableCell align="left">{detailsRow.Total}</TableCell>
                         <TableCell align="left">{detailsRow.Accepted}</TableCell>
                         <TableCell align="left">{detailsRow.Rejected}</TableCell>
                         <TableCell sx={style} align="left">{detailsRow.rejected_percentage}</TableCell>
                     </TableRow>
       )})}
     </TableBody>
   </Table>
 </TableContainer>
);
}

