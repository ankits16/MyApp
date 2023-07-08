import React, { useContext, useState } from "react";
import { Context } from "../App";

const ParentContext = React.createContext()
export default function ParentComponent() {
  const [count, setCount] = useState(0);
  const messageFromParent = {'message': 'Hello from parent!', 'flower' : 'Rose'};
  const handleIncrement = () => {
    setCount(count + 1);
  };
  return (
    <ParentContext.Provider value={messageFromParent}>
      <ChildComponent name={"Ankit"} age={40} />
      <div>
        <p>The counter is set to {count}</p>
        <button onClick={handleIncrement}>Increment</button>
      </div>
    </ParentContext.Provider>
  );
}

function ChildComponent({ name, age }) {
  const context = useContext(Context);
  const parentContext = useContext(ParentContext)
  return (
    <div>
      <p>
        My name is {name} and my age is {age}
      </p>
      <p>Data passed by context = {context.message}</p>
      <p>Data passed from parent context = {parentContext.message} flower = {parentContext.flower}</p>
    </div>
  );
}
