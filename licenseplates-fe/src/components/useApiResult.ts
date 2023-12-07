import { useState } from 'react';

const useApiResult = () => {
  const [img, setImg] = useState<string | null>(null);
  const [bbImage, setBbImage] = useState<string | null>(null);
  const [croppedImage, setCroppedImage] = useState<string | null>(null);
  const [transformedImage, setTransformedImage] = useState<string | null>(null);
  const [preprocessingImage, setPreprocessingImage] = useState<string | null>(null);
  const [text, setText] = useState<string | null>(null);

  const [bbFetching, setBbFetching] = useState<boolean>(false);
  const [croppedFetching, setCroppedFetching] = useState<boolean>(false);
  const [transformedFetching, setTransformedFetching] = useState<boolean>(false);
  const [preprocessingFetching, setPreprocessingFetching] = useState<boolean>(false);
  const [textFetching, setTextFetching] = useState<boolean>(false);

  const setImage = (image: string) => {
    setImg(image);
    setBbImage(null);
    setCroppedImage(null);
    setTransformedImage(null);
    setPreprocessingImage(null);
    setText(null);
  };

  const fetchImg = async (url: string) => {
    if (!img) {
      return;
    }
    const imgResponse = await fetch(img);
    const blob = await imgResponse.blob();
    const formData = new FormData();
    formData.append('file', blob, 'a.jpg');

    return fetch(url, {
      method: 'POST',
      headers: {
        mode: 'no-cors',
      },
      body: formData,
    });
  };

  const fetchBb = async () => {
    setBbFetching(true);

    const img = await fetchImg('http://localhost:8000/api/plot-bounding-box');
    const blob = await img?.blob();
    if (blob) {
      const url = URL.createObjectURL(blob);
      setBbImage(url ?? null);
    }

    setBbFetching(false);
  };

  const fetchCropped = async () => {
    setCroppedFetching(true);

    const img = await fetchImg('http://localhost:8000/api/crop-bounding-box');

    const blob = await img?.blob();
    if (blob) {
      const url = URL.createObjectURL(blob);
      setCroppedImage(url ?? null);
    }

    setCroppedFetching(false);
  };

  const fetchTransformed = async () => {
    setTransformedFetching(true);

    const img = await fetchImg('http://localhost:8000/api/transform');
    const blob = await img?.blob();
    if (blob) {
      const url = URL.createObjectURL(blob);
      setTransformedImage(url ?? null);
    }

    setTransformedFetching(false);
  };

  const fetchPreprocessing = async () => {
    setPreprocessingFetching(true);

    const img = await fetchImg('http://localhost:8000/api/preprocessing-steps');
    const blob = await img?.blob();
    if (blob) {
      const url = URL.createObjectURL(blob);
      setPreprocessingImage(url ?? null);
    }

    setPreprocessingFetching(false);
  };

  const fetchText = async () => {
    setTextFetching(true);

    const img = await fetchImg('http://localhost:8000/api/read-text');
    const json: { text: string } = await img?.json();
    setText(json.text);

    setTextFetching(false);
  };

  return [
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
    preprocessingImage,
    preprocessingFetching,
    fetchPreprocessing,
    text,
    textFetching,
    fetchText,
  ] as const;
};

export default useApiResult;
