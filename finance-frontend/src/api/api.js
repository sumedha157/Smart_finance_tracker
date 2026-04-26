const BASE_URL = "http://127.0.0.1:8000/api/";

export const getInsights = async (token) => {
  const res = await fetch(BASE_URL + "insights/", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
};

export const addTransaction = async (data, token) => {
  const res = await fetch(BASE_URL + "add-transaction/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  return res.json();
};