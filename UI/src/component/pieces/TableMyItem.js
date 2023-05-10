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



export default function TableMyItem() {

  const { currentUser } = useAuth();
  console.log(currentUser);

  const [myitem, setMyitem] = useState([]);
  const getMyitem = async() => {
    const response = await fetch('http://localhost:8000/tradeplaza/display_myitem/' + currentUser.email);
    const data = await response.json();
    console.log(data.data)
    setMyitem(data.data); 
    return myitem;
  };

  useEffect(() => {
    getMyitem();
  }, []);
  
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>           
                    <TableCell align="left">Item #</TableCell>
                    <TableCell align="left">Game type</TableCell>
                    <TableCell align="left">Title</TableCell>
                    <TableCell align="left">Condition</TableCell>
                    <TableCell align="left">Description</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {myitem.map((detailsRow) => (
                        <TableRow key={detailsRow.itemNum}>
                        <TableCell component="th" scope="row">
                            {detailsRow.itemNumber}
                        </TableCell>
                            <TableCell align="left">{detailsRow.game_type}</TableCell>
                            <TableCell align="left">{detailsRow.title}</TableCell>
                            <TableCell align="left">{detailsRow.condition}</TableCell>
                            <TableCell align="left">{detailsRow.description}</TableCell>
                            <TableCell align="left"><Link to={'/ViewItem'} state={{'itemNumber':detailsRow.itemNumber}}>Detail</Link></TableCell>
                        </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

