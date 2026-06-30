"use client";

import { motion } from "framer-motion";
import {
  Sparkles, MapPin, Globe, Compass, Star, Calendar, Camera, Sun,
  Wallet, ArrowRight, Zap, Shield, Lightbulb, Send, Clock, Backpack,
  CheckCircle, Layers, Target, TrendingUp, Play, Users,
} from "lucide-react";
import Button from "@/components/ui/Button";
import {
  Card, CardHeader, CardTitle, CardDescription, CardContent,
} from "@/components/ui/Card";
import Section from "@/components/ui/Section";

/* ============================================
   DATA
   ============================================ */

const FLOATING_ICONS = [
  { Icon: MapPin, className: "top-[12%] left-[7%]", delay: 0 },
  { Icon: Globe, className: "top-[18%] right-[9%]", delay: 1.2 },
  { Icon: Compass, className: "bottom-[28%] left-[5%]", delay: 0.6 },
  { Icon: Star, className: "top-[8%] left-[42%]", delay: 1.8 },
  { Icon: Calendar, className: "bottom-[22%] right-[7%]", delay: 0.3 },
  { Icon: Camera, className: "top-[38%] right-[4%]", delay: 2.2 },
  { Icon: Sun, className: "bottom-[12%] left-[14%]", delay: 1.5 },
  { Icon: Wallet, className: "top-[32%] left-[3%]", delay: 0.9 },
];

const STATS = [
  { value: "10,000+", label: "Trips Planned", icon: MapPin },
  { value: "150+", label: "Destinations", icon: Globe },
  { value: "4.9/5", label: "User Rating", icon: Star },
  { value: "<30s", label: "Generation Time", icon: Zap },
];

const FEATURES = [
  {
    icon: Sparkles,
    title: "AI-Powered Itineraries",
    description: "Our AI agents research destinations, analyze preferences, and craft detailed day-by-day travel plans unique to you.",
    featured: true,
  },
  {
    icon: Wallet,
    title: "Smart Budget Estimation",
    description: "Get realistic cost breakdowns including accommodation, food, transport, and activities.",
  },
  {
    icon: Backpack,
    title: "Packing Intelligence",
    description: "AI-generated packing lists based on your destination, weather, and trip activities.",
  },
  {
    icon: Lightbulb,
    title: "Insider Travel Tips",
    description: "Local recommendations, hidden gems, and practical advice from AI analysis.",
  },
  {
    icon: Zap,
    title: "Instant Generation",
    description: "Describe your dream trip in plain English — get a complete plan in under 30 seconds.",
  },
  {
    icon: Shield,
    title: "Save & Revisit",
    description: "All your generated itineraries are saved securely. Access them anytime, anywhere.",
  },
];

const STEPS = [
  {
    num: "01",
    icon: Send,
    title: "Describe Your Trip",
    description: "Tell VoyAgent where you want to go, your budget, travel dates, group size, and what you love doing.",
    color: "text-primary-light",
    bg: "bg-primary/10",
  },
  {
    num: "02",
    icon: Sparkles,
    title: "AI Agents Plan Everything",
    description: "Our intelligent agents research your destination, plan each day, estimate costs, and prepare packing lists.",
    color: "text-violet-light",
    bg: "bg-violet/10",
  },
  {
    num: "03",
    icon: Globe,
    title: "Travel with Confidence",
    description: "Review your personalized itinerary, save it to your dashboard, and enjoy a perfectly organized trip.",
    color: "text-accent-light",
    bg: "bg-accent/10",
  },
];

const WHY_POINTS = [
  { icon: Layers, text: "Multi-agent architecture — not a simple chatbot" },
  { icon: Target, text: "Every itinerary is personalized to your style" },
  { icon: TrendingUp, text: "Budget, packing, and tips — all in one plan" },
  { icon: Shield, text: "Your trips are saved securely forever" },
];

const AGENT_PIPELINE = [
  { label: "Research Agent", description: "Analyzes your destination" },
  { label: "Planning Agent", description: "Crafts day-by-day itinerary" },
  { label: "Budget Agent", description: "Estimates realistic costs" },
  { label: "Tips Agent", description: "Adds local insights & packing" },
];

/* ============================================
   ANIMATION HELPERS
   ============================================ */

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5, ease: "easeOut" },
  }),
};

const stagger = {
  visible: { transition: { staggerChildren: 0.1 } },
};

/* ============================================
   HERO SECTION
   ============================================ */

function HeroSection() {
  return (
    <section className="relative min-h-[92vh] flex items-center justify-center glow-bg dot-grid overflow-hidden">
      {/* Gradient Orbs */}
      <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full bg-primary/8 blur-[120px] animate-orb" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-violet/6 blur-[100px] animate-orb" style={{ animationDelay: "-8s" }} />
      <div className="absolute top-1/2 left-1/2 w-[300px] h-[300px] rounded-full bg-accent/5 blur-[80px] animate-orb" style={{ animationDelay: "-15s" }} />

      {/* Floating Travel Icons */}
      {FLOATING_ICONS.map(({ Icon, className, delay }, i) => (
        <motion.div
          key={i}
          animate={{ y: [0, -16, 0] }}
          transition={{ duration: 5 + i * 0.5, repeat: Infinity, ease: "easeInOut", delay }}
          className={`absolute hidden lg:block ${className}`}
        >
          <div className="p-3 rounded-2xl glass opacity-50 hover:opacity-90 transition-opacity duration-300">
            <Icon className="h-5 w-5 text-primary-light/70" />
          </div>
        </motion.div>
      ))}

      {/* Hero Content */}
      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 text-center py-20">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold tracking-widest uppercase rounded-full bg-primary/10 text-primary-light border border-primary/20">
            <Sparkles className="h-3.5 w-3.5" />
            Powered by Intelligent AI Agents
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.15 }}
          className="mt-8 text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1]"
        >
          Your Intelligent{" "}
          <span className="text-gradient">AI Travel Concierge</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.25 }}
          className="mt-6 text-lg sm:text-xl text-muted max-w-2xl mx-auto leading-relaxed"
        >
          Describe your dream trip in plain English. Our AI agents research destinations,
          craft personalized itineraries, estimate budgets, and pack your bags — all in seconds.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.35 }}
          className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <Button variant="primary" size="lg">
            Start Planning — It&apos;s Free
            <ArrowRight className="h-5 w-5" />
          </Button>
          <Button variant="outline" size="lg">
            <Play className="h-4 w-4" />
            Watch Demo
          </Button>
        </motion.div>

        {/* Trust Badges */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="mt-10 flex items-center justify-center gap-6 sm:gap-8 text-xs text-muted flex-wrap"
        >
          <span className="flex items-center gap-1.5">
            <CheckCircle className="h-3.5 w-3.5 text-green-400" />
            No credit card required
          </span>
          <span className="flex items-center gap-1.5">
            <Clock className="h-3.5 w-3.5" />
            Results in seconds
          </span>
          <span className="flex items-center gap-1.5">
            <Users className="h-3.5 w-3.5" />
            10,000+ happy travelers
          </span>
        </motion.div>
      </div>
    </section>
  );
}

/* ============================================
   STATS BAR
   ============================================ */

function StatsBar() {
  return (
    <div className="relative z-10 -mt-12 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="max-w-4xl mx-auto glass rounded-2xl p-6 sm:p-8"
      >
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-8">
          {STATS.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="flex items-center justify-center gap-2 mb-1">
                <stat.icon className="h-4 w-4 text-primary-light" />
                <span className="text-2xl sm:text-3xl font-bold text-foreground">{stat.value}</span>
              </div>
              <p className="text-xs sm:text-sm text-muted">{stat.label}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}

/* ============================================
   FEATURES SECTION
   ============================================ */

function FeaturesSection() {
  return (
    <Section
      id="features"
      badge="Core Features"
      title="Everything You Need to Travel Smarter"
      subtitle="VoyAgent combines intelligent AI agents with thoughtful design to make travel planning effortless and enjoyable."
    >
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {FEATURES.map((feature, index) => (
          <motion.div
            key={feature.title}
            variants={fadeUp}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-50px" }}
            custom={index}
            className={feature.featured ? "sm:col-span-2 lg:col-span-1" : ""}
          >
            <Card className="h-full">
              <CardContent className="p-6 sm:p-7">
                <div className="p-3 rounded-xl bg-primary/10 w-fit mb-4 border border-primary/10">
                  <feature.icon className="h-6 w-6 text-primary-light" />
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
                <p className="text-sm text-muted leading-relaxed">{feature.description}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </Section>
  );
}

/* ============================================
   HOW IT WORKS SECTION
   ============================================ */

function HowItWorksSection() {
  return (
    <Section
      id="how-it-works"
      badge="How It Works"
      title="From Idea to Itinerary in Three Steps"
      subtitle="No forms, no endless browsing. Just describe your dream trip and let our AI agents handle the rest."
      className="bg-surface/30"
    >
      <div className="relative max-w-5xl mx-auto">
        {/* Connecting line (desktop) */}
        <div className="hidden md:block absolute top-[72px] left-[16%] right-[16%] h-px bg-gradient-to-r from-primary/40 via-violet/40 to-accent/40" />

        <div className="grid md:grid-cols-3 gap-10 md:gap-8">
          {STEPS.map((step, index) => (
            <motion.div
              key={step.num}
              variants={fadeUp}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true, margin: "-50px" }}
              custom={index}
              className="text-center relative"
            >
              {/* Step icon with number badge */}
              <div className="relative inline-flex items-center justify-center mb-6">
                <div className={`p-5 rounded-2xl ${step.bg} border border-white/5`}>
                  <step.icon className={`h-8 w-8 ${step.color}`} />
                </div>
                <span className="absolute -top-2 -right-2 h-8 w-8 rounded-full bg-gradient-to-br from-primary to-violet text-white text-xs font-bold flex items-center justify-center shadow-lg shadow-primary/30">
                  {step.num}
                </span>
              </div>

              <h3 className="text-xl font-semibold text-foreground mb-3">{step.title}</h3>
              <p className="text-sm text-muted leading-relaxed max-w-xs mx-auto">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </Section>
  );
}

/* ============================================
   WHY VOYAGENT SECTION
   ============================================ */

function WhySection() {
  return (
    <section id="why" className="py-20 md:py-28 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        {/* Left — Content */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6 }}
        >
          <span className="inline-flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold tracking-widest uppercase rounded-full bg-violet/10 text-violet-light border border-violet/20 mb-5">
            Why VoyAgent
          </span>

          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight leading-tight">
            Not Just Another{" "}
            <span className="text-gradient">Travel App</span>
          </h2>

          <p className="mt-5 text-muted text-lg leading-relaxed">
            VoyAgent is built on an agentic AI architecture. Instead of simple templates,
            our intelligent agents collaborate to research, plan, budget, and personalize
            every trip — just like a human travel concierge, but faster.
          </p>

          <div className="mt-8 space-y-4">
            {WHY_POINTS.map((point, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -15 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.4 }}
                className="flex items-center gap-3"
              >
                <div className="p-2 rounded-lg bg-primary/10 shrink-0">
                  <point.icon className="h-4 w-4 text-primary-light" />
                </div>
                <span className="text-sm text-muted">{point.text}</span>
              </motion.div>
            ))}
          </div>

          <div className="mt-8">
            <Button variant="primary" size="lg">
              Try VoyAgent Now
              <ArrowRight className="h-5 w-5" />
            </Button>
          </div>
        </motion.div>

        {/* Right — Agent Pipeline Visual */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true, margin: "-80px" }}
          transition={{ duration: 0.6, delay: 0.15 }}
        >
          <div className="glass rounded-3xl p-6 sm:p-8 border border-border relative overflow-hidden">
            {/* Background glow */}
            <div className="absolute top-0 right-0 w-40 h-40 bg-primary/10 rounded-full blur-[60px]" />
            <div className="absolute bottom-0 left-0 w-32 h-32 bg-violet/8 rounded-full blur-[50px]" />

            <div className="relative z-10">
              {/* Input prompt */}
              <div className="rounded-xl bg-surface-light/80 border border-border p-4 mb-6">
                <p className="text-xs text-muted mb-1 font-medium">Your Request</p>
                <p className="text-sm text-foreground italic">
                  &quot;Plan a 4-day trip to Goa under ₹35,000 for two people. We love beaches and cafés.&quot;
                </p>
              </div>

              {/* Agent Pipeline */}
              <div className="space-y-3">
                {AGENT_PIPELINE.map((agent, i) => (
                  <motion.div
                    key={agent.label}
                    initial={{ opacity: 0, y: 10 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: 0.3 + i * 0.12 }}
                    className="flex items-center gap-3 p-3 rounded-xl bg-white/[0.03] border border-white/[0.05] hover:border-primary/20 transition-colors duration-200"
                  >
                    <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-primary to-violet flex items-center justify-center shrink-0">
                      <Sparkles className="h-4 w-4 text-white" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-foreground">{agent.label}</p>
                      <p className="text-xs text-muted">{agent.description}</p>
                    </div>
                    <CheckCircle className="h-4 w-4 text-green-400 shrink-0 ml-auto" />
                  </motion.div>
                ))}
              </div>

              {/* Output */}
              <div className="mt-6 rounded-xl bg-gradient-to-r from-primary/10 to-violet/10 border border-primary/20 p-4 text-center">
                <Sparkles className="h-5 w-5 text-primary-light mx-auto mb-2" />
                <p className="text-sm font-semibold text-foreground">Your Personalized Itinerary</p>
                <p className="text-xs text-muted mt-1">Complete with budget, packing list & travel tips</p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

/* ============================================
   CTA SECTION
   ============================================ */

function CTASection() {
  return (
    <section className="py-20 md:py-28 px-4 sm:px-6 lg:px-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
        className="max-w-4xl mx-auto text-center rounded-3xl p-10 md:p-16 relative overflow-hidden"
      >
        {/* Background layers */}
        <div className="absolute inset-0 glass rounded-3xl" />
        <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-violet/10 rounded-3xl" />
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[250px] bg-primary/8 rounded-full blur-[100px]" />

        <div className="relative z-10">
          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
          >
            <Compass className="h-12 w-12 text-primary-light mx-auto mb-6" />
          </motion.div>

          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-gradient leading-tight">
            Ready to Plan Your Next Adventure?
          </h2>
          <p className="mt-5 text-muted text-lg max-w-xl mx-auto leading-relaxed">
            Join thousands of travelers who plan smarter with VoyAgent.
            Your AI concierge is ready — no signup required to try.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button variant="primary" size="lg">
              Start Planning — It&apos;s Free
              <ArrowRight className="h-5 w-5" />
            </Button>
            <Button variant="secondary" size="lg">
              View Sample Itinerary
            </Button>
          </div>

          <p className="mt-6 text-xs text-muted flex items-center justify-center gap-1.5">
            <Shield className="h-3.5 w-3.5" />
            Free forever for basic usage. No credit card needed.
          </p>
        </div>
      </motion.div>
    </section>
  );
}

/* ============================================
   PAGE — Main Export
   ============================================ */

export default function Home() {
  return (
    <>
      <HeroSection />
      <StatsBar />
      <FeaturesSection />
      <HowItWorksSection />
      <WhySection />
      <CTASection />
    </>
  );
}
