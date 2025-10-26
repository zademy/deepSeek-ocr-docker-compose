# DeepSeek OCR - Optimized Build Script
# This script enables Docker BuildKit for faster, more efficient builds

Write-Host "🚀 Starting Optimized Docker Build..." -ForegroundColor Cyan
Write-Host ""

# Enable Docker BuildKit for better caching and parallel builds
$env:DOCKER_BUILDKIT = "1"
$env:COMPOSE_DOCKER_CLI_BUILD = "1"

Write-Host "✓ BuildKit enabled" -ForegroundColor Green
Write-Host "✓ This will optimize layer caching and reduce build time" -ForegroundColor Green
Write-Host ""

# Show current images
Write-Host "Current images:" -ForegroundColor Yellow
docker images | Select-String -Pattern "deepseek"
Write-Host ""

# Build with BuildKit
Write-Host "Building containers with BuildKit optimizations..." -ForegroundColor Cyan
docker-compose build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    Write-Host ""
    
    # Show new image sizes
    Write-Host "Updated images:" -ForegroundColor Yellow
    docker images | Select-String -Pattern "deepseek"
    Write-Host ""
    
    Write-Host "To start the services, run:" -ForegroundColor Cyan
    Write-Host "  docker-compose up -d" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Build failed. Check the errors above." -ForegroundColor Red
    exit 1
}
