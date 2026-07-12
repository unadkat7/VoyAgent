import mongoose from "mongoose";

const tripSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },

    threadId: {
      type: String,
      required: true,
      index: true,
    },

    promptHistory: [
      {
        type: String,
      },
    ],

    status: {
      type: String,
      enum: ["clarification_needed", "completed", "error"],
      default: "clarification_needed",
    },

    clarification: {
      missing_fields: [
        {
          type: String,
        },
      ],
      question: {
        type: String,
      },
    },

    finalPlan: {
      type: mongoose.Schema.Types.Mixed,
      default: null,
    },
  },
  {
    timestamps: true,
  }
);

const Trip = mongoose.model("Trip", tripSchema);

export default Trip;
