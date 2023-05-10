import * as React from 'react';
import { useState, useEffect} from "react"
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { useAuth } from "../../authentication/AuthContext";


function TableItemCounts() {
  
  const { currentUser } = useAuth();
  console.log(currentUser);

  const [count, setCount] = useState({
    BoardGame: 0,
    CollectiveCardGame:0,
    ComputerGame: 0,
    PlayingCardGame: 0,
    VideoGame: 0,
    Total: 0
  }) 
  
  const getCount = async() => {
    const response = await fetch("http://localhost:8000/tradeplaza/display_myitem_count/" + currentUser.email);
    const data = await response.json();
    console.log(data)
    setCount(data);
    return count;
  }

  useEffect(()=>{
    getCount();
  },{})
  
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>           
            <TableCell align="center">Board Game</TableCell>
            <TableCell align="center">Playing Card Game</TableCell>
            <TableCell align="center">Computer Game</TableCell>
            <TableCell align="center">Collectible Card Game</TableCell>
            <TableCell align="center">Video Game</TableCell>
            <TableCell align="center">Total</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
        <TableRow
              key={count.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align="center">{count.BoardGame}</TableCell>
              <TableCell align="center">{count.PlayingCardGame}</TableCell>
              <TableCell align="center">{count.ComputerGame}</TableCell>
              <TableCell align="center">{count.CollectiveCardGame}</TableCell>
              <TableCell align="center">{count.VideoGame}</TableCell>
              <TableCell align="center">{count.Total}</TableCell>
            </TableRow>
        {/* {Count.map(row => (
            <TableRow
              key={row.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <TableCell align="center">{row.BoardGame}</TableCell>
              <TableCell align="center">{row.PlayingCardGame}</TableCell>
              <TableCell align="center">{row.ComputerGame}</TableCell>
              <TableCell align="center">{row.ColCardGame}</TableCell>
              <TableCell align="center">{row.VideoGame}</TableCell>
              <TableCell align="center">{row.Total}</TableCell>
            </TableRow>
          ))} */}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
export default TableItemCounts;