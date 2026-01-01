import {
    CreateVerificationRequest,
    CreateVerificationResponse,
    SubmitVerificationRequest,
    SubmitVerificationResponse,
    Verification,
    VALookupResponse,
    VAAggregateResponse,
    VerificationHistoryResponse,
} from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
    private baseUrl: string;
    private apiKey?: string;
    private token?: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    setApiKey(apiKey: string) {
        this.apiKey = apiKey;
    }

    setToken(token: string) {
        this.token = token;
    }

    private getHeaders(): HeadersInit {
        const headers: HeadersInit = {
            "Content-Type": "application/json",
        };

        if (this.apiKey) {
            headers["X-API-Key"] = this.apiKey;
        } else if (this.token) {
            headers["Authorization"] = `Bearer ${this.token}`;
        }

        return headers;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;

        const response = await fetch(url, {
            ...options,
            headers: {
                ...this.getHeaders(),
                ...options.headers,
            },
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({
                message: response.statusText,
            }));
            throw new Error(error.detail || error.message || "Request failed");
        }

        return response.json();
    }

    // Verification endpoints
    async createVerification(
        data: CreateVerificationRequest
    ): Promise<CreateVerificationResponse> {
        return this.request("/api/verify/create", {
            method: "POST",
            body: JSON.stringify(data),
        });
    }

    async submitVerification(
        data: SubmitVerificationRequest
    ): Promise<SubmitVerificationResponse> {
        return this.request("/api/verify/submit", {
            method: "POST",
            body: JSON.stringify(data),
        });
    }

    async getVerificationStatus(verificationId: string): Promise<Verification> {
        return this.request(`/api/verify/${verificationId}/status`);
    }

    async uploadDocument(
        verificationId: string,
        file: File,
        documentType: string
    ): Promise<{ status: string; message: string }> {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("document_type", documentType);

        const response = await fetch(
            `${this.baseUrl}/api/verify/${verificationId}/document`,
            {
                method: "POST",
                headers: {
                    ...(this.apiKey ? { "X-API-Key": this.apiKey } : {}),
                    ...(this.token ? { Authorization: `Bearer ${this.token}` } : {}),
                },
                body: formData,
            }
        );

        if (!response.ok) {
            throw new Error("Failed to upload document");
        }

        return response.json();
    }

    // VA Lookup endpoints
    async searchGraveLocator(params: {
        firstName?: string;
        lastName?: string;
        state?: string;
    }): Promise<VALookupResponse> {
        const query = new URLSearchParams();
        if (params.firstName) query.set("first_name", params.firstName);
        if (params.lastName) query.set("last_name", params.lastName);
        if (params.state) query.set("state", params.state);

        return this.request(`/api/lookup/grave?${query.toString()}`);
    }

    async searchVLM(params: {
        firstName?: string;
        lastName?: string;
        branch?: string;
    }): Promise<VALookupResponse> {
        const query = new URLSearchParams();
        if (params.firstName) query.set("first_name", params.firstName);
        if (params.lastName) query.set("last_name", params.lastName);
        if (params.branch) query.set("branch", params.branch);

        return this.request(`/api/lookup/vlm?${query.toString()}`);
    }

    async searchArmyExplorer(params: {
        firstName?: string;
        lastName?: string;
    }): Promise<VALookupResponse> {
        const query = new URLSearchParams();
        if (params.firstName) query.set("first_name", params.firstName);
        if (params.lastName) query.set("last_name", params.lastName);

        return this.request(`/api/lookup/army?${query.toString()}`);
    }

    async searchAllSources(params: {
        firstName?: string;
        lastName?: string;
        branch?: string;
    }): Promise<VAAggregateResponse> {
        const query = new URLSearchParams();
        if (params.firstName) query.set("first_name", params.firstName);
        if (params.lastName) query.set("last_name", params.lastName);
        if (params.branch) query.set("branch", params.branch);

        return this.request(`/api/lookup/aggregate?${query.toString()}`);
    }

    // History endpoints
    async getHistory(params?: {
        page?: number;
        perPage?: number;
        status?: string;
        serviceType?: string;
    }): Promise<VerificationHistoryResponse> {
        const query = new URLSearchParams();
        if (params?.page) query.set("page", params.page.toString());
        if (params?.perPage) query.set("per_page", params.perPage.toString());
        if (params?.status) query.set("status", params.status);
        if (params?.serviceType) query.set("service_type", params.serviceType);

        return this.request(`/api/history?${query.toString()}`);
    }

    // Health check
    async healthCheck(): Promise<{ status: string; version: string }> {
        return this.request("/health");
    }
}

// Export singleton instance
export const api = new ApiClient(API_URL);
