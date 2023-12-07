import React from 'react';
import './App.css';
import { Col, Container, Navbar, Row, Button } from 'react-bootstrap';
import InputCard from './components/InputCard';
import useApiResult from './components/useApiResult';
import ResultCard from './components/ResultCard';
import TextCard from './components/TextCard';

function App() {
  const [allFetching, setAllFetching] = React.useState(false);
  const [
    img,
    setImage,
    bbImage,
    bbFetching,
    fetchBb,
    croppedImage,
    croppedFetching,
    fetchCropped,
    transformedImage,
    transformedFetching,
    fetchTransformed,
    text,
    textFetching,
    fetchText,
  ] = useApiResult();

  const upload = (image: string) => {
    setImage(image);
  };

  const fetchAll = async () => {
    if (allFetching) return;
    setAllFetching(true);
    try {
      await fetchBb();
      await fetchCropped();
      await fetchTransformed();
      await fetchText();
    } catch (e) {
      console.log(e);
    }
    setAllFetching(false);
  };

  return (
    <Container>
      <Row>
        <Navbar bg="dark" variant="dark" fixed="top" className="custom-nav">
          <Navbar.Brand href="#home">
            &nbsp;
            <img alt="" src="/logo.png" width="35vw" className="d-inline-block align-top" />
            &nbsp; License Plate Classification
          </Navbar.Brand>
        </Navbar>
      </Row>

      <Row>
        <br />
        <br />
      </Row>

      <Row className="card-container">
        <Col>
          <div>
            <br />
            <InputCard image={img} setImage={upload} />
          </div>
        </Col>
        <Col>
          {text && (
            <div>
              <br />
              <TextCard text={text} title={'License Plate Text'} />
            </div>
          )}
          {transformedImage && (
            <div>
              <br />
              <ResultCard image={transformedImage} title={'Transformed Image'} />
            </div>
          )}
          {croppedImage && (
            <div>
              <br />
              <ResultCard image={croppedImage} title={'Cropped Image'} />
            </div>
          )}
          {bbImage && (
            <div>
              <br />
              <ResultCard image={bbImage} title={'Bounding Box Image'} />
            </div>
          )}
        </Col>
      </Row>

      <Row>
        <br />
        <br />
        <br />
        <br />
      </Row>

      <Row>
        <Navbar bg="dark" variant="dark" fixed="bottom" className="custom-nav">
          <Navbar.Brand href="#home">
            &nbsp;
            <img alt="" src="/logo.png" width="35vw" className="d-inline-block align-top" />
            &nbsp; License Plate Classification
          </Navbar.Brand>
          <Row>
            <Col xs="auto">
              <Button disabled={!img || bbFetching} onClick={() => fetchBb()}>
                Find Bounding Box
              </Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img || croppedFetching} onClick={() => fetchCropped()}>
                Crop Bounding Box
              </Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img || transformedFetching} onClick={() => fetchTransformed()}>
                Transform
              </Button>
            </Col>
            <Col xs="auto">
              <Button disabled={!img || textFetching} onClick={() => fetchText()}>
                OCR Detection
              </Button>
            </Col>
            <Col xs="auto">
              <Button
                disabled={!img || bbFetching || croppedFetching || transformedFetching || textFetching}
                onClick={() => fetchAll()}
              >
                All
              </Button>
            </Col>
          </Row>
        </Navbar>
      </Row>
    </Container>
  );
}

export default App;
