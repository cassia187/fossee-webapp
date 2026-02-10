import { useState } from "react";
import { registerUser } from "../services/auth";
import { useNavigate } from "react-router-dom";

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await registerUser({
        username,
        email,
        password,
      });

      localStorage.setItem("token", res.data.token);
      navigate("/dashboard");
    } catch {
      alert("Registration Failed");
    }
  };

  return (
    <div className="center-container">
      <div className="card">
        <h2>Register</h2>

        <form onSubmit={handleRegister}>
          <input
            className="input-field"
            placeholder="Username"
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            className="input-field"
            type="email"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            className="input-field"
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button className="btn">Register</button>
        </form>

        <div
          className="switch-text"
          onClick={() => navigate("/")}
        >
          Already have an account? Login
        </div>
      </div>
    </div>
  );
}

export default Register;
