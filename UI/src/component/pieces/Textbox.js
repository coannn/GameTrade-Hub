import React, { useState } from "react";

class Textbox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};   
        this.handleChange = this.handleChange.bind(this);
      }
    
      callBackMethod(value){
        this.props.sendData(value);
      }

    handleChange(event) {
        this.setState({value: event.target.value});
        this.callBackMethod(event.target.value);
      }
    

    render() {
    return(
    // <form onSubmit={handleSubmit}>
    <form>
    <label>
    <div className="left">{this.props.name}</div> 
        <input value={this.state.value} onChange ={this.handleChange} type="text" name={this.props.name}></input>
    </label>
    </form>
    )
    }
}

export default Textbox;
