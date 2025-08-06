import { useForm } from 'react-hook-form';
import { useState } from 'react';
import api from '../api';

const RegisterForm = ({ onRegisterationSuccess, onClosure }) => {
  const { register, handleSubmit } = useForm();
  const [errorState, setErrorState] = useState(false);
  const [registerError, setRegisterError] = useState('');

  const onSubmit = async (data) => {
    try {
      const signupData = {
        email: data.email,
        user_name: data.username,
        password: data.password,
      };

      const response = await api.post("/users/signup/", signupData);

      if (response.status === 200) {
        setErrorState(false);
        setRegisterError('');
        onRegisterationSuccess();
      }
    } catch (error) {
      console.log(error.response?.data?.detail);
      setRegisterError(error.response?.data?.detail || "Registration failed.");
      setErrorState(true);
    }
  };

  return (
    <div className="fixed inset-0 bg-white bg-opacity-50 flex justify-center items-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-xl font-bold mb-4 text-center text-cyan-900">Register</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col space-y-4">
          <input
            className="border border-gray-300 rounded px-3 py-2"
            placeholder="Email"
            {...register("email", { required: true })}
          />
          <input
            className="border border-gray-300 rounded px-3 py-2"
            placeholder="Username"
            {...register("username", { required: true, minLength: 2, maxLength: 256 })}
          />
          <input
            type="password"
            className="border border-gray-300 rounded px-3 py-2"
            placeholder="Password"
            {...register("password", { required: true, minLength: 8, maxLength: 512 })}
          />
          <input
            type="submit"
            value="Sign Up"
            className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 cursor-pointer"
          />
        </form>
        {errorState && (
          <div className="text-red-600 text-sm mt-2 text-center">{registerError}</div>
        )}
        <button
          onClick={onClosure}
          className="mt-4 text-sm text-gray-500 hover:text-gray-700 block mx-auto cursor-pointer"
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default RegisterForm;
