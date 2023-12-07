import { Button, Card } from 'react-bootstrap';
import React from 'react';

type Props = {
  title: string;
  image: string | null;
};

const ResultCard = ({ image, title }: Props) => (
  <Card bg="secondary" text="white" style={{ width: '100%' }}>
    <Card.Body>
      <Card.Text className="card-title">{title}</Card.Text>
    </Card.Body>

    {image && <Card.Img variant="bottom" src={image} width="50%" />}
  </Card>
);

export default ResultCard;
