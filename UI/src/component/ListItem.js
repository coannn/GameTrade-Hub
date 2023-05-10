import React, {useState} from "react";
import Navigation from "./pieces/Navigation";
import Footer from "./pieces/Footer";
import DropdownSec from "./pieces/DropdownSec";
import Textbox from "./pieces/Textbox";
import Button from "./pieces/Button";
import { useAuth } from "../authentication/AuthContext";

const gameTypeList = [
    {id: 1, value: "Board game"}, 
    {id: 2, value: "Playing card game"}, 
    {id: 3, value: "Collectible card game"}, 
    {id: 4, value: "Video Game"}, 
    {id: 5, value: "Computer game"}
]

const conditionList = [
    {id: 1, value: "Unopened"}, 
    {id: 2, value: "Like New"}, 
    {id: 3, value: "Lightly Used"}, 
    {id:4, value: "Moderately Used"}, 
    {id: 5, value: "Heavily Used"},
    {id: 6, value: "Damaged/Missing parts"}
]

const videoPlatformList = [
    {id: 1, value: "Nintendo"}, 
    {id: 2, value: "PlayStation"}, 
    {id: 3, value: "Xbox"}
]

const computerPlatformList = [
    {id: 1, value: "Linux"}, 
    {id: 2, value: "macOS"}, 
    {id: 3, value: "Windows"}
]

const mediaList =[
    {id: 1, value: "optical disc"}, 
    {id: 2, value: "game card"}, 
    {id: 3, value: "cartridge"}
]

function ListItem(){    
    const [condition, setCondition] = useState('Unopened');
    const [game_type, setType] =useState('BoardGame');  
    const [title, setTitle] = useState('');
    const [cards_offered, setCard]= useState('');
    const [description, setdescription] = useState(''); 
    const [computer_platform, setComputerPlatform] = useState('Linux');
    const [video_game_platform, setVideoPlatform] = useState('Nintendo');
    const [media, setMedia] = useState('optical disc');
    const [unacceptedTrades, setTrades] = useState(0);
    let disable = false
    let tradealert = false;

    const { currentUser } = useAuth();
    console.log(currentUser);

    fetch('http://127.0.0.1:8000/TradePlaza/main_menu/' + currentUser.email)
    .then(res => res.json())
    .then(data => {
        if (data && data.data.length === 4) {
            setTrades(data.data[1].unacceptedTrades);
        } else {
            console.log('Error: No enough data returned!');
        }
    })
    .catch(error => console.log({error}))

    if(unacceptedTrades>=2){
        disable = true;
        tradealert = true;
    }


    function getDatafromChildDropGameType(val){
        console.log(val);
        if( val ==='Video Game'){
            setType('VideoGame');
        } else if(val ==='Board game'){
            setType('BoardGame');
        } else if(val ==='Playing card game'){
            setType('PlayingCardGame');
        } else if(val ==='Collectible card game'){
            setType('CollectiveCardGame');
        } else{
            setType('ComputerGame');
        }
    }

    function getDatafromChildDropCondition(val){
        console.log(val);
        if( val ==='Unopened'){
            setCondition('Unopened');
        } else if (val === 'Like New'){
            setCondition('Like New');
        } else if (val === 'Lightly Used'){
            setCondition('Lightly Used');
        } else if (val === 'Moderately Used'){
            setCondition('Moderately Used');
        } else if (val === 'Heavily Used'){
            setCondition('Heavily Used');
        } else {
            setCondition('Damaged/Missing parts');
        }
    }
    
    function getDatafromChildDropComputerPlatform(val){
        console.log(val);

        if(val=== 'Linux'){
            setComputerPlatform('Linux');
        } else if (val === 'macOS'){
            setComputerPlatform('macOS');
        } else if (val === 'Windows'){
            setComputerPlatform('Windows');
        }
    }
    
    function getDatafromChildDropVideoPlatform(val){
        console.log(val);
        if (val === 'Xbox'){
            setVideoPlatform('Xbox');
        } else if (val === 'PlayStation'){
            setVideoPlatform('PlayStation');
        } else if ( val === 'Nintendo'){
            setVideoPlatform ('Nintendo');
        }   
    }

    function getDatafromChildDropMedia(val){
        console.log(val);
        if (val === 'optical disc'){
            setMedia('optical disc');
        } else if (val === 'game card'){
            setMedia('game card');
        } else if ( val === 'cartridge'){
            setMedia('cartridge');
        }   
    }

    function getDatafromChildTitle(val){
        console.log(val);
        setTitle(val);
    }

    function getDatafromChildCard(val){
        console.log(val);
        setCard(val);
    }

    function getDatafromChildDescription(val){
        console.log(val);
        setdescription(val);
    }

    function handleSubmit(event) {
        console.log(game_type)
        let correct = true;
        if(game_type===''){
            alert('select a game type')
            correct = false
        } else {
            if(title === ''){
                alert('enter a title')
                correct = false
            }
            if(condition ===''){
                alert('select a condition')
                correct = false
            }
            if(game_type==='CollectiveCardGame'){
                if(cards_offered === ''){
                    alert('enter cards offered')
                    correct = false
                }
            }
            if(game_type==='ComputerGame'){
                if(computer_platform === ''){
                    alert('select computer platform')
                    correct = false
                }
            }
            if(game_type==='VideoGame'){
                if(video_game_platform === ''){
                    alert('select Video game platform')
                    correct = false
                }
                if(media === ''){
                    alert('select Video game media')
                    correct = false
                }
            }
        }
        correct && Fetch();
        event.preventDefault();
       
    }


    function Fetch(){
        fetch("http://localhost:8000/tradeplaza/list_item/",
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body : JSON.stringify({

            game_type,
            'email': currentUser.email,
            title,
            condition,
            cards_offered,
            computer_platform,
            media,
            video_game_platform,
            description
        })
    })
    .then(res => res.json())
    .then(data => 
        {   
            console.log(data.data[0]);
            alert('Your item has been listed! Your item number is '+data.data[0].fk_itemNumber+'.');
        })
    .catch(error => console.log({error}))
    }

    return (
        <div>
            <Navigation />
            <div className="left-container">
            <form action="" method="post" onSubmit={handleSubmit}>
            <DropdownSec sendData={getDatafromChildDropGameType} name="Game Type"  itemList = {gameTypeList}/>
            <Textbox sendData={getDatafromChildTitle} name="Title" />
            <DropdownSec sendData={getDatafromChildDropCondition} name="Condition" itemList = {conditionList}/>
            
            {(game_type==="VideoGame") &&
            <div>
            <DropdownSec sendData={getDatafromChildDropVideoPlatform} name="Video Platform" itemList = {videoPlatformList}/>
            <DropdownSec sendData={getDatafromChildDropMedia} name="Media" itemList = {mediaList}/>
            </div>
            }

            {(game_type==="ComputerGame") &&
            <div><DropdownSec sendData={getDatafromChildDropComputerPlatform} name="Computer Platform" itemList = {computerPlatformList}/></div>
            }

            {(game_type==="CollectiveCardGame") &&
            <div><Textbox sendData={getDatafromChildCard} name="Cards Offered" /></div>
            }
            
            <label>
            <div className="left">Description</div> 
            <Textbox sendData={getDatafromChildDescription}  id="description" />
            </label>
            
            <br></br>
            <Button type= "submit" name="List Item"  disabled={disable}/>
            </form>
            {tradealert && <p style = {{color: "red"}}>More than 2 unaccpeted trades, button is disabled!!</p>}
            </div>
            <Footer />
        </div>
    )
}

export default ListItem;