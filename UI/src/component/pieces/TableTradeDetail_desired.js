import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {useState, useEffect} from "react";


export default function TableDesiredItem(props) {
  const [item, setItem] = useState([]);
  // fetch get to collect for get data
  const getItem = async () => {
    const response = await fetch("http://localhost:8000/TradePlaza/display_tradedetail/desiredItem/"+props.itemNumber);
    const data = await response.json();
    console.log(data.data);
    setItem(data.data)
    console.log(data.data); // probably a safer way to do this, but if you console.log(data) you'll see an object is being returned, not an array.  
  return item;
};
  //call for fetch get at the beginning of loading page
    useEffect(() => {
      getItem();
        },[])
return (
 <TableContainer component={Paper}>
   <Table sx={{ minWidth: 650 }} aria-label="simple table">
     <TableHead>
       <TableRow>           
                 <TableCell align="left">Item #</TableCell>
                 <TableCell align="left">Title</TableCell>
                 <TableCell align="left">Game type</TableCell>
                 <TableCell align="left">Condition</TableCell>
                 {(item.description !== null && item.description !== '' && item.description !== '\r') &&<TableCell align="left">Description</TableCell>}
                 {(item.game_type==='CollectiveCardGame') && <TableCell align="left">Card #</TableCell>}
                  {(item.game_type === 'VideoGame' || item.game_type === 'ComputerGame') && <TableCell align="left">Platform</TableCell>}
                  {(item.game_type === 'VideoGame') && <TableCell align="left">Media</TableCell>}
 
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
                         <TableCell align="left">{item.condition}</TableCell>
                         {(item.description !== null && item.description !== '' && item.description !== '\r') &&<TableCell align="left">{item.description}</TableCell>}
                         {(item.game_type==='CollectiveCardGame') &&<TableCell align="left">{item.cardsOffered}</TableCell>}
              {(item.game_type === 'VideoGame' || item.game_type === 'ComputerGame') && <TableCell align="left">{item.platform}</TableCell> }                    
              {(item.game_type === 'VideoGame') &&<TableCell align="left">{item.media}</TableCell>}

                     </TableRow>
       }

     </TableBody>
   </Table>
 </TableContainer>
);
}