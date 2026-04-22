
function App() {
  return (
    <div className="flex">
      <div id='left-panel' className="bg-gray-500 flex-[1.2]">
        <div className="min-h-screen">EXPLANATION HERE</div>
        <div className="min-h-screen">EXPLANATION HERE</div>
        <div className="min-h-screen">EXPLANATION HERE</div>
      </div>
      <div id='right-panel' className="sticky top-0 bg-gray-300 flex-1 h-screen">VISUALIZER HERE</div>
    </div>
  );
}

export default App;