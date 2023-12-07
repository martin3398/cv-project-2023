import { Button, Card } from 'react-bootstrap';
import React from 'react';

type Props = {
  title: string;
  text: string | null;
};

const TextCard = ({ title, text }: Props) => (
  <Card bg="secondary" text="white" style={{ width: '100%' }}>
    <Card.Body>
      <Card.Title>{title}</Card.Title>
      <Card.Text>{text || ''}</Card.Text>
    </Card.Body>
  </Card>
);

export default TextCard;
