/**
 * Real-time Threat Dashboard
 * WebSocket ilə canlı threat monitoring
 */

class ThreatDashboard {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.charts = {};
        this.init();
    }

    init() {
        this.connectWebSocket();
        this.initializeCharts();
        this.setupEventListeners();
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/audit/threat-monitor/`;

        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('✅ Threat Monitor WebSocket connected');
            this.reconnectAttempts = 0;
            this.updateConnectionStatus('connected');

            // Request initial stats
            this.ws.send(JSON.stringify({
                type: 'get_stats'
            }));
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.ws.onerror = (error) => {
            console.error('❌ WebSocket error:', error);
            this.updateConnectionStatus('error');
        };

        this.ws.onclose = () => {
            console.log('🔌 WebSocket closed');
            this.updateConnectionStatus('disconnected');
            this.attemptReconnect();
        };
    }

    handleMessage(data) {
        console.log('📨 Received:', data.type);

        switch (data.type) {
            case 'initial_data':
            case 'stats_update':
                this.updateDashboard(data.data);
                break;

            case 'threat_alert':
                this.showThreatAlert(data.data);
                break;

            case 'recent_threats':
                this.updateRecentThreats(data.data);
                break;
        }
    }

    updateDashboard(stats) {
        console.log('📊 Updating dashboard:', stats);

        // Update threat distribution chart
        if (this.charts.threatDistribution) {
            this.charts.threatDistribution.data.datasets[0].data = [
                stats.threat_distribution.critical,
                stats.threat_distribution.high,
                stats.threat_distribution.medium,
                stats.threat_distribution.low
            ];
            this.charts.threatDistribution.update();
        }

        // Update failed logins chart
        if (this.charts.failedLogins && stats.failed_logins_hourly) {
            this.charts.failedLogins.data.labels = stats.failed_logins_hourly.map(h => h.hour);
            this.charts.failedLogins.data.datasets[0].data = stats.failed_logins_hourly.map(h => h.count);
            this.charts.failedLogins.update();
        }

        // Update top threat users table
        this.updateTopThreatUsers(stats.top_threat_users);

        // Update summary stats
        this.updateSummaryStats(stats);
    }

    updateSummaryStats(stats) {
        const totalThreats = stats.threat_distribution.critical +
                           stats.threat_distribution.high +
                           stats.threat_distribution.medium +
                           stats.threat_distribution.low;

        // Update DOM elements
        document.getElementById('total-threats')?.innerText(totalThreats);
        document.getElementById('critical-threats')?.innerText(stats.threat_distribution.critical);
        document.getElementById('high-threats')?.innerText(stats.threat_distribution.high);
        document.getElementById('medium-threats')?.innerText(stats.threat_distribution.medium);

        // Update timestamp
        const timestamp = new Date(stats.timestamp).toLocaleTimeString('az-AZ');
        document.getElementById('last-update')?.innerText(`Son yenilənmə: ${timestamp}`);
    }

    updateTopThreatUsers(users) {
        const tbody = document.getElementById('top-threat-users-tbody');
        if (!tbody) return;

        tbody.innerHTML = '';

        users.forEach((user, index) => {
            const row = document.createElement('tr');
            row.className = 'hover:bg-gray-50';

            // Threat level badge color
            let badgeColor = 'bg-gray-100 text-gray-800';
            if (user.max_score >= 80) badgeColor = 'bg-red-100 text-red-800';
            else if (user.max_score >= 60) badgeColor = 'bg-orange-100 text-orange-800';
            else if (user.max_score >= 40) badgeColor = 'bg-yellow-100 text-yellow-800';

            row.innerHTML = `
                <td class="px-4 py-3 text-sm">${index + 1}</td>
                <td class="px-4 py-3 text-sm font-medium">${user.username}</td>
                <td class="px-4 py-3 text-sm">${user.count}</td>
                <td class="px-4 py-3 text-sm">
                    <span class="px-2 py-1 rounded text-xs ${badgeColor}">
                        ${user.max_score}
                    </span>
                </td>
            `;

            tbody.appendChild(row);
        });
    }

    updateRecentThreats(threats) {
        const container = document.getElementById('recent-threats-list');
        if (!container) return;

        container.innerHTML = '';

        threats.forEach(threat => {
            const item = document.createElement('div');
            item.className = 'border-l-4 border-red-500 bg-red-50 p-3 mb-2 rounded-r';

            const levelColor = {
                'critical': 'text-red-800',
                'high': 'text-orange-800',
                'medium': 'text-yellow-800',
                'low': 'text-blue-800'
            }[threat.threat_level] || 'text-gray-800';

            item.innerHTML = `
                <div class="flex justify-between items-start">
                    <div>
                        <span class="font-semibold">${threat.user}</span>
                        <span class="text-sm text-gray-600 ml-2">${threat.action}</span>
                    </div>
                    <span class="text-xs ${levelColor} font-bold">
                        ${threat.threat_score}
                    </span>
                </div>
                <div class="text-xs text-gray-500 mt-1">
                    ${new Date(threat.timestamp).toLocaleString('az-AZ')}
                    ${threat.ip_address ? `• ${threat.ip_address}` : ''}
                </div>
            `;

            container.appendChild(item);
        });
    }

    showThreatAlert(alertData) {
        // Show browser notification if permitted
        if (Notification.permission === 'granted') {
            new Notification('🚨 Yüksək Təhlükə Aşkarlandı!', {
                body: `İstifadəçi: ${alertData.user}\nTəhdid Skoru: ${alertData.threat_score}`,
                icon: '/static/img/alert-icon.png',
                tag: 'threat-alert'
            });
        }

        // Show in-page alert
        this.showInPageAlert(alertData);

        // Play alert sound
        this.playAlertSound();
    }

    showInPageAlert(alertData) {
        const alertsContainer = document.getElementById('threat-alerts');
        if (!alertsContainer) return;

        const alert = document.createElement('div');
        alert.className = 'bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-2 animate-pulse';
        alert.innerHTML = `
            <div class="flex justify-between items-center">
                <div>
                    <p class="font-bold">🚨 Kritik Təhlükə!</p>
                    <p class="text-sm">${alertData.user} - ${alertData.action}</p>
                    <p class="text-xs mt-1">Skor: ${alertData.threat_score}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="text-red-500 hover:text-red-700">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                    </svg>
                </button>
            </div>
        `;

        alertsContainer.prepend(alert);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            alert.remove();
        }, 10000);
    }

    playAlertSound() {
        // Optional: Play alert sound
        const audio = new Audio('/static/sounds/alert.mp3');
        audio.volume = 0.3;
        audio.play().catch(e => console.log('Sound play failed:', e));
    }

    initializeCharts() {
        // Threat Distribution Pie Chart
        const threatDistCtx = document.getElementById('threat-distribution-chart');
        if (threatDistCtx) {
            this.charts.threatDistribution = new Chart(threatDistCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Kritik', 'Yüksək', 'Orta', 'Aşağı'],
                    datasets: [{
                        data: [0, 0, 0, 0],
                        backgroundColor: [
                            '#DC2626', // red-600
                            '#F59E0B', // yellow-500
                            '#FBBF24', // yellow-400
                            '#3B82F6'  // blue-500
                        ],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        title: {
                            display: true,
                            text: 'Təhdid Səviyyəsi Paylanması (24 saat)'
                        }
                    }
                }
            });
        }

        // Failed Logins Line Chart
        const failedLoginsCtx = document.getElementById('failed-logins-chart');
        if (failedLoginsCtx) {
            this.charts.failedLogins = new Chart(failedLoginsCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Uğursuz Giriş Cəhdləri',
                        data: [],
                        borderColor: '#EF4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Saatlıq Uğursuz Giriş Cəhdləri'
                        }
                    }
                }
            });
        }
    }

    setupEventListeners() {
        // Refresh button
        document.getElementById('refresh-dashboard')?.addEventListener('click', () => {
            this.requestStatsUpdate();
        });

        // Time range selector
        document.getElementById('time-range-selector')?.addEventListener('change', (e) => {
            const hours = parseInt(e.target.value);
            this.requestRecentThreats(hours);
        });

        // Request browser notification permission
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }

    requestStatsUpdate() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'get_stats'
            }));
        }
    }

    requestRecentThreats(hours = 1) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'get_recent_threats',
                hours: hours
            }));
        }
    }

    updateConnectionStatus(status) {
        const statusEl = document.getElementById('ws-connection-status');
        if (!statusEl) return;

        const statusConfig = {
            connected: { text: 'Bağlı', class: 'bg-green-500', icon: '🟢' },
            disconnected: { text: 'Əlaqə kəsildi', class: 'bg-red-500', icon: '🔴' },
            error: { text: 'Xəta', class: 'bg-yellow-500', icon: '🟡' }
        };

        const config = statusConfig[status] || statusConfig.disconnected;
        statusEl.innerHTML = `${config.icon} ${config.text}`;
        statusEl.className = `px-3 py-1 rounded text-xs text-white ${config.class}`;
    }

    attemptReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('❌ Max reconnect attempts reached');
            return;
        }

        this.reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);

        console.log(`🔄 Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            this.connectWebSocket();
        }, delay);
    }

    destroy() {
        if (this.ws) {
            this.ws.close();
        }

        // Destroy charts
        Object.values(this.charts).forEach(chart => {
            if (chart) chart.destroy();
        });
    }
}

// Auto-initialize when DOM is ready
let threatDashboard;
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('threat-dashboard-container')) {
        threatDashboard = new ThreatDashboard();
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (threatDashboard) {
        threatDashboard.destroy();
    }
});
