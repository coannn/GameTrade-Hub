import React from "react";

class DropdownSec extends React.Component {
    constructor(props) {
      super(props);
      this.state = {value: ''};
  
      this.handleChange = this.handleChange.bind(this);
      // this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    callBackMethod(value){
      this.props.sendData(value);
    }

    handleChange(event) {
      this.setState({value: event.target.value});
      this.callBackMethod(event.target.value);
      // alert('A name was submitted: ' + event.target.value);
    }
  
    // handleSubmit(event) {
    //   alert('A name was submitted: ' + this.state.value);
    //   event.preventDefault();
    // }
  
    render() {
      return (
        // 
        <form>
          <label>
            <div className="left">{this.props.name}</div> 
            <select value={this.state.value} onChange ={this.handleChange}>
                {this.props.itemList.map(item=>(
                    <option key={item.key} value={item.value}>{item.value}</option>
                ))}
             </select>
          </label>
        </form>
      );
    }
  }

export default DropdownSec;