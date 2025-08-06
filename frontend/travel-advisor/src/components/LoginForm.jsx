import { useForm } from 'react-hook-form';
import api from '../api';

const LoginForm = ({ onLoginSuccess, onClosure }) => {
  const { register, handleSubmit } = useForm();

  const onSubmit = async (data) => {
    const params = new URLSearchParams();
    params.append('username', data.email);
    params.append('password', data.password);

    try {
      const response = await api.post("/login/auth", params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      });

      const token = response.data.access_token;
      localStorage.setItem("token", token);
      onLoginSuccess();
    } catch (error) {
      console.error("Login failed:", error);
      alert("Login failed. Please check your credentials.");
    }
  };

  return (
    <div className="fixed min-h-lvh inset-0 bg-white bg-opacity-50 flex justify-center items-center z-1">
      <div className="bg-white p-6 rounded-lg shadow-lg w-full max-w-sm">
        <h2 className="text-xl font-bold text-center text-cyan-900">Login</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col space-y-4">
          <input
            className="border border-gray-300 rounded px-3 py-2"
            placeholder="Email"
            {...register("email", { required: true })}
          />
          <input
            type="password"
            className="border border-gray-300 rounded px-3 py-2"
            placeholder="Password"
            {...register("password", { required: true })}
          />
          <input
            type="submit"
            value="Login"
            className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 cursor-pointer"
          />
        </form>
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

export default LoginForm;
