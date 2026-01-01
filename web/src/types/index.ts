// Veterans Verification System - TypeScript Types

// Military Branch enum
export type MilitaryBranch =
    | "Army"
    | "Navy"
    | "Air Force"
    | "Marine Corps"
    | "Coast Guard"
    | "Space Force"
    | "Army National Guard"
    | "Army Reserve"
    | "Air National Guard"
    | "Air Force Reserve"
    | "Navy Reserve"
    | "Marine Corps Reserve"
    | "Coast Guard Reserve";

export type MilitaryStatus = "ACTIVE_DUTY" | "VETERAN" | "RESERVE" | "RETIRED";

export type VerificationStatus =
    | "pending"
    | "processing"
    | "approved"
    | "rejected"
    | "document_required"
    | "error"
    | "expired";

export type ServiceType = "chatgpt" | "spotify" | "youtube" | "google_one" | "other";

export type VASource = "grave_locator" | "vlm" | "army_explorer";

// Veteran types
export interface Veteran {
    id: string;
    firstName: string;
    lastName: string;
    birthDate?: string;
    branch: MilitaryBranch;
    militaryStatus: MilitaryStatus;
    dischargeDate?: string;
    isVerified: boolean;
    source?: string;
    createdAt: string;
}

export interface VeteranCreate {
    firstName: string;
    lastName: string;
    birthDate?: string;
    branch: MilitaryBranch;
    militaryStatus: MilitaryStatus;
    dischargeDate?: string;
}

// Verification types
export interface Verification {
    id: string;
    serviceType: ServiceType;
    status: VerificationStatus;
    veteran?: Veteran;
    sheeridVerificationId?: string;
    createdAt: string;
    submittedAt?: string;
    completedAt?: string;
    errorMessage?: string;
}

export interface CreateVerificationRequest {
    serviceType: ServiceType;
    programId?: string;
}

export interface CreateVerificationResponse {
    verificationId: string;
    sheeridVerificationId?: string;
    status: VerificationStatus;
    createdAt: string;
}

export interface SubmitVerificationRequest {
    verificationId: string;
    veteran: VeteranCreate;
    email: string;
}

export interface SubmitVerificationResponse {
    verificationId: string;
    status: VerificationStatus;
    message: string;
    nextStep?: string;
}

// VA Lookup types
export interface VALookupResult {
    source: VASource;
    name: string;
    branch?: string;
    rank?: string;
    birthDate?: string;
    deathDate?: string;
    cemetery?: string;
    location?: string;
    serviceDates?: string;
    awards?: string[];
    metadata: Record<string, unknown>;
}

export interface VALookupResponse {
    query: string;
    source?: VASource;
    totalResults: number;
    results: VALookupResult[];
    cached: boolean;
}

export interface VAAggregateResponse {
    query: string;
    totalResults: number;
    sources: Record<string, VALookupResponse>;
}

// History types
export interface VerificationHistoryItem {
    id: string;
    serviceType: ServiceType;
    status: VerificationStatus;
    veteranName?: string;
    createdAt: string;
    completedAt?: string;
}

export interface VerificationHistoryResponse {
    total: number;
    page: number;
    perPage: number;
    items: VerificationHistoryItem[];
}

// User/Profile types
export interface Profile {
    id: string;
    email: string;
    fullName?: string;
    organization?: string;
    apiKey: string;
    role: "user" | "admin";
    isActive: boolean;
    createdAt: string;
}

// API Response wrapper
export interface ApiResponse<T> {
    success: boolean;
    message: string;
    data?: T;
}

export interface ApiError {
    success: false;
    errorCode: string;
    message: string;
    details?: Record<string, unknown>;
}

// Military branches list for UI
export const MILITARY_BRANCHES: { value: MilitaryBranch; label: string }[] = [
    { value: "Army", label: "Army" },
    { value: "Navy", label: "Navy" },
    { value: "Air Force", label: "Air Force" },
    { value: "Marine Corps", label: "Marine Corps" },
    { value: "Coast Guard", label: "Coast Guard" },
    { value: "Space Force", label: "Space Force" },
    { value: "Army National Guard", label: "Army National Guard" },
    { value: "Army Reserve", label: "Army Reserve" },
    { value: "Air National Guard", label: "Air National Guard" },
    { value: "Air Force Reserve", label: "Air Force Reserve" },
    { value: "Navy Reserve", label: "Navy Reserve" },
    { value: "Marine Corps Reserve", label: "Marine Corps Reserve" },
    { value: "Coast Guard Reserve", label: "Coast Guard Reserve" },
];

// Service types list for UI
export const SERVICE_TYPES: { value: ServiceType; label: string; icon: string }[] = [
    { value: "chatgpt", label: "ChatGPT Plus", icon: "🤖" },
    { value: "spotify", label: "Spotify Premium", icon: "🎵" },
    { value: "youtube", label: "YouTube Premium", icon: "📺" },
    { value: "google_one", label: "Google One", icon: "☁️" },
    { value: "other", label: "Other", icon: "📦" },
];

// Status colors and labels
export const STATUS_CONFIG: Record<VerificationStatus, { label: string; color: string; bgColor: string }> = {
    pending: { label: "Pending", color: "text-yellow-600", bgColor: "bg-yellow-100" },
    processing: { label: "Processing", color: "text-blue-600", bgColor: "bg-blue-100" },
    approved: { label: "Approved", color: "text-green-600", bgColor: "bg-green-100" },
    rejected: { label: "Rejected", color: "text-red-600", bgColor: "bg-red-100" },
    document_required: { label: "Document Required", color: "text-orange-600", bgColor: "bg-orange-100" },
    error: { label: "Error", color: "text-red-600", bgColor: "bg-red-100" },
    expired: { label: "Expired", color: "text-gray-600", bgColor: "bg-gray-100" },
};
