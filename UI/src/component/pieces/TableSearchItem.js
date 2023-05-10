import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {Link} from 'react-router-dom';
import { useAuth } from "../../authentication/AuthContext";


export default function TableSearchItem(props) {
  const { currentUser } = useAuth();
  console.log(currentUser); 
  
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
                    <TableCell align="left">Response Time (days)</TableCell>
                    <TableCell align="left">Rank</TableCell>
                    <TableCell align="left">Distance</TableCell>
                    <TableCell align="left">Detail</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>

          {props.input.map(function(detailsRow, index){ 
            let style;
            if(detailsRow.response_time==='None'){
                style = {color: "black"}
            } else if (detailsRow.response_time>=0 && detailsRow.response_time<7.1){
              style = {color: "green"}
            } else if (detailsRow.response_time>=7.1 && detailsRow.response_time<=14.0){
              style = {color: "yellow"}
            } else if (detailsRow.response_time>14.0 && detailsRow.response_time<=20.9){
              style = {color: "orange"}
            } else if (detailsRow.response_time>=21.0 && detailsRow.response_time<=27.9){
              style = {color: "red"}
            } else {
              style = {color: 'red', fontWeight: 'bold'}
            }
            
            let kStyleType;
            let kStyleDescription;
            let kStyleTitle;
            let kStyleCondition;

            console.log(detailsRow.description.includes(props.keyword))
            if(props.select === "keyword"){

              if(detailsRow.description && detailsRow.description.toLowerCase().includes(props.keyword.toLowerCase())){
                kStyleDescription= {backgroundColor: "lightblue"}
              } else {
                kStyleDescription= {backgroundColor: "white"}
              }

              if(detailsRow.title && detailsRow.title.toLowerCase().includes(props.keyword.toLowerCase())){
                kStyleTitle= {backgroundColor: "lightblue"}
              } else {
                kStyleTitle= {backgroundColor: "white"}
              }

            }
            return(
                        <TableRow key={detailsRow.itemNumber}>
                        {(detailsRow.fk_email!==currentUser.email) && <TableCell component="th" scope="row">
                            {detailsRow.itemNumber}
                        </TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell sx={kStyleType} align="left">{detailsRow.game_type}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell sx={kStyleTitle} align="left">{detailsRow.title}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell sx={kStyleCondition} align="left">{detailsRow.condition}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell sx={kStyleDescription} align="left">{detailsRow.description}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell sx={style} align="left" >{detailsRow.response_time}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell align="left">{detailsRow.rank}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell align="left">{detailsRow.distance === 0 ? detailsRow.distance.toFixed(1) : detailsRow.distance}</TableCell>}
                            {(detailsRow.fk_email!==currentUser.email) && <TableCell align="left"><Link to={'/ViewItem'} state= {{'itemNumber': detailsRow.itemNumber}}>Detail</Link></TableCell>}
                        </TableRow>
          )})}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
