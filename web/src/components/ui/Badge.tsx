"use client";

import { cn } from "@/lib/utils";
import { STATUS_CONFIG, VerificationStatus } from "@/types";

interface BadgeProps {
    status: VerificationStatus;
    className?: string;
}

export function StatusBadge({ status, className }: BadgeProps) {
    const config = STATUS_CONFIG[status];

    return (
        <span
            className={cn(
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                config.bgColor,
                config.color,
                className
            )}
        >
            {config.label}
        </span>
    );
}

interface SimpleBadgeProps {
    children: React.ReactNode;
    variant?: "default" | "success" | "warning" | "danger" | "info";
    className?: string;
}

export function Badge({
    children,
    variant = "default",
    className,
}: SimpleBadgeProps) {
    const variantStyles = {
        default: "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300",
        success: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
        warning: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
        danger: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
        info: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
    };

    return (
        <span
            className={cn(
                "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                variantStyles[variant],
                className
            )}
        >
            {children}
        </span>
    );
}
