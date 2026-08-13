import FileUpload from "./components/FileUpload";

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="text-5xl font-bold text-center text-blue-700">
        AI Business Intelligence Platform
      </h1>

      <p className="text-center text-gray-600 mt-4">
        Upload your business datasets to generate AI-powered insights.
      </p>

      <FileUpload />
    </div>
  );
}

export default App;