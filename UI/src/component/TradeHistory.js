import React from "react";
import Navigation from "./pieces/Navigation";
import Footer from "./pieces/Footer";
import TableTradeHistoryCounts from "./pieces/TableTradeHistoryCounts";
import TableTradeHistory from "./pieces/TableTradeHistory";

function TradeHistory(){
    return (
        <div>
        <Navigation />
        <h2> Trade history counts</h2>
            <div className="table">
                <TableTradeHistoryCounts />
            </div>
            <h2> Trade history</h2>
            <div className="table">
                <TableTradeHistory />
            </div>
        <Footer />
        </div>
        
    );
}

export default TradeHistory;