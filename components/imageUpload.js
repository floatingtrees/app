import { useState } from 'react';

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [message, setMessage] = useState('');

  const handleImageChange = (e) => {
    setSelectedImage(e.target.files[0]);
  };

  const uploadImage = async (e) => {
    e.preventDefault();
    if (!selectedImage) {
      alert('Please select an image.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedImage);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      console.log(response)

      if (response.ok) {
        setMessage("Success");
      } else {
        alert('Image upload failed.');
      }
    } catch (error) {
      console.error('Error uploading the image:', error);
      alert('Error uploading image.');
    }
  };

  return (
    <form onSubmit={uploadImage}>
      <input type='file' onChange={handleImageChange} accept='image/*' />
      <button type='submit'>Upload Image</button>

      <p>{message}</p>
    </form>
  );
};

export default ImageUploader;
