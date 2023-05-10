import React, {useState} from "react";
import Footer from './pieces/Footer'
import Box from './pieces/Box'
import Nav from './pieces/Nav'
import { useAuth } from "../authentication/AuthContext";

function MainMenu(){
    const [fname, setFirstName] = useState('');
    const [lname , setLastName] = useState('');
    const [nickName , setNickName] = useState('');
    const [unacceptedTrades,setTrades]=useState(0);
    const [responseTime, setTime] = useState(0);
    const [myRank, setRank] = useState('');

    const { currentUser } = useAuth();

    fetch('http://127.0.0.1:8000/TradePlaza/main_menu/' + currentUser.email)
    .then(res => res.json())
    .then(data => {
        if (data && data.data.length === 4) {
            setFirstName(data.data[0].first_name);
            setLastName(data.data[0].last_name);
            setNickName(data.data[0].nickname);
            setTrades(data.data[1].unacceptedTrades);
            setRank(data.data[2].rank);
            setTime(data.data[3].responseTime);
        } else {
            console.log('Error: No enough data returned!');
        }
    })
    .catch(error => console.log({error}))

    return(
        <div>
            <Nav fname={fname} lname = {lname} nickName = {nickName}/>           
            <Box unacceptedTrades= {unacceptedTrades} responseTime={responseTime} myRank = {myRank}/>
            <Footer />
        </div>
    );

}
export default MainMenu;