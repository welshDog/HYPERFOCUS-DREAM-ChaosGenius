# BroskiDiscordIntegration.ps1 🚀💬
# Add this to your main script or run separately
# DISCORD WEBHOOK MISSION SENDER

param(
    [string]$WebhookURL = "",
    [string]$Mission = ""
)

if ($WebhookURL -eq "" -or $Mission -eq "") {
    Write-Host "🔧 SETUP: Add your Discord webhook URL to enable Discord missions!" -ForegroundColor Yellow
    Write-Host "Usage: .\BroskiDiscordIntegration.ps1 -WebhookURL 'your_webhook_url' -Mission 'your_mission'" -ForegroundColor Cyan
    exit
}

$payload = @{
    embeds = @(
        @{
            title = "🌀 BROSKI MISSION DEPLOYMENT 🌀"
            description = $Mission
            color = 8388736  # Purple color
            footer = @{
                text = "ChaosGenius Cave Portal | $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            }
            thumbnail = @{
                url = "https://cdn.discordapp.com/emojis/your_custom_emoji_here.png"
            }
        }
    )
} | ConvertTo-Json -Depth 3

try {
    Invoke-RestMethod -Uri $WebhookURL -Method Post -Body $payload -ContentType "application/json"
    Write-Host "✅ Mission sent to Discord successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to send to Discord: $($_.Exception.Message)" -ForegroundColor Red
}