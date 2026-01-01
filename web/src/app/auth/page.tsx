"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { Button, Input, Card, CardContent } from "@/components/ui";
import { Shield, ArrowLeft, Loader2 } from "lucide-react";

function AuthForm() {
    const searchParams = useSearchParams();
    const initialMode = searchParams.get("mode") === "register" ? "register" : "login";
    const [mode, setMode] = useState<"login" | "register">(initialMode);
    const [isLoading, setIsLoading] = useState(false);
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        fullName: "",
        confirmPassword: "",
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 1500));

        // In production, call Supabase auth
        window.location.href = "/dashboard";
    };

    return (
        <>
            {/* Title */}
            <h2 className="text-2xl font-bold text-white text-center mb-2">
                {mode === "login" ? "Welcome Back" : "Create Account"}
            </h2>
            <p className="text-gray-400 text-center mb-8">
                {mode === "login"
                    ? "Sign in to access your dashboard"
                    : "Register to start verifying your status"}
            </p>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
                {mode === "register" && (
                    <Input
                        label="Full Name"
                        type="text"
                        required
                        value={formData.fullName}
                        onChange={(e) =>
                            setFormData({ ...formData, fullName: e.target.value })
                        }
                        placeholder="John Smith"
                        className="bg-white/10 border-white/20 text-white placeholder:text-gray-500"
                    />
                )}

                <Input
                    label="Email Address"
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) =>
                        setFormData({ ...formData, email: e.target.value })
                    }
                    placeholder="john@example.com"
                    className="bg-white/10 border-white/20 text-white placeholder:text-gray-500"
                />

                <Input
                    label="Password"
                    type="password"
                    required
                    value={formData.password}
                    onChange={(e) =>
                        setFormData({ ...formData, password: e.target.value })
                    }
                    placeholder="••••••••"
                    className="bg-white/10 border-white/20 text-white placeholder:text-gray-500"
                />

                {mode === "register" && (
                    <Input
                        label="Confirm Password"
                        type="password"
                        required
                        value={formData.confirmPassword}
                        onChange={(e) =>
                            setFormData({ ...formData, confirmPassword: e.target.value })
                        }
                        placeholder="••••••••"
                        className="bg-white/10 border-white/20 text-white placeholder:text-gray-500"
                    />
                )}

                <Button
                    type="submit"
                    isLoading={isLoading}
                    className="w-full"
                    size="lg"
                >
                    {mode === "login" ? "Sign In" : "Create Account"}
                </Button>
            </form>

            {/* Divider */}
            <div className="my-6 flex items-center gap-4">
                <div className="flex-1 h-px bg-white/20" />
                <span className="text-gray-400 text-sm">or</span>
                <div className="flex-1 h-px bg-white/20" />
            </div>

            {/* Toggle Mode */}
            <p className="text-center text-gray-400">
                {mode === "login" ? (
                    <>
                        Don&apos;t have an account?{" "}
                        <button
                            onClick={() => setMode("register")}
                            className="text-blue-400 hover:text-blue-300 font-medium"
                        >
                            Sign up
                        </button>
                    </>
                ) : (
                    <>
                        Already have an account?{" "}
                        <button
                            onClick={() => setMode("login")}
                            className="text-blue-400 hover:text-blue-300 font-medium"
                        >
                            Sign in
                        </button>
                    </>
                )}
            </p>
        </>
    );
}

function AuthFormLoading() {
    return (
        <div className="flex items-center justify-center py-12">
            <Loader2 className="w-8 h-8 text-blue-400 animate-spin" />
        </div>
    );
}

export default function AuthPage() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 flex items-center justify-center p-6">
            <div className="w-full max-w-md">
                {/* Back to Home */}
                <Link
                    href="/"
                    className="inline-flex items-center gap-2 text-gray-300 hover:text-white transition-colors mb-8"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Home
                </Link>

                <Card className="bg-white/10 backdrop-blur-lg border-white/20">
                    <CardContent className="p-8">
                        {/* Logo */}
                        <div className="flex items-center justify-center gap-3 mb-8">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                                <Shield className="w-7 h-7 text-white" />
                            </div>
                            <div>
                                <h1 className="text-xl font-bold text-white">Veterans Verify</h1>
                                <p className="text-xs text-gray-400">Verification System</p>
                            </div>
                        </div>

                        <Suspense fallback={<AuthFormLoading />}>
                            <AuthForm />
                        </Suspense>
                    </CardContent>
                </Card>

                {/* Footer */}
                <p className="text-center text-gray-500 text-sm mt-8">
                    By continuing, you agree to our{" "}
                    <Link href="/terms" className="text-gray-400 hover:text-white">
                        Terms of Service
                    </Link>{" "}
                    and{" "}
                    <Link href="/privacy" className="text-gray-400 hover:text-white">
                        Privacy Policy
                    </Link>
                </p>
            </div>
        </div>
    );
}
