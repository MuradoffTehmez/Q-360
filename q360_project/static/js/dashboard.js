/**
 * Dashboard Real-time Data Handler
 */

// Global chart instances
let trendsChart = null;
let forecastChart = null;

/**
 * Load dashboard statistics
 */
async function loadDashboardStats() {
    try {
        const response = await fetch('/dashboard/api/stats/');
        const data = await response.json();

        if (data.success) {
            updateStatsCards(data.stats);
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
        showError('Statistika yüklənərkən xəta baş verdi');
    }
}

/**
 * Update statistics cards with real data
 */
function updateStatsCards(stats) {
    // Users
    const totalUsersEl = document.getElementById('totalUsers');
    const activeUsersEl = document.getElementById('activeUsers');
    const userGrowthEl = document.getElementById('userGrowth');

    if (totalUsersEl) totalUsersEl.textContent = stats.users.total;
    if (activeUsersEl) activeUsersEl.textContent = stats.users.active;
    if (userGrowthEl) userGrowthEl.textContent = `${stats.users.growth_rate}%`;

    // Evaluations
    const activeCampaignsEl = document.getElementById('activeCampaigns');
    const completedEvalsEl = document.getElementById('completedEvaluations');
    const avgScoreEl = document.getElementById('averageScore');

    if (activeCampaignsEl) activeCampaignsEl.textContent = stats.evaluations.active_campaigns;
    if (completedEvalsEl) completedEvalsEl.textContent = stats.evaluations.completed_last_30_days;
    if (avgScoreEl) avgScoreEl.textContent = stats.evaluations.average_score;

    // Training
    const completedTrainingsEl = document.getElementById('completedTrainings');
    const inProgressTrainingsEl = document.getElementById('inProgressTrainings');

    if (completedTrainingsEl) completedTrainingsEl.textContent = stats.training.completed_last_30_days;
    if (inProgressTrainingsEl) inProgressTrainingsEl.textContent = stats.training.in_progress;

    // Goals
    const activeGoalsEl = document.getElementById('activeGoals');
    const completedGoalsEl = document.getElementById('completedGoals');

    if (activeGoalsEl) activeGoalsEl.textContent = stats.goals.active;
    if (completedGoalsEl) completedGoalsEl.textContent = stats.goals.completed_last_30_days;
}

/**
 * Load and render trends chart
 */
async function loadTrendsChart() {
    try {
        const response = await fetch('/dashboard/api/trends/');
        const data = await response.json();

        if (data.success) {
            renderTrendsChart(data.trends);
        }
    } catch (error) {
        console.error('Error loading trends:', error);
        showError('Trend məlumatları yüklənərkən xəta baş verdi');
    }
}

/**
 * Render trends chart with real data
 */
function renderTrendsChart(trendsData) {
    const canvas = document.getElementById('trendsChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Destroy existing chart if exists
    if (trendsChart) {
        trendsChart.destroy();
    }

    trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendsData.labels,
            datasets: trendsData.datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Son 30 Günün Trendləri'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

/**
 * Load and render forecasting chart
 */
async function loadForecastingChart() {
    try {
        const response = await fetch('/dashboard/api/forecasting/');
        const data = await response.json();

        if (data.success) {
            renderForecastingChart(data.forecasting);
        }
    } catch (error) {
        console.error('Error loading forecasting:', error);
        showError('Proqnoz məlumatları yüklənərkən xəta baş verdi');
    }
}

/**
 * Render forecasting chart with real data
 */
function renderForecastingChart(forecastingData) {
    const canvas = document.getElementById('forecastChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // Destroy existing chart if exists
    if (forecastChart) {
        forecastChart.destroy();
    }

    forecastChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: forecastingData.combined_labels,
            datasets: forecastingData.combined_datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Performans Proqnozu (90 Gün Tarixi + 30 Gün Proqnoz)'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null && context.parsed.y !== undefined) {
                                label += context.parsed.y.toFixed(2);
                            }
                            return label;
                        }
                    }
                },
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            xMin: forecastingData.historical.labels.length - 1,
                            xMax: forecastingData.historical.labels.length - 1,
                            borderColor: 'rgba(255, 99, 132, 0.5)',
                            borderWidth: 2,
                            borderDash: [5, 5],
                            label: {
                                enabled: true,
                                content: 'Proqnoz Başlanğıcı',
                                position: 'top'
                            }
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(1);
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

/**
 * Refresh all dashboard data
 */
async function refreshDashboard() {
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.disabled = true;
        refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Yenilənir...';
    }

    try {
        await Promise.all([
            loadDashboardStats(),
            loadTrendsChart(),
            loadForecastingChart()
        ]);

        showSuccess('Dashboard uğurla yeniləndi');
    } catch (error) {
        console.error('Error refreshing dashboard:', error);
        showError('Dashboard yenilənərkən xəta baş verdi');
    } finally {
        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Yenilə';
        }
    }
}

/**
 * Show success message
 */
function showSuccess(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 end-0 p-3';
    toast.style.zIndex = '11';
    toast.innerHTML = `
        <div class="toast show" role="alert">
            <div class="toast-header bg-success text-white">
                <i class="fas fa-check-circle me-2"></i>
                <strong class="me-auto">Uğurlu</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

/**
 * Show error message
 */
function showError(message) {
    const toast = document.createElement('div');
    toast.className = 'position-fixed top-0 end-0 p-3';
    toast.style.zIndex = '11';
    toast.innerHTML = `
        <div class="toast show" role="alert">
            <div class="toast-header bg-danger text-white">
                <i class="fas fa-exclamation-circle me-2"></i>
                <strong class="me-auto">Xəta</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}

/**
 * Initialize dashboard when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Load initial data
    loadDashboardStats();

    // Load charts if canvas exists
    if (document.getElementById('trendsChart')) {
        loadTrendsChart();
    }

    if (document.getElementById('forecastChart')) {
        loadForecastingChart();
    }

    // Setup refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshDashboard);
    }

    // Auto-refresh every 5 minutes
    setInterval(loadDashboardStats, 5 * 60 * 1000);
});
