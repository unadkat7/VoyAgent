import axios from "axios";
import Trip from "../models/trip.model.js";

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || "http://localhost:8000";

// ============================================================
// PLAN TRIP REQUEST
// ============================================================
export const planTrip = async (req, res) => {
  try {
    const { prompt, threadId: providedThreadId } = req.body;

    if (!prompt) {
      return res.status(400).json({
        success: false,
        message: "Prompt is required",
      });
    }

    const userId = req.user._id;
    const threadId = providedThreadId || `${userId}_trip_${Date.now()}`;

    console.log(`📡 Forwarding prompt to AI Service [threadId: ${threadId}]...`);

    // Call FastAPI AI microservice
    const aiResponse = await axios.post(`${AI_SERVICE_URL}/planner/plan-trip`, {
      prompt,
      thread_id: threadId,
    });

    const aiData = aiResponse.data;

    // Find existing trip session or initialize a new one
    let trip = await Trip.findOne({ userId, threadId });

    if (!trip) {
      trip = new Trip({
        userId,
        threadId,
        promptHistory: [prompt],
      });
    } else {
      trip.promptHistory.push(prompt);
    }

    if (aiData.status === "clarification_needed") {
      trip.status = "clarification_needed";
      trip.clarification = {
        missing_fields: aiData.clarification?.missing_fields || [],
        question: aiData.clarification?.question || "Please provide more details.",
      };
      trip.finalPlan = null;
      await trip.save();

      return res.status(200).json({
        success: true,
        status: "clarification_needed",
        threadId,
        clarification: trip.clarification,
      });
    }

    if (aiData.status === "completed") {
      trip.status = "completed";
      trip.clarification = {
        missing_fields: [],
        question: null,
      };
      trip.finalPlan = aiData.final_plan;
      await trip.save();

      return res.status(200).json({
        success: true,
        status: "completed",
        threadId,
        trip,
      });
    }

    return res.status(500).json({
      success: false,
      message: "Unknown status returned from AI Service",
    });
  } catch (error) {
    console.error("❌ Error in planTrip controller:", error?.response?.data || error.message);
    return res.status(500).json({
      success: false,
      message: error?.response?.data?.detail || "Failed to process travel planning request with AI Service.",
    });
  }
};

// ============================================================
// GET USER TRIPS
// ============================================================
export const getUserTrips = async (req, res) => {
  try {
    const trips = await Trip.find({ userId: req.user._id }).sort({ createdAt: -1 });

    return res.status(200).json({
      success: true,
      count: trips.length,
      trips,
    });
  } catch (error) {
    console.error("❌ Error in getUserTrips controller:", error.message);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch user trips.",
    });
  }
};

// ============================================================
// GET TRIP BY ID
// ============================================================
export const getTripById = async (req, res) => {
  try {
    const { id } = req.params;
    const trip = await Trip.findById(id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: "Trip not found",
      });
    }

    if (trip.userId.toString() !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: "Not authorized to access this trip",
      });
    }

    return res.status(200).json({
      success: true,
      trip,
    });
  } catch (error) {
    console.error("❌ Error in getTripById controller:", error.message);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch trip details.",
    });
  }
};

// ============================================================
// DELETE TRIP
// ============================================================
export const deleteTrip = async (req, res) => {
  try {
    const { id } = req.params;
    const trip = await Trip.findById(id);

    if (!trip) {
      return res.status(404).json({
        success: false,
        message: "Trip not found",
      });
    }

    if (trip.userId.toString() !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: "Not authorized to delete this trip",
      });
    }

    await Trip.findByIdAndDelete(id);

    return res.status(200).json({
      success: true,
      message: "Trip deleted successfully",
    });
  } catch (error) {
    console.error("❌ Error in deleteTrip controller:", error.message);
    return res.status(500).json({
      success: false,
      message: "Failed to delete trip.",
    });
  }
};
