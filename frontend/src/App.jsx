import Section from "./components/Section";
import StickyVisualizer from "./components/StickyVisualizer";
import { steps } from "./data/steps";

function App() {
  return (
    <>
    <div className="flex gap-8 px-8">
      <div className="flex-[1.2] min-h-screen">
        {steps.map(step => (
          <Section key={step.id} title={step.title} description={step.description} />
        ))}
      </div>
      <StickyVisualizer />
    </div>
    </>
  );
}

export default App;