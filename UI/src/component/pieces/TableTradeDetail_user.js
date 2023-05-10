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


export default function TableUserDetail(props) {

  const { currentUser } = useAuth();
  console.log(currentUser);

  const [myItemList, setList] = useState([]);
  // fetch get to collect for get data
  const getList = async () => {
    const response = await fetch("http://localhost:8000/TradePlaza/display_tradedetail/user_detail/?proposedItemNum="+ props.proposedItemNum + "&desiredItemNum=" + props.desiredItemNum +"&email=" + currentUser.email);
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
                 <TableCell align="left">Nickname</TableCell>
                 <TableCell align="left">Distance</TableCell>
                 <TableCell align="left">Name</TableCell>
                 <TableCell align="left">Email</TableCell>
       </TableRow>
     </TableHead>
     <TableBody>
       {myItemList.map((detailsRow) => (
                     <TableRow key={detailsRow.nickname}>
                     <TableCell component="th" scope="row">
                         {detailsRow.nickname}
                     </TableCell>
                         <TableCell align="left">{detailsRow.distance} miles</TableCell>
                         <TableCell align="left">{detailsRow.first_name}</TableCell>
                         <TableCell align="left">{detailsRow.email}</TableCell>
                     </TableRow>
       ))}
     </TableBody>
   </Table>
 </TableContainer>
);
}