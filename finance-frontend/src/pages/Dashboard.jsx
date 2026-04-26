import { useEffect, useState } from "react";
import { getInsights } from "../api/api";
import CategoryChart from "../components/CategoryChart";

const Dashboard = () => {
  const [data, setData] = useState(null);

  const token = localStorage.getItem("token"); // from login

  useEffect(() => {
    const fetchData = async () => {
      const res = await getInsights(token);
      setData(res);
    };
    fetchData();
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 shadow rounded">
          <h2>Total Spent</h2>
          <p className="text-xl font-bold">₹{data.total_spent}</p>
        </div>

        <div className="bg-white p-4 shadow rounded">
          <h2>Remaining</h2>
          <p className="text-xl font-bold">₹{data.remaining}</p>
        </div>

        <div className="bg-white p-4 shadow rounded">
          <h2>Budget Used</h2>
          <p className="text-xl font-bold">{data.percent_used}%</p>
        </div>
      </div>

      {/* Alert */}
      {data.alert && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {data.alert}
        </div>
      )}

      {/* Suggestion */}
      {data.suggestion && (
        <div className="mt-4 p-3 bg-blue-100 text-blue-700 rounded">
          {data.suggestion}
        </div>
      )}
       <div className="flex justify-center">
      <CategoryChart data={data.category_breakdown} />
    </div>
    </div>
  );
};

export default Dashboard;