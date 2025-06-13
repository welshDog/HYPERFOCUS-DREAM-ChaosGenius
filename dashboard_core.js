// Revenue Autopilot Integration
loadRevenueAutopilotData() {
    fetch('/api/revenue_autopilot_status')
        .then(response => response.json())
        .then(data => {
            this.updateRevenueMetrics(data);
            this.displayOptimizationSuggestions(data);
            this.updateBroskiRewards(data);
        })
        .catch(error => console.error('Revenue autopilot data load failed:', error));
}

updateRevenueMetrics(data) {
    const autopilotData = data.revenue_autopilot || {};
    
    // Update revenue displays
    const dailyRevenueEl = document.getElementById('daily-revenue');
    if (dailyRevenueEl) {
        dailyRevenueEl.innerHTML = `
            <div class="revenue-metric">
                <h3>💰 Today's Revenue</h3>
                <div class="amount">£${autopilotData.daily_revenue?.toFixed(2) || '0.00'}</div>
                <div class="status ${autopilotData.status === 'LEGENDARY MODE ACTIVE' ? 'active' : 'standby'}">
                    ${autopilotData.status || 'STANDBY'}
                </div>
            </div>
        `;
    }

    // Update stream performance
    const streamsEl = document.getElementById('revenue-streams');
    if (streamsEl && autopilotData.stream_performance) {
        streamsEl.innerHTML = autopilotData.stream_performance.map(stream => `
            <div class="stream-card">
                <h4>${stream.name}</h4>
                <div class="stream-metrics">
                    <span class="daily-avg">£${stream.daily_avg?.toFixed(2)}/day</span>
                    <span class="roi-score">ROI: ${stream.roi_score?.toFixed(1)}</span>
                </div>
                <div class="recommendation">${stream.recommendation}</div>
            </div>
        `).join('');
    }
}

updateBroskiRewards(data) {
    const autopilotData = data.revenue_autopilot || {};
    
    const broskiEl = document.getElementById('broski-rewards');
    if (broskiEl) {
        broskiEl.innerHTML = `
            <div class="broski-display">
                <h3>🎮 BROski$ Rewards</h3>
                <div class="broski-amount">${autopilotData.total_broski_earned?.toFixed(1) || '0.0'}</div>
                <div class="streak">🔥 ${autopilotData.daily_streak || 0} day streak</div>
            </div>
        `;
    }
}

displayOptimizationSuggestions(data) {
    const autopilotData = data.revenue_autopilot || {};
    
    const suggestionsEl = document.getElementById('optimization-suggestions');
    if (suggestionsEl && autopilotData.optimization_suggestions) {
        suggestionsEl.innerHTML = `
            <div class="suggestions-panel">
                <h3>🧠 AI Optimization Suggestions</h3>
                ${autopilotData.optimization_suggestions.map(suggestion => `
                    <div class="suggestion-item">${suggestion}</div>
                `).join('')}
            </div>
        `;
    }
}

// Add to initialization
initializeRevenueAutopilot() {
    // Load revenue data immediately
    this.loadRevenueAutopilotData();
    
    // Set up auto-refresh every 5 minutes
    setInterval(() => {
        this.loadRevenueAutopilotData();
    }, 300000);
    
    console.log("🚀 Revenue Autopilot dashboard integration ACTIVE!");
}