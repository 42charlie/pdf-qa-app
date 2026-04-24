import Banner from "./components/Banner";
import Document from "./components/Document";
import Chat from "./components/Chat";

function App() {
  return (
    <div className="bg-white h-screen flex">
      <Banner />
      <Document/>
      <Chat/>
    </div>
  );
}

export default App;