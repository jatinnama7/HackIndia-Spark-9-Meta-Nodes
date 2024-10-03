import React, { useState } from "react";
import ChatBot from "react-simple-chatbot";
import { ThemeProvider } from "styled-components";

// Optional: Customize chatbot theme
const theme = {
  background: "#f5f8fb",
  headerBgColor: "#1976D2",
  headerFontColor: "#fff",
  headerFontSize: "15px",
  botBubbleColor: "#1976D2",
  botFontColor: "#fff",
  userBubbleColor: "#fff",
  userFontColor: "#4a4a4a",
};

// Function to create the steps dynamically
const createSteps = (userMessage, botResponse) => {
  return [
    {
      id: "1",
      message: "Hi, how can I help you today?",
      trigger: "2",
    },
    {
      id: "2",
      options: [
        { value: "info", label: "Get Information", trigger: "3" },
        { value: "contact", label: "Contact Support", trigger: "4" },
        { value: "custom", label: "Type your own message", trigger: "5" },
      ],
    },
    {
      id: "3",
      message: "You can get information from our website!",
      end: true,
    },
    {
      id: "4",
      message: "Please email us at support@example.com.",
      end: true,
    },
    {
      id: "5",
      message: "Type your message:",
      trigger: "user-input",
    },
    {
      id: "user-input",
      user: true,
      trigger: "handle-user-input",
    },
    {
      id: "handle-user-input",
      message: "Processing your request...",
      trigger: "fetch-response",
    },
    {
      id: "fetch-response",
      component: <FetchResponse />,
      waitAction: true,
      trigger: "2", // Loop back to step 2 for more options
    },
  ];
};

const FetchResponse = ({ steps }) => {
  const userMessage = steps["user-input"].value; // Retrieve user input
  const [botResponse, setBotResponse] = useState("Processing...");

  // Use effect to fetch response from Flask API
  React.useEffect(() => {
    const fetchResponse = async () => {
      try {
        const response = await fetch("http://localhost:5000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: userMessage }),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        setBotResponse(data.reply || "No reply from server.");
      } catch (error) {
        console.error("Error fetching response:", error);
        setBotResponse("Sorry, an error occurred.");
      }
    };

    fetchResponse();
  }, [userMessage]);

  return <div>{botResponse}</div>;
};

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
        <ChatBot steps={createSteps()} />
      </ThemeProvider>
    </div>
  );
}

export default App;
