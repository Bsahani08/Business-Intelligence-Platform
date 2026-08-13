import { useState } from "react";
import axios from "axios";

function FileUpload() {
  const [salesFile, setSalesFile] = useState(null);
  const [featuresFile, setFeaturesFile] = useState(null);
  const [storesFile, setStoresFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!salesFile || !featuresFile || !storesFile) {
      setError("Please upload all three datasets.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();

    formData.append("sales", salesFile);
    formData.append("features", featuresFile);
    formData.append("stores", storesFile);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload/",
        formData
      );

      console.log("Backend response:", response.data);

      setResult(response.data);
    } catch (err) {
      console.error("Upload error:", err);

      if (err.response) {
        const detail = err.response.data?.detail;

        setError(
          typeof detail === "object"
            ? detail.message || "Dataset processing failed."
            : detail || "Server error."
        );
      } else {
        setError(
          "Unable to connect to the backend. Make sure FastAPI is running."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return "text-green-600";
    if (score >= 75) return "text-blue-600";
    if (score >= 50) return "text-yellow-600";
    return "text-red-600";
  };

  const getStatusStyle = (status) => {
    if (status === "Excellent") {
      return "bg-green-100 text-green-700";
    }

    if (status === "Good") {
      return "bg-blue-100 text-blue-700";
    }

    if (status === "Needs Improvement") {
      return "bg-yellow-100 text-yellow-700";
    }

    return "bg-red-100 text-red-700";
  };

  const DatasetQualityCard = ({ icon, title, quality }) => {
    if (!quality) return null;

    return (
      <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3">
            <div className="text-3xl">{icon}</div>

            <div>
              <h4 className="text-lg font-bold text-gray-800">
                {title}
              </h4>

              <p className="text-sm text-gray-500">
                Data quality analysis
              </p>
            </div>
          </div>

          <div
            className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusStyle(
              quality.quality_status
            )}`}
          >
            {quality.quality_status}
          </div>
        </div>

        {/* Quality Score */}
        <div className="bg-gray-50 rounded-xl p-5 mb-5 text-center">
          <p className="text-sm text-gray-500 mb-1">
            Quality Score
          </p>

          <p
            className={`text-4xl font-extrabold ${getScoreColor(
              quality.quality_score
            )}`}
          >
            {quality.quality_score}%
          </p>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-gray-50 rounded-xl p-4">
            <p className="text-xs text-gray-500">
              Rows
            </p>
            <p className="text-xl font-bold text-gray-800">
              {quality.rows.toLocaleString()}
            </p>
          </div>

          <div className="bg-gray-50 rounded-xl p-4">
            <p className="text-xs text-gray-500">
              Columns
            </p>
            <p className="text-xl font-bold text-gray-800">
              {quality.columns}
            </p>
          </div>

          <div className="bg-gray-50 rounded-xl p-4">
            <p className="text-xs text-gray-500">
              Missing Values
            </p>
            <p className="text-xl font-bold text-gray-800">
              {quality.total_missing_values.toLocaleString()}
            </p>
          </div>

          <div className="bg-gray-50 rounded-xl p-4">
            <p className="text-xs text-gray-500">
              Duplicate Rows
            </p>
            <p className="text-xl font-bold text-gray-800">
              {quality.duplicate_rows.toLocaleString()}
            </p>
          </div>
        </div>

        {/* Missing Percentage */}
        <div className="mt-4">
          <div className="flex justify-between text-sm mb-1">
            <span className="text-gray-500">
              Missing Data
            </span>

            <span className="font-semibold">
              {quality.missing_percentage}%
            </span>
          </div>

          <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-orange-400 rounded-full"
              style={{
                width: `${Math.min(
                  quality.missing_percentage,
                  100
                )}%`,
              }}
            />
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">

      {/* Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold mb-4">
          ✨ AI-Powered Data Analysis
        </div>

        <h2 className="text-4xl font-extrabold text-gray-900 mb-3">
          Upload Business Datasets
        </h2>

        <p className="text-gray-500 max-w-2xl mx-auto">
          Upload your business datasets and let the platform
          automatically validate, analyze, and evaluate data quality.
        </p>
      </div>

      {/* Upload Cards */}
      <div className="grid md:grid-cols-3 gap-5 mb-8">

        {/* Sales */}
        <div className="border-2 border-dashed border-gray-300 hover:border-blue-400 rounded-2xl p-6 bg-white transition">
          <div className="text-4xl mb-4">📊</div>

          <h3 className="font-bold text-lg mb-1">
            Sales Dataset
          </h3>

          <p className="text-sm text-gray-500 mb-5">
            Upload your sales transaction data
          </p>

          <input
            type="file"
            accept=".csv"
            onChange={(e) =>
              setSalesFile(e.target.files[0])
            }
            className="w-full text-sm"
          />

          {salesFile && (
            <p className="text-sm text-green-600 mt-3 truncate">
              ✓ {salesFile.name}
            </p>
          )}
        </div>

        {/* Features */}
        <div className="border-2 border-dashed border-gray-300 hover:border-purple-400 rounded-2xl p-6 bg-white transition">
          <div className="text-4xl mb-4">📈</div>

          <h3 className="font-bold text-lg mb-1">
            Features Dataset
          </h3>

          <p className="text-sm text-gray-500 mb-5">
            Upload external business features
          </p>

          <input
            type="file"
            accept=".csv"
            onChange={(e) =>
              setFeaturesFile(e.target.files[0])
            }
            className="w-full text-sm"
          />

          {featuresFile && (
            <p className="text-sm text-green-600 mt-3 truncate">
              ✓ {featuresFile.name}
            </p>
          )}
        </div>

        {/* Stores */}
        <div className="border-2 border-dashed border-gray-300 hover:border-green-400 rounded-2xl p-6 bg-white transition">
          <div className="text-4xl mb-4">🏪</div>

          <h3 className="font-bold text-lg mb-1">
            Stores Dataset
          </h3>

          <p className="text-sm text-gray-500 mb-5">
            Upload store information
          </p>

          <input
            type="file"
            accept=".csv"
            onChange={(e) =>
              setStoresFile(e.target.files[0])
            }
            className="w-full text-sm"
          />

          {storesFile && (
            <p className="text-sm text-green-600 mt-3 truncate">
              ✓ {storesFile.name}
            </p>
          )}
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl">
          ⚠️ {error}
        </div>
      )}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full bg-gray-900 hover:bg-black disabled:bg-gray-400 text-white py-4 rounded-xl text-lg font-bold transition shadow-lg"
      >
        {loading
          ? "⏳ Analyzing Your Data..."
          : "🚀 Analyze Business Data"}
      </button>

      {/* Results */}
      {result && (
        <div className="mt-12">

          {/* Success Header */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 bg-green-50 text-green-700 px-4 py-2 rounded-full text-sm font-semibold mb-3">
              ✓ Analysis Complete
            </div>

            <h3 className="text-3xl font-extrabold text-gray-900">
              Data Quality Report
            </h3>

            <p className="text-gray-500 mt-2">
              Your datasets have been validated and analyzed successfully.
            </p>
          </div>

          {/* Dataset Quality Cards */}
          {result.data_quality && (
            <div className="grid lg:grid-cols-3 gap-6">

              <DatasetQualityCard
                icon="📊"
                title="Sales Dataset"
                quality={result.data_quality.sales}
              />

              <DatasetQualityCard
                icon="📈"
                title="Features Dataset"
                quality={result.data_quality.features}
              />

              <DatasetQualityCard
                icon="🏪"
                title="Stores Dataset"
                quality={result.data_quality.stores}
              />

            </div>
          )}

          {/* Overall Dataset Summary */}
          <div className="mt-8 bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">

            <h4 className="text-xl font-bold text-gray-800 mb-5">
              📋 Dataset Summary
            </h4>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

              <div className="bg-blue-50 rounded-xl p-5">
                <p className="text-sm text-blue-600">
                  Sales Rows
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {result.sales_rows?.toLocaleString()}
                </p>
              </div>

              <div className="bg-purple-50 rounded-xl p-5">
                <p className="text-sm text-purple-600">
                  Features Rows
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {result.features_rows?.toLocaleString()}
                </p>
              </div>

              <div className="bg-green-50 rounded-xl p-5">
                <p className="text-sm text-green-600">
                  Stores Rows
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {result.stores_rows?.toLocaleString()}
                </p>
              </div>

              <div className="bg-orange-50 rounded-xl p-5">
                <p className="text-sm text-orange-600">
                  Merged Rows
                </p>
                <p className="text-2xl font-bold text-gray-900">
                  {result.merged_rows?.toLocaleString()}
                </p>
              </div>

            </div>
          </div>

        </div>
      )}
    </div>
  );
}

export default FileUpload;