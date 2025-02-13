import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

export const sendMessage = async (message) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, { query: message });
    return response.data;
  } catch (error) {
    console.error("Error fetching response:", error);
    return { response: "Something went wrong, please try again." };
  }
};
