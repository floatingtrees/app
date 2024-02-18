import { useForm, SubmitHandler } from 'react-hook-form';

export default function Upload() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm();

  const onSubmit: SubmitHandler = async (data) => {
    const formData = new FormData();
    formData.append('files', data.files);

    await fetch('/api/upload', {
        method: 'POST',
        body: formData,
    });    

    reset();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input type="file" multiple={true} />
    </form>
  );
}