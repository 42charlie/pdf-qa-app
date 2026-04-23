import { useEffect, useState } from "react";
import Section from "./components/Section";
import StickyVisualizer from "./components/StickyVisualizer";
import { steps } from "./data/steps";

function App() {
  const [activeStep, setActiveStep] = useState(steps[0].id);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) setActiveStep(entry.target.id);
        });
      }, { threshold: 0.6 }
    );

    steps.forEach(step => {
      const element = document.getElementById(step.id);
      if (element) observer.observe(element);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <>
    <div className="flex gap-8 px-8">
      <div className="flex-[1.2] min-h-screen">
        {steps.map(step => (
          <Section key={step.id} id={step.id} title={step.title} description={step.description} />
        ))}
      </div>
      <StickyVisualizer activeStep={activeStep} />
    </div>
    </>
  );
}

export default App;