import React from 'react';
import './App.css';
import {Col, Container, Navbar, Row, Button} from "react-bootstrap";
import InputCard from "./components/InputCard";
import useApiResult from "./components/useApiResult";
import ResultCard from "./components/ResultCard";

function App() {
  const [
    img,
    setImage,
    bbImage,
    bbFetching,
    fetchBb,
    croppedImage,
    croppedFetching,
    fetchCropped,
    homImage,
    homFetching,
    fetchHom,
    text,
    textFetching,
    setTextFetching,
  ] = useApiResult();

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

      <Row>
        <br/>
        <br/>
        <br/>
      </Row>

      <Row className="card-container">
        <Col>
          <InputCard image={img} setImage={upload}/>
        </Col>
          <Col>
            {bbImage &&
              <ResultCard image={bbImage} title={"Bounding Box Image"}/>
            }
            {croppedImage &&
              <ResultCard image={croppedImage} title={"Cropped Image"}/>
            }
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
              <Button disabled={!img} onClick={() => fetchBb()}>Find Bounding Box</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img} onClick={() => fetchCropped()}>Crop Bounding Box</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img}>Transform Homography</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img}>OCR Detection</Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img}>All</Button>
            </Col>
          </Row>
        </Navbar>
      </Row>
    </Container>
  );
}

export default App;
