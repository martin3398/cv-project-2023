import {useState} from "react";

const useApiResult = () => {
  const [img, setImg] = useState<string | null>(null);
  const [bbImage, setBbImage] = useState<string | null>(null);
  const [croppedImage, setCroppedImage] = useState<string | null>(null);
  const [homImage, setHomImage] = useState<string | null>(null);
  const [text, setText] = useState<string | null>(null);

  const [bbFetching, setBbFetching] = useState<boolean>(false);
  const [croppedFetching, setCroppedFetching] = useState<boolean>(false);
  const [homFetching, setHomFetching] = useState<boolean>(false);
  const [textFetching, setTextFetching] = useState<boolean>(false);

  const setImage = (image: string) => {
    setImg(image)
    setBbImage(null)
    setHomImage(null)
    setText(null)
  }

  const fetchImg = async (url: string) => {
    if (!img) {
      return
    }
    const imgResponse = await fetch(img);
    const blob = await imgResponse.blob()
    const formData = new FormData();
    formData.append("file", blob, "a.jpg");

    return fetch(url, {
        method: 'POST',
        headers: {
          'mode': 'no-cors',
        },
        body: formData,
    })
  }

  const fetchBb = async () => {
    setBbFetching(true)

    const img = await fetchImg('http://localhost:8000/api/bounding-box')
    const blob = await img?.blob()
    if (blob) {
      const url = URL.createObjectURL(blob)
      setBbImage(url ?? null)
    }

    setBbFetching(false)
  }

  const fetchCropped = async () => {
    setCroppedFetching(true)

    const img = await fetchImg('http://localhost:8000/api/crop-bounding-box')

    const blob = await img?.blob()
    if (blob) {
      const url = URL.createObjectURL(blob)
      setCroppedImage(url ?? null)
    }

    setCroppedFetching(false)
  }

  const fetchHom= async () => {
    setHomFetching(true)

    const img = await fetchImg('http://localhost:8000/api/transform-hom')
    const blob = await img?.blob()
    if (blob) {
      const url = URL.createObjectURL(blob)
      setHomImage(url ?? null)
    }

    setHomFetching(false)
  }

  const fetchText = async () => {
    setTextFetching(true)

    const img = await fetchImg('http://localhost:8000/api/ocr')
    const blob = await img?.blob()
    if (blob) {
      const url = URL.createObjectURL(blob)
      setText(url ?? null)
    }

    setTextFetching(false)
  }

  return [
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
  ] as const
}

export default useApiResult;
