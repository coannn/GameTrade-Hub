import React, {useState} from "react";
import Footer from "./pieces/Footer";
import Navigation from "./pieces/Navigation";
import TableSearchItem from "./pieces/TableSearchItem";
import Button from "./pieces/Button";
import { useAuth } from "../authentication/AuthContext";
import { Alert } from "react-bootstrap";

function SearchItem(){
    const { currentUser } = useAuth();
    console.log(currentUser);
    
    const [keyword, setKey] = useState('') 
    const [postalCode, setPostal] = useState('') 
    const [miles, setDistance] = useState(0)
    const [select, setSelection] = useState('')
    
    const [sub,setsub]=useState(0)
    const [post,setpost]=useState(0)
    const [title,settitle]=useState(0)
    const [res,setres]=useState([])
    const [searchTitle, setSearch]=useState('');

    function getDatafromKeyword(event){
        console.log(event.target.value);
        setKey(event.target.value);
    }
    
    function getDatafromMiles(event){
        console.log(event.target.value);
        setDistance(event.target.value);
    }

    function getDatafromPostal(event){
        console.log(event.target.value);
        setPostal(event.target.value);
    }
    
    function handleSubmit(event) {
        if(select === ''){
            alert('select one search option!');
            window.location.reload();
        } else {
            getList();
            event.preventDefault();
            setsub(1);
            settitle(1);
            if(select === 'PostalCode'){
                setSearch('Search results: postalcode '+postalCode);
            } else if (select === 'keyword'){
                setSearch('Search results: '+select+' "'+keyword+'"');
            } else if (select === 'distance'){
                setSearch('Search results: '+select+' of '+miles +' miles');
            } else{
                setSearch('Search results: in my postal code');
            }
            console.log(searchTitle);
        }

    }
    const getList = async () => {
        const response = await fetch("http://localhost:8000/tradeplaza/search_item/",{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({
                'email': currentUser.email,
                select,
                keyword,
                miles,
                postalCode
            })
        });
        const data = await response.json();
        
        if (data.data === 'Invalid postal code.' && select==='PostalCode'){
            setpost(1);
        } else if(data.data.length === 0){ 
            setpost(0);
            alert('Sorry, no results found!')
            window.location.reload();
        } else {
            setpost(0);
            setres(data.data); 
        }
        
      return res;
    };

    
    function handleChange(event){
        console.log(event.target.value)
        setSelection(event.target.value)
    }


    return (
        <div>
            <Navigation />
            <div className="left-container">
                <form action="" onSubmit={handleSubmit}>
                    <input type="radio" name = "search" value='keyword' onChange={handleChange} id='keyword'></input>
                    <label for="keyword">By keyword: </label>
                    <input onChange ={getDatafromKeyword} type="text" name="keyword" ></input> 
                    <br></br>
                    <input type="radio" name ="search" value='myPostalCode' onChange={handleChange} id = 'mypostal'></input>
                    <label for="mypostal">In my postal code</label>
                    <br></br>
                    <input type="radio" name="search" value='distance' onChange={handleChange} id='miles'></input>
                    <label for="miles">Distance from me (miles): </label>
                    <input onChange ={getDatafromMiles} type="number" name="distance"></input>    
                    <br></br>
                    <input type="radio" name = "search" value='PostalCode' onChange={handleChange} id = 'postalCode'/>
                    <label for="postalCode">In postal code: </label>
                    <input onChange ={getDatafromPostal} type="text" name="postalCode" ></input> 
                    <p  > {(post===1) && <Alert className='errorMes_search' variant='danger'> Please enter a valid postal code!</Alert>} </p>   
                    <br></br>
                    <Button type= "submit" name="Search!"  />              
                </form>
            </div>

            {(sub===1 && post === 0) && <div className="table"><p>{searchTitle}</p><TableSearchItem select = {select} keyword = {keyword} input = {res} /></div>}
            <Footer />
        </div>
        
    )
}

export default SearchItem;