"use client";

import { useState } from "react";
import { Header } from "@/components/layout";
import {
    Card,
    CardContent,
    Button,
    Input,
    Select,
    Badge,
} from "@/components/ui";
import { MILITARY_BRANCHES, VALookupResult, VASource } from "@/types";
import { Search, MapPin, Award, Calendar, User, Building } from "lucide-react";

export default function LookupPage() {
    const [isLoading, setIsLoading] = useState(false);
    const [activeSource, setActiveSource] = useState<VASource | "all">("all");
    const [searchParams, setSearchParams] = useState({
        firstName: "",
        lastName: "",
        branch: "",
        state: "",
    });
    const [results, setResults] = useState<VALookupResult[]>([]);
    const [hasSearched, setHasSearched] = useState(false);

    const handleSearch = async () => {
        setIsLoading(true);
        setHasSearched(true);

        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 1500));

        // Mock results
        setResults([
            {
                source: "grave_locator",
                name: "John Smith",
                branch: "Army",
                rank: "Sergeant",
                birthDate: "1945-03-15",
                deathDate: "2020-11-22",
                cemetery: "Arlington National Cemetery",
                location: "Section 60, Grave 1234",
                serviceDates: "1963-1967",
                awards: ["Purple Heart", "Bronze Star"],
                metadata: {},
            },
            {
                source: "vlm",
                name: "John William Smith",
                branch: "Army",
                rank: "Staff Sergeant",
                birthDate: "1942",
                deathDate: "2018",
                cemetery: "Fort Logan National Cemetery",
                location: "Denver, CO",
                serviceDates: "1960-1968",
                awards: ["Combat Infantryman Badge"],
                metadata: {},
            },
            {
                source: "army_explorer",
                name: "Jonathan Smith",
                branch: "Marine Corps",
                rank: "Corporal",
                birthDate: "1950-06-10",
                deathDate: "2015-01-05",
                cemetery: "San Francisco National Cemetery",
                location: "San Francisco, CA",
                serviceDates: "1968-1972",
                metadata: {},
            },
        ]);
        setIsLoading(false);
    };

    const filteredResults =
        activeSource === "all"
            ? results
            : results.filter((r) => r.source === activeSource);

    const getSourceLabel = (source: VASource) => {
        const labels: Record<VASource, string> = {
            grave_locator: "VA Grave Locator",
            vlm: "Veterans Legacy Memorial",
            army_explorer: "Army Explorer",
        };
        return labels[source];
    };

    const getSourceColor = (source: VASource) => {
        const colors: Record<VASource, "info" | "success" | "warning"> = {
            grave_locator: "info",
            vlm: "success",
            army_explorer: "warning",
        };
        return colors[source];
    };

    return (
        <>
            <Header
                title="VA Lookup"
                description="Search public VA databases for veteran records"
            />

            <div className="p-6 space-y-6">
                {/* Search Form */}
                <Card>
                    <CardContent className="p-6">
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <Input
                                label="First Name"
                                value={searchParams.firstName}
                                onChange={(e) =>
                                    setSearchParams({ ...searchParams, firstName: e.target.value })
                                }
                                placeholder="John"
                            />
                            <Input
                                label="Last Name"
                                value={searchParams.lastName}
                                onChange={(e) =>
                                    setSearchParams({ ...searchParams, lastName: e.target.value })
                                }
                                placeholder="Smith"
                            />
                            <Select
                                label="Branch (Optional)"
                                value={searchParams.branch}
                                onChange={(e) =>
                                    setSearchParams({ ...searchParams, branch: e.target.value })
                                }
                                options={[{ value: "", label: "All Branches" }, ...MILITARY_BRANCHES]}
                            />
                            <Input
                                label="State (Optional)"
                                value={searchParams.state}
                                onChange={(e) =>
                                    setSearchParams({ ...searchParams, state: e.target.value })
                                }
                                placeholder="CA"
                            />
                        </div>
                        <div className="mt-6 flex justify-end">
                            <Button
                                onClick={handleSearch}
                                isLoading={isLoading}
                                disabled={!searchParams.firstName && !searchParams.lastName}
                            >
                                <Search className="w-4 h-4 mr-2" />
                                Search VA Records
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                {/* Source Tabs */}
                {hasSearched && (
                    <div className="flex flex-wrap gap-2">
                        <button
                            onClick={() => setActiveSource("all")}
                            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeSource === "all"
                                    ? "bg-blue-600 text-white"
                                    : "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200"
                                }`}
                        >
                            All Sources ({results.length})
                        </button>
                        {(["grave_locator", "vlm", "army_explorer"] as VASource[]).map(
                            (source) => {
                                const count = results.filter((r) => r.source === source).length;
                                return (
                                    <button
                                        key={source}
                                        onClick={() => setActiveSource(source)}
                                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeSource === source
                                                ? "bg-blue-600 text-white"
                                                : "bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200"
                                            }`}
                                    >
                                        {getSourceLabel(source)} ({count})
                                    </button>
                                );
                            }
                        )}
                    </div>
                )}

                {/* Results */}
                {hasSearched && (
                    <div className="space-y-4">
                        {filteredResults.length === 0 ? (
                            <Card>
                                <CardContent className="p-12 text-center">
                                    <Search className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                                        No Results Found
                                    </h3>
                                    <p className="text-gray-500 dark:text-gray-400">
                                        Try adjusting your search criteria or searching a different name.
                                    </p>
                                </CardContent>
                            </Card>
                        ) : (
                            filteredResults.map((result, index) => (
                                <Card key={index} hover>
                                    <CardContent className="p-6">
                                        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-3 mb-3">
                                                    <Badge variant={getSourceColor(result.source as VASource)}>
                                                        {getSourceLabel(result.source as VASource)}
                                                    </Badge>
                                                    {result.awards && result.awards.length > 0 && (
                                                        <Badge variant="warning">
                                                            <Award className="w-3 h-3 mr-1" />
                                                            {result.awards.length} Awards
                                                        </Badge>
                                                    )}
                                                </div>

                                                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                                    {result.name}
                                                </h3>

                                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                                    {result.branch && (
                                                        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                                                            <User className="w-4 h-4" />
                                                            <span>
                                                                {result.rank && `${result.rank}, `}
                                                                {result.branch}
                                                            </span>
                                                        </div>
                                                    )}
                                                    {result.serviceDates && (
                                                        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                                                            <Calendar className="w-4 h-4" />
                                                            <span>{result.serviceDates}</span>
                                                        </div>
                                                    )}
                                                    {result.cemetery && (
                                                        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                                                            <Building className="w-4 h-4" />
                                                            <span>{result.cemetery}</span>
                                                        </div>
                                                    )}
                                                    {result.location && (
                                                        <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                                                            <MapPin className="w-4 h-4" />
                                                            <span>{result.location}</span>
                                                        </div>
                                                    )}
                                                </div>

                                                {result.awards && result.awards.length > 0 && (
                                                    <div className="mt-4 flex flex-wrap gap-2">
                                                        {result.awards.map((award, i) => (
                                                            <span
                                                                key={i}
                                                                className="px-2 py-1 bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300 text-xs rounded-full"
                                                            >
                                                                {award}
                                                            </span>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>

                                            <div className="text-right text-sm text-gray-500 dark:text-gray-400">
                                                {result.birthDate && (
                                                    <p>Born: {result.birthDate}</p>
                                                )}
                                                {result.deathDate && (
                                                    <p>Passed: {result.deathDate}</p>
                                                )}
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </div>
                )}

                {/* Initial State */}
                {!hasSearched && (
                    <Card>
                        <CardContent className="p-12 text-center">
                            <div className="w-20 h-20 mx-auto bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mb-6">
                                <Search className="w-10 h-10 text-blue-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                                Search VA Records
                            </h3>
                            <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
                                Enter a name to search across VA Grave Locator, Veterans Legacy
                                Memorial, and Army National Cemetery Explorer.
                            </p>
                        </CardContent>
                    </Card>
                )}
            </div>
        </>
    );
}
