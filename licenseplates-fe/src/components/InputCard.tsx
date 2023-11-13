import {Button, Card, Col} from "react-bootstrap";
import React, {ChangeEvent, MouseEventHandler} from "react";

type Props = {
  image: string|null,
  setImage: (image: string) => void,
}

const InputCard = ({image, setImage} : Props) => {
  const hiddenFileInput = React.useRef(null as HTMLInputElement | null);

  const handleUpload = (event: ChangeEvent<HTMLInputElement>)  => {
    const target = event.target;
    if (target && target.files && target.files.length > 0) {
      const fileUploaded = URL.createObjectURL(target.files[0])
      console.log(fileUploaded)
      setImage(fileUploaded)
    }
  }

  const handleClick = () => {
    hiddenFileInput.current?.click();
  }

  console.log(image)

  return (
    <Card bg="secondary" text="white" style={{ width: '100%' }}>
      <Card.Body>
        <Card.Text className="card-title">
            text
        </Card.Text>
      </Card.Body>

      {image && <Card.Img variant="bottom" src={image} width="50%"/>}

      <Card.Body>
        <input
          type="file"
          ref={hiddenFileInput}
          onChange={handleUpload}
          style={{ display: 'none' }}
        >
        </input>
        <Button className="float-right bt-all" onClick={handleClick}>Upload</Button>
      </Card.Body>
    </Card>
  )
}

export default InputCard;
