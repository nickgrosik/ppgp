import { useState } from "react";
import { Toaster } from "react-hot-toast";
import Header from "./components/Header";
import Home from "./pages/Home";

const tabs = [
  "Keys",
  "Messages",
  "Files",
  "Advanced",
  "Settings",
];

function App() {
  const [activeTab, setActiveTab] = useState("Keys");

  return (
    <div className="app-shell">
      <Toaster 
      position="bottom-right"
      toastOptions={{ duration: 2400 }}
      />

      <Header />

      <div className="app-body">
        <nav className="tab-nav" aria-label="Primary Navigation">
          {tabs.map((tab) => (
            <button
              key={tab}
              type="button"
              className={
                tab === activeTab
                  ? "tab-button active"
                  : "tab-button"
              }
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </nav>

        <main className="app-main">
          <Home activeTab={activeTab} />
        </main>
      </div>
    </div>
  );
}

export default App;
