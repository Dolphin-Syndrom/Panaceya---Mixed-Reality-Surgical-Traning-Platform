'use client'

import { motion, Variants } from 'framer-motion'
import { 
  Brain, 
  Heart, 
  Zap, 
  Award, 
  Users, 
  Globe, 
  Activity,
  Sparkles,
  ChevronRight,
  Play
} from 'lucide-react'

export default function Home() {
  const fadeInUp: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  const staggerContainer: Variants = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  return (
    <main className="min-h-screen overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-medical-blue via-white to-purple-50" />
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-tech-purple/20 rounded-full blur-3xl animate-pulse-slow delay-1000" />
      </div>

      {/* Navigation */}
      <motion.nav 
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="fixed top-0 left-0 right-0 z-50 glass-morphism"
      >
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-primary">Panaceya</span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-700 hover:text-primary transition-colors">Features</a>
            <a href="#about" className="text-gray-700 hover:text-primary transition-colors">About</a>
            <a href="#contact" className="text-gray-700 hover:text-primary transition-colors">Contact</a>
            <button className="px-6 py-2 medical-gradient text-white rounded-full hover:opacity-90 transition-opacity">
              Get Started
            </button>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-6 pt-20">
        <div className="max-w-7xl mx-auto grid md:grid-cols-2 gap-12 items-center">
          <motion.div
            initial="initial"
            animate="animate"
            variants={staggerContainer}
          >
            <motion.h1 
              variants={fadeInUp}
              className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
            >
              Democratizing{' '}
              <span className="text-primary">Surgical Excellence</span>
            </motion.h1>

            <motion.p 
              variants={fadeInUp}
              className="text-xl text-gray-600 mb-8 leading-relaxed"
            >
              "Every surgeon deserves world-class training. Every patient deserves a surgeon who's practiced perfection."
            </motion.p>

            <motion.p
              variants={fadeInUp}
              className="text-lg text-gray-500 mb-8"
            >
              Experience the future of surgical training with AI-powered multi-agent coaching, realistic physics simulation, and gamified learning that makes excellence accessible to all.
            </motion.p>

            <motion.div 
              variants={fadeInUp}
              className="flex flex-wrap gap-4"
            >
              <button className="group px-8 py-4 medical-gradient text-white rounded-full font-semibold hover:shadow-2xl transition-all flex items-center space-x-2">
                <Play className="w-5 h-5" />
                <span>Get Started</span>
                <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="px-8 py-4 glass-morphism rounded-full font-semibold hover:shadow-xl transition-all">
                View Documentation
              </button>
            </motion.div>
          </motion.div>

          {/* 3D Illustration Placeholder */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="glass-morphism rounded-3xl p-8 animate-float">
              <div className="aspect-square rounded-2xl flex items-center justify-center relative overflow-hidden">
                <img 
                  src="panaceya.png" 
                  alt="Surgical Training Visualization" 
                  className="w-full h-full object-cover rounded-2xl"
                />
              </div>
              
              {/* Floating Cards */}
              <motion.div 
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
                className="absolute -right-4 top-20 glass-morphism p-4 rounded-2xl shadow-xl"
              >
                <Activity className="w-6 h-6 text-primary mb-2" />
                <p className="text-xs font-semibold">Real-time AI Feedback</p>
              </motion.div>

              <motion.div 
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 3, repeat: Infinity, delay: 1 }}
                className="absolute -left-4 bottom-20 glass-morphism p-4 rounded-2xl shadow-xl"
              >
                <Zap className="w-6 h-6 text-tech-purple mb-2" />
                <p className="text-xs font-semibold">SOFA Physics Engine</p>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Revolutionizing <span className="text-primary">Surgical Training</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Combining cutting-edge AI, realistic physics, and gamification for unparalleled learning experiences
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Brain,
                title: 'Multi-Agent AI Coaching',
                description: 'LangGraph-orchestrated agents analyze technique, monitor safety, and provide personalized learning paths in real-time.',
                color: 'text-primary'
              },
              {
                icon: Zap,
                title: 'Realistic Physics Simulation',
                description: 'SOFA framework delivers surgical-grade tissue deformation, collision detection, and force feedback for authentic training.',
                color: 'text-tech-purple'
              },
              {
                icon: Award,
                title: 'Gamified Learning',
                description: 'Progress through levels, earn achievements, and compete on leaderboards while mastering surgical procedures.',
                color: 'text-primary'
              },
              {
                icon: Users,
                title: 'Collaborative Environment',
                description: 'Train with peers globally, share techniques, and learn from expert surgeons through our connected platform.',
                color: 'text-tech-purple'
              },
              {
                icon: Globe,
                title: 'Accessible Worldwide',
                description: 'Cloud-based platform brings world-class surgical training to medical professionals anywhere, anytime.',
                color: 'text-primary'
              },
              {
                icon: Activity,
                title: 'Performance Analytics',
                description: 'Track your progress with detailed metrics, AI-generated insights, and adaptive difficulty adjustment.',
                color: 'text-tech-purple'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -10 }}
                className="glass-morphism rounded-2xl p-8 hover:shadow-2xl transition-all cursor-pointer group"
              >
                <feature.icon className={`w-12 h-12 ${feature.color} mb-4 group-hover:scale-110 transition-transform`} />
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-5xl mx-auto glass-morphism-dark rounded-3xl p-12 text-center relative overflow-hidden"
        >
          <div className="absolute inset-0 medical-gradient opacity-10" />
          <div className="relative z-10">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Transform Your <span className="text-primary">Surgical Skills?</span>
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Experience the next generation of surgical training powered by AI and realistic physics simulation. Your journey to excellence starts here.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <button className="px-8 py-4 medical-gradient text-white rounded-full font-semibold hover:shadow-2xl transition-all">
                Get Started
              </button>
              <button className="px-8 py-4 glass-morphism rounded-full font-semibold hover:shadow-xl transition-all">
                View Documentation
              </button>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-gray-200">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <span className="text-xl font-bold text-primary">Panaceya</span>
            </div>
            <p className="text-gray-500 text-sm">
              © 2026 Panaceya. Democratizing surgical excellence, one procedure at a time.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
