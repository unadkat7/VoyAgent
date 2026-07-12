import express from "express";
import {
  planTrip,
  getUserTrips,
  getTripById,
  deleteTrip,
} from "../controllers/trip.controller.js";
import protect from "../middleware/auth.middleware.js";

const router = express.Router();

router.post("/plan", protect, planTrip);
router.get("/", protect, getUserTrips);
router.get("/:id", protect, getTripById);
router.delete("/:id", protect, deleteTrip);

export default router;
