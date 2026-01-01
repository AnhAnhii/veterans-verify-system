"use client";

import { useState } from "react";
import { Header } from "@/components/layout";
import {
    Card,
    CardContent,
    Button,
    Select,
    StatusBadge,
} from "@/components/ui";
import { SERVICE_TYPES, VerificationHistoryItem, VerificationStatus, ServiceType } from "@/types";
import { formatDate, formatRelativeTime } from "@/lib/utils";
import { Filter, Download, Eye, ChevronLeft, ChevronRight } from "lucide-react";

export default function HistoryPage() {
    const [statusFilter, setStatusFilter] = useState<string>("");
    const [serviceFilter, setServiceFilter] = useState<string>("");
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    // Mock data
    const historyItems: VerificationHistoryItem[] = [
        { id: "1", serviceType: "chatgpt", status: "approved", veteranName: "John Smith", createdAt: "2026-01-01T10:30:00Z", completedAt: "2026-01-01T10:31:00Z" },
        { id: "2", serviceType: "spotify", status: "processing", veteranName: "Mike Johnson", createdAt: "2026-01-01T09:15:00Z" },
        { id: "3", serviceType: "youtube", status: "document_required", veteranName: "David Williams", createdAt: "2025-12-31T14:20:00Z" },
        { id: "4", serviceType: "google_one", status: "pending", veteranName: "James Brown", createdAt: "2025-12-30T16:45:00Z" },
        { id: "5", serviceType: "chatgpt", status: "approved", veteranName: "Robert Davis", createdAt: "2025-12-29T11:00:00Z", completedAt: "2025-12-29T11:02:00Z" },
        { id: "6", serviceType: "spotify", status: "rejected", veteranName: "William Miller", createdAt: "2025-12-28T09:30:00Z", completedAt: "2025-12-28T09:35:00Z" },
        { id: "7", serviceType: "chatgpt", status: "approved", veteranName: "Richard Wilson", createdAt: "2025-12-27T15:00:00Z", completedAt: "2025-12-27T15:01:00Z" },
        { id: "8", serviceType: "youtube", status: "approved", veteranName: "Joseph Taylor", createdAt: "2025-12-26T10:00:00Z", completedAt: "2025-12-26T10:02:00Z" },
    ];

    const filteredItems = historyItems.filter((item) => {
        if (statusFilter && item.status !== statusFilter) return false;
        if (serviceFilter && item.serviceType !== serviceFilter) return false;
        return true;
    });

    const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
    const paginatedItems = filteredItems.slice(
        (currentPage - 1) * itemsPerPage,
        currentPage * itemsPerPage
    );

    const getServiceIcon = (serviceType: ServiceType) => {
        return SERVICE_TYPES.find((s) => s.value === serviceType)?.icon || "📦";
    };

    return (
        <>
            <Header
                title="Verification History"
                description="Track all your verification requests"
            />

            <div className="p-6 space-y-6">
                {/* Filters */}
                <Card>
                    <CardContent className="p-4">
                        <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
                            <div className="flex items-center gap-2 text-gray-500">
                                <Filter className="w-4 h-4" />
                                <span className="text-sm font-medium">Filters:</span>
                            </div>
                            <div className="flex flex-wrap gap-4">
                                <Select
                                    value={statusFilter}
                                    onChange={(e) => setStatusFilter(e.target.value)}
                                    options={[
                                        { value: "", label: "All Status" },
                                        { value: "pending", label: "Pending" },
                                        { value: "processing", label: "Processing" },
                                        { value: "approved", label: "Approved" },
                                        { value: "rejected", label: "Rejected" },
                                        { value: "document_required", label: "Document Required" },
                                    ]}
                                    className="w-40"
                                />
                                <Select
                                    value={serviceFilter}
                                    onChange={(e) => setServiceFilter(e.target.value)}
                                    options={[
                                        { value: "", label: "All Services" },
                                        ...SERVICE_TYPES.map((s) => ({
                                            value: s.value,
                                            label: s.label,
                                        })),
                                    ]}
                                    className="w-40"
                                />
                            </div>
                            <div className="flex-1" />
                            <Button variant="outline" size="sm">
                                <Download className="w-4 h-4 mr-2" />
                                Export
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {/* History Table */}
                <Card>
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-50 dark:bg-gray-800/50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Service
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Veteran
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Status
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Created
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Completed
                                    </th>
                                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                                {paginatedItems.map((item) => (
                                    <tr
                                        key={item.id}
                                        className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                                    >
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="flex items-center gap-3">
                                                <span className="text-2xl">
                                                    {getServiceIcon(item.serviceType)}
                                                </span>
                                                <span className="font-medium text-gray-900 dark:text-white">
                                                    {SERVICE_TYPES.find((s) => s.value === item.serviceType)
                                                        ?.label}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className="text-gray-900 dark:text-white">
                                                {item.veteranName || "-"}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <StatusBadge status={item.status} />
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <div className="text-sm">
                                                <p className="text-gray-900 dark:text-white">
                                                    {formatDate(item.createdAt)}
                                                </p>
                                                <p className="text-gray-500 dark:text-gray-400">
                                                    {formatRelativeTime(item.createdAt)}
                                                </p>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            {item.completedAt ? (
                                                <span className="text-gray-900 dark:text-white">
                                                    {formatDate(item.completedAt)}
                                                </span>
                                            ) : (
                                                <span className="text-gray-400">-</span>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-right">
                                            <Button variant="ghost" size="sm">
                                                <Eye className="w-4 h-4" />
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Pagination */}
                    <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                            Showing {(currentPage - 1) * itemsPerPage + 1} to{" "}
                            {Math.min(currentPage * itemsPerPage, filteredItems.length)} of{" "}
                            {filteredItems.length} results
                        </p>
                        <div className="flex items-center gap-2">
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                                disabled={currentPage === 1}
                            >
                                <ChevronLeft className="w-4 h-4" />
                            </Button>
                            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                                <Button
                                    key={page}
                                    variant={page === currentPage ? "primary" : "ghost"}
                                    size="sm"
                                    onClick={() => setCurrentPage(page)}
                                >
                                    {page}
                                </Button>
                            ))}
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                                disabled={currentPage === totalPages}
                            >
                                <ChevronRight className="w-4 h-4" />
                            </Button>
                        </div>
                    </div>
                </Card>
            </div>
        </>
    );
}
