import { useState } from "react";
import { loginUser } from "../services/auth";
import { useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser({ username, password });
      localStorage.setItem("token", res.data.token);
      navigate("/dashboard");
    } catch {
      alert("Invalid Credentials");
    }
  };

  return (
    <div className="center-container">
      <div className="card">
        <h2>Login</h2>

        <form onSubmit={handleLogin}>
          <input
            className="input-field"
            placeholder="Username"
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            className="input-field"
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="btn">Login</button>
        </form>

        <div
          className="switch-text"
          onClick={() => navigate("/register")}
        >
          Don’t have an account? Register
        </div>
      </div>
    </div>
  );
}

export default Login;
