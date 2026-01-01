"use client";

import { useState } from "react";
import { Header } from "@/components/layout";
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CardDescription,
    Button,
    Input,
    Select,
} from "@/components/ui";
import { MILITARY_BRANCHES, SERVICE_TYPES, MilitaryBranch, ServiceType } from "@/types";
import { Shield, CheckCircle, ArrowRight, ArrowLeft, Upload, Loader2 } from "lucide-react";

type Step = "service" | "info" | "submit" | "result";

export default function VerifyPage() {
    const [step, setStep] = useState<Step>("service");
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<{
        status: "approved" | "processing" | "document_required" | "error";
        message: string;
    } | null>(null);

    // Form state
    const [serviceType, setServiceType] = useState<ServiceType>("chatgpt");
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        email: "",
        birthDate: "",
        branch: "" as MilitaryBranch | "",
        militaryStatus: "VETERAN",
        dischargeDate: "",
    });

    const handleSubmit = async () => {
        setIsLoading(true);

        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 2000));

        // Mock result
        setResult({
            status: "approved",
            message: "Your veteran status has been verified successfully!",
        });
        setStep("result");
        setIsLoading(false);
    };

    const renderStep = () => {
        switch (step) {
            case "service":
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                Select Service
                            </h2>
                            <p className="text-gray-500 dark:text-gray-400">
                                Choose the service you want to verify for
                            </p>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {SERVICE_TYPES.map((service) => (
                                <button
                                    key={service.value}
                                    onClick={() => setServiceType(service.value)}
                                    className={`p-6 rounded-xl border-2 text-left transition-all ${serviceType === service.value
                                            ? "border-blue-500 bg-blue-50 dark:bg-blue-900/20"
                                            : "border-gray-200 dark:border-gray-700 hover:border-gray-300"
                                        }`}
                                >
                                    <span className="text-3xl">{service.icon}</span>
                                    <h3 className="mt-3 font-semibold text-gray-900 dark:text-white">
                                        {service.label}
                                    </h3>
                                    <p className="text-sm text-gray-500 dark:text-gray-400">
                                        Verify for {service.label} discount
                                    </p>
                                </button>
                            ))}
                        </div>

                        <div className="flex justify-end">
                            <Button onClick={() => setStep("info")}>
                                Continue
                                <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>
                        </div>
                    </div>
                );

            case "info":
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                Personal Information
                            </h2>
                            <p className="text-gray-500 dark:text-gray-400">
                                Enter your military service details
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <Input
                                label="First Name"
                                required
                                value={formData.firstName}
                                onChange={(e) =>
                                    setFormData({ ...formData, firstName: e.target.value })
                                }
                                placeholder="John"
                            />
                            <Input
                                label="Last Name"
                                required
                                value={formData.lastName}
                                onChange={(e) =>
                                    setFormData({ ...formData, lastName: e.target.value })
                                }
                                placeholder="Smith"
                            />
                            <Input
                                label="Email Address"
                                type="email"
                                required
                                value={formData.email}
                                onChange={(e) =>
                                    setFormData({ ...formData, email: e.target.value })
                                }
                                placeholder="john.smith@email.com"
                            />
                            <Input
                                label="Date of Birth"
                                type="date"
                                required
                                value={formData.birthDate}
                                onChange={(e) =>
                                    setFormData({ ...formData, birthDate: e.target.value })
                                }
                            />
                            <Select
                                label="Military Branch"
                                required
                                value={formData.branch}
                                onChange={(e) =>
                                    setFormData({
                                        ...formData,
                                        branch: e.target.value as MilitaryBranch,
                                    })
                                }
                                options={MILITARY_BRANCHES}
                                placeholder="Select branch..."
                            />
                            <Select
                                label="Military Status"
                                required
                                value={formData.militaryStatus}
                                onChange={(e) =>
                                    setFormData({ ...formData, militaryStatus: e.target.value })
                                }
                                options={[
                                    { value: "VETERAN", label: "Veteran" },
                                    { value: "ACTIVE_DUTY", label: "Active Duty" },
                                    { value: "RESERVE", label: "Reserve" },
                                    { value: "RETIRED", label: "Retired" },
                                ]}
                            />
                            <Input
                                label="Discharge Date"
                                type="date"
                                value={formData.dischargeDate}
                                onChange={(e) =>
                                    setFormData({ ...formData, dischargeDate: e.target.value })
                                }
                                helperText="Required for Veterans"
                            />
                        </div>

                        <div className="flex justify-between">
                            <Button variant="outline" onClick={() => setStep("service")}>
                                <ArrowLeft className="w-4 h-4 mr-2" />
                                Back
                            </Button>
                            <Button onClick={() => setStep("submit")}>
                                Continue
                                <ArrowRight className="w-4 h-4 ml-2" />
                            </Button>
                        </div>
                    </div>
                );

            case "submit":
                return (
                    <div className="space-y-6">
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                Review & Submit
                            </h2>
                            <p className="text-gray-500 dark:text-gray-400">
                                Verify your information and submit for verification
                            </p>
                        </div>

                        <Card className="bg-gray-50 dark:bg-gray-800/50">
                            <CardContent className="p-6">
                                <h3 className="font-medium text-gray-900 dark:text-white mb-4">
                                    Verification Summary
                                </h3>
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div>
                                        <span className="text-gray-500">Service:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {SERVICE_TYPES.find((s) => s.value === serviceType)?.label}
                                        </p>
                                    </div>
                                    <div>
                                        <span className="text-gray-500">Name:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {formData.firstName} {formData.lastName}
                                        </p>
                                    </div>
                                    <div>
                                        <span className="text-gray-500">Email:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {formData.email}
                                        </p>
                                    </div>
                                    <div>
                                        <span className="text-gray-500">Branch:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {formData.branch}
                                        </p>
                                    </div>
                                    <div>
                                        <span className="text-gray-500">Status:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {formData.militaryStatus}
                                        </p>
                                    </div>
                                    <div>
                                        <span className="text-gray-500">Birth Date:</span>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {formData.birthDate}
                                        </p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                            <p className="text-sm text-blue-800 dark:text-blue-300">
                                <strong>Note:</strong> Your information will be verified against the
                                DoD/DEERS database through SheerID. This typically takes a few seconds
                                but may require document upload if automatic verification fails.
                            </p>
                        </div>

                        <div className="flex justify-between">
                            <Button variant="outline" onClick={() => setStep("info")}>
                                <ArrowLeft className="w-4 h-4 mr-2" />
                                Back
                            </Button>
                            <Button onClick={handleSubmit} isLoading={isLoading}>
                                Submit Verification
                                <Shield className="w-4 h-4 ml-2" />
                            </Button>
                        </div>
                    </div>
                );

            case "result":
                return (
                    <div className="text-center py-12">
                        {result?.status === "approved" ? (
                            <>
                                <div className="w-20 h-20 mx-auto bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mb-6">
                                    <CheckCircle className="w-10 h-10 text-green-600" />
                                </div>
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                    Verification Approved!
                                </h2>
                                <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-md mx-auto">
                                    {result.message}
                                </p>
                            </>
                        ) : result?.status === "document_required" ? (
                            <>
                                <div className="w-20 h-20 mx-auto bg-orange-100 dark:bg-orange-900/20 rounded-full flex items-center justify-center mb-6">
                                    <Upload className="w-10 h-10 text-orange-600" />
                                </div>
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                    Document Required
                                </h2>
                                <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-md mx-auto">
                                    Please upload your DD-214 or Military ID to complete verification.
                                </p>
                                <Button>
                                    Upload Document
                                    <Upload className="w-4 h-4 ml-2" />
                                </Button>
                            </>
                        ) : (
                            <>
                                <div className="w-20 h-20 mx-auto bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mb-6">
                                    <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
                                </div>
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                                    Processing...
                                </h2>
                                <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-md mx-auto">
                                    Your verification is being processed. This may take a few minutes.
                                </p>
                            </>
                        )}

                        <div className="flex justify-center gap-4 mt-8">
                            <Button
                                variant="outline"
                                onClick={() => {
                                    setStep("service");
                                    setResult(null);
                                }}
                            >
                                New Verification
                            </Button>
                            <Button onClick={() => (window.location.href = "/dashboard")}>
                                Go to Dashboard
                            </Button>
                        </div>
                    </div>
                );
        }
    };

    return (
        <>
            <Header
                title="Verify Status"
                description="Verify your military veteran status"
            />

            <div className="p-6">
                {/* Progress Steps */}
                {step !== "result" && (
                    <div className="mb-8">
                        <div className="flex items-center justify-center gap-4">
                            {["service", "info", "submit"].map((s, index) => (
                                <div key={s} className="flex items-center">
                                    <div
                                        className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${step === s
                                                ? "bg-blue-600 text-white"
                                                : ["service", "info", "submit"].indexOf(step) >
                                                    index
                                                    ? "bg-green-500 text-white"
                                                    : "bg-gray-200 dark:bg-gray-700 text-gray-500"
                                            }`}
                                    >
                                        {["service", "info", "submit"].indexOf(step) > index ? (
                                            <CheckCircle className="w-5 h-5" />
                                        ) : (
                                            index + 1
                                        )}
                                    </div>
                                    {index < 2 && (
                                        <div
                                            className={`w-20 h-1 mx-2 ${["service", "info", "submit"].indexOf(step) > index
                                                    ? "bg-green-500"
                                                    : "bg-gray-200 dark:bg-gray-700"
                                                }`}
                                        />
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                <Card className="max-w-3xl mx-auto">
                    <CardContent className="p-8">{renderStep()}</CardContent>
                </Card>
            </div>
        </>
    );
}
