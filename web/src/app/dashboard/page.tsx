"use client";

import { Header } from "@/components/layout";
import { Card, CardContent, StatusBadge } from "@/components/ui";
import {
    Shield,
    CheckCircle,
    Clock,
    AlertCircle,
    TrendingUp,
    Users,
    FileCheck,
    ArrowRight,
} from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
    // Mock data - in production, fetch from API
    const stats = [
        {
            label: "Total Verifications",
            value: "24",
            change: "+12%",
            icon: FileCheck,
            color: "from-blue-500 to-indigo-600",
        },
        {
            label: "Approved",
            value: "18",
            change: "+8%",
            icon: CheckCircle,
            color: "from-green-500 to-emerald-600",
        },
        {
            label: "Pending",
            value: "4",
            change: "-2%",
            icon: Clock,
            color: "from-yellow-500 to-orange-600",
        },
        {
            label: "Rejected",
            value: "2",
            change: "0%",
            icon: AlertCircle,
            color: "from-red-500 to-pink-600",
        },
    ];

    const recentVerifications = [
        {
            id: "1",
            name: "John Smith",
            service: "ChatGPT Plus",
            status: "approved" as const,
            date: "2026-01-01",
        },
        {
            id: "2",
            name: "Mike Johnson",
            service: "Spotify Premium",
            status: "processing" as const,
            date: "2026-01-01",
        },
        {
            id: "3",
            name: "David Williams",
            service: "YouTube Premium",
            status: "document_required" as const,
            date: "2025-12-31",
        },
        {
            id: "4",
            name: "James Brown",
            service: "Google One",
            status: "pending" as const,
            date: "2025-12-30",
        },
    ];

    return (
        <>
            <Header
                title="Dashboard"
                description="Overview of your verification activities"
            />

            <div className="p-6 space-y-6">
                {/* Stats Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {stats.map((stat) => (
                        <Card key={stat.label} hover>
                            <CardContent className="p-6">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
                                            {stat.label}
                                        </p>
                                        <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
                                            {stat.value}
                                        </p>
                                        <div className="flex items-center gap-1 mt-2">
                                            <TrendingUp className="w-4 h-4 text-green-500" />
                                            <span className="text-sm text-green-500">{stat.change}</span>
                                            <span className="text-sm text-gray-400">vs last month</span>
                                        </div>
                                    </div>
                                    <div
                                        className={`w-14 h-14 rounded-xl bg-gradient-to-br ${stat.color} flex items-center justify-center`}
                                    >
                                        <stat.icon className="w-7 h-7 text-white" />
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>

                {/* Quick Actions */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Link href="/verify">
                        <Card hover className="cursor-pointer group">
                            <CardContent className="p-6">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center">
                                        <Shield className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="font-semibold text-gray-900 dark:text-white">
                                            New Verification
                                        </h3>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            Start a new verification request
                                        </p>
                                    </div>
                                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors" />
                                </div>
                            </CardContent>
                        </Card>
                    </Link>

                    <Link href="/lookup">
                        <Card hover className="cursor-pointer group">
                            <CardContent className="p-6">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center">
                                        <Users className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="font-semibold text-gray-900 dark:text-white">
                                            VA Lookup
                                        </h3>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            Search veteran records
                                        </p>
                                    </div>
                                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-green-600 transition-colors" />
                                </div>
                            </CardContent>
                        </Card>
                    </Link>

                    <Link href="/history">
                        <Card hover className="cursor-pointer group">
                            <CardContent className="p-6">
                                <div className="flex items-center gap-4">
                                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                                        <Clock className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="flex-1">
                                        <h3 className="font-semibold text-gray-900 dark:text-white">
                                            View History
                                        </h3>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            Track all verifications
                                        </p>
                                    </div>
                                    <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-purple-600 transition-colors" />
                                </div>
                            </CardContent>
                        </Card>
                    </Link>
                </div>

                {/* Recent Verifications */}
                <Card>
                    <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                            Recent Verifications
                        </h2>
                        <Link
                            href="/history"
                            className="text-sm text-blue-600 hover:text-blue-700 font-medium"
                        >
                            View all
                        </Link>
                    </div>
                    <div className="divide-y divide-gray-200 dark:divide-gray-700">
                        {recentVerifications.map((verification) => (
                            <div
                                key={verification.id}
                                className="px-6 py-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                            >
                                <div className="flex items-center gap-4">
                                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-indigo-600 flex items-center justify-center text-white font-bold">
                                        {verification.name[0]}
                                    </div>
                                    <div>
                                        <p className="font-medium text-gray-900 dark:text-white">
                                            {verification.name}
                                        </p>
                                        <p className="text-sm text-gray-500 dark:text-gray-400">
                                            {verification.service}
                                        </p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    <StatusBadge status={verification.status} />
                                    <span className="text-sm text-gray-500 dark:text-gray-400">
                                        {verification.date}
                                    </span>
                                </div>
                            </div>
                        ))}
                    </div>
                </Card>
            </div>
        </>
    );
}
