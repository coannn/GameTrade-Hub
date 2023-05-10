import React from "react";
import Navigation from "./pieces/Navigation";
import Footer from "./pieces/Footer";
import TableTradeDetail from "./pieces/TableTradeDetail";
import TableUserDetail from "./pieces/TableTradeDetail_user";
import TableProposedItem from "./pieces/TableTradeDetail_proposed";
import TableDesiredItem from "./pieces/TableTradeDetail_desired";
import {useNavigate, useLocation } from 'react-router-dom'

function TradeDetail(){
    const location = useLocation()
    console.log(location.state)
    return (
        <div>
        <Navigation />
        <h2> Trade Detail</h2>
            <div className="table">
                <TableTradeDetail proposedDate={location.state.proposedDate} decisionDate={location.state.decisionDate} status={location.state.status} response_time={location.state.response_time} role={location.state.role}/>
            </div>
            <h2> User Detail</h2>
            <div className="table">
                <TableUserDetail proposedItemNum={location.state.proposedItemNum} desiredItemNum={location.state.desiredItemNum}/>
            </div>
            <h2> Proposed Item</h2>
            <div className="table">
                <TableProposedItem itemNumber={location.state.proposedItemNum}/>
            </div>
            <h2> Desired Item</h2>
            <div className="table">
                <TableDesiredItem itemNumber={location.state.desiredItemNum}/>
            </div>
        <Footer />
        </div>
        
    );
}

export default TradeDetail;