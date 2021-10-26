import React from "react"
import Lovelyz from "./Lovelyz";
import {Container} from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
  return(
    <Container>
      <img src='lovelyz_logo.png' style={{display:"block", marginLeft:"auto", marginRight:"auto"}} alt=""/>
      <hr />
      <Lovelyz />
      
    </Container>
    
  )

};

export default App;
