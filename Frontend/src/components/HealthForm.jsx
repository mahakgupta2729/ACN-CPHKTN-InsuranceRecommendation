import React, { useState, useRef } from "react";
import axios from "axios";
import { Loader2, FileText } from "lucide-react";

const MAX_FILE_SIZE_MB = 5;

const HealthForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    gender: "Female",
    conditions: "",
  });

  const [file, setFile] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [recommendation, setRecommendation] = useState("");
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false;
    const isTooLarge = selectedFile.size > MAX_FILE_SIZE_MB * 1024 * 1024;
    if (isTooLarge) {
      setError(`File size exceeds ${MAX_FILE_SIZE_MB}MB limit.`);
      return false;
    }
    return true;
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (validateFile(selectedFile)) {
      setFile(selectedFile);
      setError("");
    } else {
      setFile(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (validateFile(droppedFile)) {
      setFile(droppedFile);
      setError("");
    }
  };

  const handleDragOver = (e) => e.preventDefault();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError("Please upload a valid PDF report.");
      return;
    }

    const data = new FormData();
    data.append("file", file);
    Object.entries(formData).forEach(([key, value]) =>
      data.append(key, value)
    );

    try {
      setIsSubmitting(true);
      setError("");
      setRecommendation("");
      const response = await axios.post("http://localhost:5000/recommend", data);
      setRecommendation(response.data.recommendation || "No recommendation received.");
    } catch (err) {
      console.error(err);
      setError("Submission failed. Please try again later.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-8 rounded-2xl shadow-lg">
      <h1 className="text-3xl font-semibold mb-6 text-gray-800">
        Health Insurance Recommendation
      </h1>

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-600">Full Name</label>
          <input
            id="name"
            name="name"
            required
            className="mt-1 w-full border border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={formData.name}
            onChange={handleChange}
          />
        </div>

        <div>
          <label htmlFor="age" className="block text-sm font-medium text-gray-600">Age</label>
          <input
            id="age"
            type="number"
            name="age"
            required
            className="mt-1 w-full border border-gray-300 p-3 rounded-lg shadow-sm"
            value={formData.age}
            onChange={handleChange}
          />
        </div>

        <div>
          <label htmlFor="gender" className="block text-sm font-medium text-gray-600">Gender</label>
          <select
            id="gender"
            name="gender"
            className="mt-1 w-full border border-gray-300 p-3 rounded-lg shadow-sm"
            value={formData.gender}
            onChange={handleChange}
          >
            <option value="Female">Female</option>
            <option value="Male">Male</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div>
          <label htmlFor="conditions" className="block text-sm font-medium text-gray-600">
            Medical Conditions
          </label>
          <input
            id="conditions"
            type="text"
            name="conditions"
            required
            className="mt-1 w-full border border-gray-300 p-3 rounded-lg shadow-sm"
            value={formData.conditions}
            onChange={handleChange}
            placeholder="e.g., diabetes, asthma"
          />
        </div>

        {/* Drag-and-Drop Upload */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="flex items-center justify-center border-2 border-dashed border-blue-400 bg-blue-50 hover:bg-blue-100 transition p-6 rounded-xl cursor-pointer"
          onClick={() => fileInputRef.current.click()}
        >
          {file ? (
            <div className="flex items-center space-x-2 text-blue-700 font-medium">
              <FileText size={20} />
              <span>{file.name}</span>
              <button
                type="button"
                className="ml-4 text-red-500 text-sm underline"
                onClick={(e) => {
                  e.stopPropagation();
                  setFile(null);
                }}
              >
                Remove
              </button>
            </div>
          ) : (
            <p className="text-blue-600">Drag & drop a PDF file here or click to browse</p>
          )}
          <input
            type="file"
            accept=".pdf"
            ref={fileInputRef}
            className="hidden"
            onChange={handleFileSelect}
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition flex items-center justify-center"
          disabled={isSubmitting}
        >
          {isSubmitting ? (
            <>
              <Loader2 className="animate-spin mr-2" size={20} /> Submitting...
            </>
          ) : (
            "Get Recommendation"
          )}
        </button>
      </form>

      {recommendation && (
        <div className="mt-6 p-4 bg-green-100 text-green-800 rounded-lg border border-green-300">
          <strong>Recommendation:</strong> {recommendation}
        </div>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-100 text-red-700 rounded-lg border border-red-300">
          <strong>Error:</strong> {error}
        </div>
      )}
    </div>
  );
};

export default HealthForm;
