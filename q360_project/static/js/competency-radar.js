/**
 * Competency Radar Chart for Profile Page
 * Displays user's competency levels in an interactive radar/bar chart
 */

document.addEventListener('DOMContentLoaded', function() {
    // Competency Radar Chart
    let competencyChart = null;
    let currentChartType = 'radar';

    // Fetch user skills data
    async function fetchUserSkills() {
        try {
            const response = await fetch('/api/competencies/user-skills/my_skills/');
            if (!response.ok) {
                throw new Error('Failed to fetch skills');
            }
            const data = await response.json();
            return data.results || data || [];
        } catch (error) {
            console.error('Error fetching skills:', error);
            return [];
        }
    }

    // Create chart
    async function createCompetencyChart() {
        const skills = await fetchUserSkills();

        const legendContainer = document.getElementById('competencyLegend');
        if (!legendContainer) return;

        if (skills.length === 0) {
            legendContainer.innerHTML = `
                <div class="text-center py-8 text-gray-500 dark:text-gray-400">
                    <i class="fas fa-info-circle text-4xl mb-3 block"></i>
                    <p>Hələ qeydə alınmış kompetensiya yoxdur</p>
                </div>
            `;
            return;
        }

        // Prepare data
        const labels = skills.map(skill => skill.competency_name || 'N/A');
        const scores = skills.map(skill => skill.current_score || 0);
        const maxScores = skills.map(skill => skill.target_score || 100);

        // Get dark mode status
        const isDark = document.documentElement.classList.contains('dark');
        const gridColor = isDark ? 'rgba(156, 163, 175, 0.2)' : 'rgba(209, 213, 219, 0.5)';
        const textColor = isDark ? '#D1D5DB' : '#6B7280';

        const ctx = document.getElementById('competencyRadarChart');
        if (!ctx) return;

        const chartConfig = {
            type: currentChartType,
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Cari Səviyyə',
                        data: scores,
                        backgroundColor: 'rgba(34, 197, 94, 0.2)',
                        borderColor: 'rgba(34, 197, 94, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(34, 197, 94, 1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(34, 197, 94, 1)',
                        pointRadius: 4,
                        pointHoverRadius: 6,
                    },
                    {
                        label: 'Hədəf Səviyyə',
                        data: maxScores,
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderColor: 'rgba(59, 130, 246, 0.5)',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        pointBackgroundColor: 'rgba(59, 130, 246, 0.5)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
                        pointRadius: 3,
                        pointHoverRadius: 5,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: textColor,
                            font: {
                                size: 12
                            },
                            padding: 15,
                            usePointStyle: true,
                        }
                    },
                    tooltip: {
                        backgroundColor: isDark ? 'rgba(31, 41, 55, 0.95)' : 'rgba(255, 255, 255, 0.95)',
                        titleColor: isDark ? '#F3F4F6' : '#111827',
                        bodyColor: isDark ? '#D1D5DB' : '#374151',
                        borderColor: isDark ? '#4B5563' : '#E5E7EB',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed.r !== undefined ? context.parsed.r : context.parsed.y;
                                return context.dataset.label + ': ' + value + ' bal';
                            }
                        }
                    }
                },
                scales: currentChartType === 'radar' ? {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20,
                            color: textColor,
                            backdropColor: 'transparent',
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            color: gridColor,
                        },
                        pointLabels: {
                            color: textColor,
                            font: {
                                size: 11,
                                weight: '600'
                            }
                        }
                    }
                } : {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            color: textColor,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            color: gridColor,
                        }
                    },
                    x: {
                        ticks: {
                            color: textColor,
                            font: {
                                size: 10
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        };

        // Destroy existing chart
        if (competencyChart) {
            competencyChart.destroy();
        }

        competencyChart = new Chart(ctx, chartConfig);

        // Update legend
        updateLegend(skills);
    }

    // Update legend with progress bars
    function updateLegend(skills) {
        const legendHTML = skills.map(skill => {
            const score = skill.current_score || 0;
            const targetScore = skill.target_score || 100;
            const percentage = targetScore > 0 ? Math.round((score / targetScore) * 100) : 0;
            const colorClass = percentage >= 80 ? 'bg-green-500' :
                              percentage >= 60 ? 'bg-blue-500' :
                              percentage >= 40 ? 'bg-yellow-500' : 'bg-red-500';

            return `
                <div class="group hover:bg-gray-50 dark:hover:bg-gray-700/50 p-3 rounded-lg transition-colors">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-sm font-semibold text-gray-900 dark:text-white">${skill.competency_name || 'N/A'}</span>
                        <span class="text-xs font-medium text-gray-600 dark:text-gray-400">
                            ${score}/${targetScore}
                        </span>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div class="${colorClass} h-full transition-all duration-500" style="width: ${percentage}%"></div>
                        </div>
                        <span class="text-xs font-semibold text-gray-700 dark:text-gray-300 min-w-[3rem] text-right">
                            ${percentage}%
                        </span>
                    </div>
                    ${skill.level_name ? `
                        <div class="mt-1">
                            <span class="inline-block px-2 py-0.5 text-xs font-medium rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300">
                                ${skill.level_name}
                            </span>
                        </div>
                    ` : ''}
                </div>
            `;
        }).join('');

        document.getElementById('competencyLegend').innerHTML = legendHTML;
    }

    // Update chart view (radar/bar)
    window.updateChartView = function(type) {
        currentChartType = type;
        createCompetencyChart();
    };

    // Initial load
    createCompetencyChart();

    // Listen for dark mode changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'class') {
                createCompetencyChart();
            }
        });
    });

    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['class']
    });
});
