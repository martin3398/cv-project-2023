import React from 'react';
import './App.css';
import {Col, Container, Navbar, Row, Button} from "react-bootstrap";
import InputCard from "./components/InputCard";

function App() {
  const [image, setImage] = React.useState<string | null>(null);

  const upload = (image: string) => {
    setImage(image)
  }

  return (
    <Container>
      <Row>
        <Navbar bg="dark" variant="dark" fixed='top' className="custom-nav">
          <Navbar.Brand href="#home">
            &nbsp;
            <img
              alt=""
              src="/logo.png"
              width="35vw"
              className="d-inline-block align-top"
            />
            &nbsp;
            License Plate Classification
          </Navbar.Brand>
        </Navbar>
      </Row>

      <Row className="card-container">
        <Col>
          <InputCard image={image} setImage={upload}/>
        </Col>
        <Col>
          abc
        </Col>
      </Row>

      <Row>
        <Navbar bg="dark" variant="dark" fixed='bottom' className="custom-nav">
          <Navbar.Brand href="#home">
            &nbsp;
            <img
              alt=""
              src="/logo.png"
              width="35vw"
              className="d-inline-block align-top"
            />
            &nbsp;
            License Plate Classification
          </Navbar.Brand>
          <Row>
            <Col xs="auto">
              <Button disabled={!image}>Find Bounding Box</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!image}>Crop Bounding Box</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!image}>Transform Homography</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!image}>OCR Detection</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!image}>All</Button>
            </Col>
          </Row>
        </Navbar>
      </Row>
    </Container>
  );
}

export default App;
