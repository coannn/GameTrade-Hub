import '../App.css';
import MainMenu from './MainMenu'
import { Routes, Route, BrowserRouter } from "react-router-dom";
import ARTrade from "./ARTrade";
import ListItem from "./ListItem";
import MyItem from './MyItem'
import SearchItem from "./SearchItem";
import Login from './Login'
import TradeHistory from "./TradeHistory";
import Register from './Register';
import ViewItem from './ViewItem';
import ProposeTrade from './ProposeTrade';
import TradeDetail from './TradeDetail';
import PrivateRoute from './PrivateRoute';
import React from 'react';

function App() {
  return (
    <div className= "App">
      <BrowserRouter>
        <Routes>
          <Route exact path="/" element={<PrivateRoute><MainMenu /></PrivateRoute>} />
            <Route path="/Login" element={<Login />} />
            <Route path="/Register" element={<Register />} />
            <Route path="/ListItem" element={<PrivateRoute><ListItem /></PrivateRoute>} />
            <Route path="/MyItem" element={<PrivateRoute><MyItem /></PrivateRoute>} />
            <Route path="/SearchItem" element={<PrivateRoute><SearchItem /></PrivateRoute>} />
            <Route path="/ARTrade" element={<PrivateRoute><ARTrade /></PrivateRoute>} />
            <Route path="/TradeHistory" element={<PrivateRoute><TradeHistory /></PrivateRoute>} />
            <Route path="/TradeDetail" element={<PrivateRoute><TradeDetail /></PrivateRoute>} />
            <Route path="/ViewItem" element={<PrivateRoute><ViewItem /></PrivateRoute>} />
            <Route path="/ProposeTrade" element={<PrivateRoute><ProposeTrade /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App;
