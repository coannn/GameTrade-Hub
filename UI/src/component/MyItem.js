import React from "react";
import Navigation from "./pieces/Navigation";
import Footer from "./pieces/Footer";
import TableItemCounts from "./pieces/TableItemCounts";
import TableMyItem from "./pieces/TableMyItem";

function MyItem(){
    return (
        <div>
            <Navigation />
            <br></br>
            <h2> Item counts</h2>
            <div className="table">
                <TableItemCounts />
            </div>
            <h2> My Items</h2>
            <div className="table">
                <TableMyItem />
            </div>
            <Footer />
        </div>
        
    )
}

export default MyItem;