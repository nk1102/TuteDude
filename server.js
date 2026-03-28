const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Schema
const todoSchema = new mongoose.Schema({
  itemName: String,
  itemDescription: String,
});

const Todo = mongoose.model("Todo", todoSchema);

// Route
app.post("/submittodoitem", async (req, res) => {
  const { itemName, itemDescription } = req.body;

  const newTodo = new Todo({ itemName, itemDescription });
  await newTodo.save();

  res.json({ message: "Item saved successfully" });
});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});