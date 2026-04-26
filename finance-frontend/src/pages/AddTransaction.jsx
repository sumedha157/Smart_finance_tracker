import { useState } from "react";
import { addTransaction } from "../api/api";

const AddTransaction = () => {
  const [title, setTitle] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const token = localStorage.getItem("token");

  const handleSubmit = async (e) => {
  e.preventDefault();

  setLoading(true);   // ✅ START loading

  const data = {
    title,
    amount: parseFloat(amount),
  };

  try {
    const res = await addTransaction(data, token);

    setMessage(
      `Added! Category: ${res.category} (Confidence: ${res.confidence?.toFixed(2)})`
    );

    setTitle("");
    setAmount("");
  } catch (err) {
    setMessage("Error adding transaction");
  }

  setLoading(false);  // ✅ STOP loading
};

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Add Transaction</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        
        {/* Title */}
        <input
          type="text"
          placeholder="Enter transaction (e.g. Zomato, Uber)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />

        {/* Amount */}
        <input
          type="number"
          placeholder="Enter amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />

        {/* Submit */}
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700" disabled={loading}>
            {loading ? "Adding..." : "Add Transaction"}
        </button>
      </form>

      {/* Result Message */}
      {message && (
        <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">
          {message}
        </div>
      )}
    </div>
  );
};

export default AddTransaction;