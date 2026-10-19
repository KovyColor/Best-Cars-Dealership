import React, { useState } from "react";
import axios from "axios";

const initialForm = { username: "", first_name: "", last_name: "", email: "", password: "" };

export default function Register() {
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState("");

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("/djangoapp/register", form);
      setMessage(`Welcome, ${response.data.userName}.`);
      setForm(initialForm);
    } catch (error) {
      const detail = error.response && error.response.data && error.response.data.error;
      setMessage(detail || "Registration failed. Please try again.");
    }
  };

  return (
    <form onSubmit={handleSubmit} aria-label="Register">
      <label htmlFor="username">Username</label>
      <input id="username" name="username" value={form.username} onChange={handleChange} required />
      <label htmlFor="first_name">First Name</label>
      <input id="first_name" name="first_name" value={form.first_name} onChange={handleChange} required />
      <label htmlFor="last_name">Last Name</label>
      <input id="last_name" name="last_name" value={form.last_name} onChange={handleChange} required />
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" value={form.email} onChange={handleChange} required />
      <label htmlFor="password">Password</label>
      <input id="password" name="password" type="password" value={form.password} onChange={handleChange} required />
      <button type="submit">Register</button>
      {message && <p role="status">{message}</p>}
    </form>
  );
}
