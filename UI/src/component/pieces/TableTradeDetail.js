import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';



export default function TableTradeDetail(props) {
  console.log(props)
return (
 <TableContainer component={Paper}>
   <Table sx={{ minWidth: 650 }} aria-label="simple table">
     <TableHead>
       <TableRow>           
                 <TableCell align="left">Proposed</TableCell>
                 <TableCell align="left">Accepted/Rejected</TableCell>
                 <TableCell align="left">Status</TableCell>
                 <TableCell align="left">My role</TableCell>
                 <TableCell align="left">Response time</TableCell>
       </TableRow>
     </TableHead>
     <TableBody>
      {
                     <TableRow>
                     <TableCell component="th" scope="row">
                         {props.proposedDate}
                     </TableCell>
                         <TableCell align="left">{props.decisionDate}</TableCell>
                         <TableCell align="left">{props.status}</TableCell>
                         <TableCell align="left">{props.role}</TableCell>
                         <TableCell align="left">{props.response_time} days</TableCell>
                     </TableRow>
       }
     </TableBody>
   </Table>
 </TableContainer>
);
}
