import Link from "next/link";
import { Shield, Search, CheckCircle, Clock, ArrowRight } from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white">Veterans Verify</span>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/auth"
              className="text-gray-300 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/auth?mode=register"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 rounded-full text-blue-300 text-sm mb-8">
            <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            Trusted Verification System
          </div>

          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
            Verify U.S. Military{" "}
            <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
              Veteran Status
            </span>
          </h1>

          <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
            A comprehensive verification system for military veterans.
            Access exclusive benefits from ChatGPT Plus, Spotify, YouTube, and more.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/auth?mode=register"
              className="flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-700 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25"
            >
              Start Verification
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/lookup"
              className="flex items-center gap-2 px-8 py-4 bg-white/10 text-white rounded-xl font-medium hover:bg-white/20 transition-all backdrop-blur-sm"
            >
              <Search className="w-5 h-5" />
              Search VA Records
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="p-8 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10">
            <div className="w-14 h-14 bg-gradient-to-br from-green-400 to-emerald-600 rounded-xl flex items-center justify-center mb-6">
              <CheckCircle className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">
              Instant Verification
            </h3>
            <p className="text-gray-400">
              Verify your veteran status in minutes through SheerID integration
              with the DoD/DEERS database.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="p-8 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10">
            <div className="w-14 h-14 bg-gradient-to-br from-blue-400 to-indigo-600 rounded-xl flex items-center justify-center mb-6">
              <Search className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">
              VA Database Lookup
            </h3>
            <p className="text-gray-400">
              Search public VA databases including Grave Locator, Veterans Legacy
              Memorial, and Army Explorer.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="p-8 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10">
            <div className="w-14 h-14 bg-gradient-to-br from-purple-400 to-pink-600 rounded-xl flex items-center justify-center mb-6">
              <Clock className="w-7 h-7 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-white mb-3">
              Track History
            </h3>
            <p className="text-gray-400">
              Keep track of all your verification requests and their status
              in one centralized dashboard.
            </p>
          </div>
        </div>
      </section>

      {/* Supported Services */}
      <section className="container mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-white text-center mb-12">
          Unlock Benefits From
        </h2>
        <div className="flex flex-wrap items-center justify-center gap-8">
          {[
            { name: "ChatGPT Plus", icon: "🤖" },
            { name: "Spotify Premium", icon: "🎵" },
            { name: "YouTube Premium", icon: "📺" },
            { name: "Google One", icon: "☁️" },
          ].map((service) => (
            <div
              key={service.name}
              className="flex items-center gap-3 px-6 py-4 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10"
            >
              <span className="text-3xl">{service.icon}</span>
              <span className="text-white font-medium">{service.name}</span>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="max-w-4xl mx-auto bg-gradient-to-r from-blue-600 to-indigo-600 rounded-3xl p-12 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Get Verified?
          </h2>
          <p className="text-blue-100 mb-8 max-w-xl mx-auto">
            Join thousands of veterans who have already verified their status
            and unlocked exclusive benefits.
          </p>
          <Link
            href="/auth?mode=register"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-blue-600 rounded-xl font-medium hover:bg-gray-100 transition-all"
          >
            Create Free Account
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-10 border-t border-white/10">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Shield className="w-6 h-6 text-blue-400" />
            <span className="text-gray-400">
              © 2026 Veterans Verify. All rights reserved.
            </span>
          </div>
          <div className="flex items-center gap-6 text-gray-400">
            <Link href="/privacy" className="hover:text-white transition-colors">
              Privacy
            </Link>
            <Link href="/terms" className="hover:text-white transition-colors">
              Terms
            </Link>
            <Link href="/contact" className="hover:text-white transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
