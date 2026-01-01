"use client";

import { Sidebar } from "@/components/layout";
import { ReactNode } from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
    return (
        <div className="flex min-h-screen bg-gray-50 dark:bg-gray-900">
            <Sidebar user={{ email: "user@example.com", name: "John Doe" }} />
            <main className="flex-1 lg:ml-0">{children}</main>
        </div>
    );
}
