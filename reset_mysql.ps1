$ErrorActionPreference = "Stop"

$ServiceName = "MySQL84"
$ExePath = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe"
$IniPath = "C:\ProgramData\MySQL\MySQL Server 8.4\my.ini"
$InitSqlPath = "$env:TEMP\reset_root.sql"

# 1. 停止服务
try {
    Write-Host "1. Stopping service $ServiceName..." -ForegroundColor Cyan
    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
} catch {
    Write-Warning "Service stop failed or service not running."
}

# 2. 确保没有 mysqld 进程在运行
Write-Host "2. Killing any remaining mysqld processes..." -ForegroundColor Cyan
Get-Process mysqld -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 3. 创建 SQL 文件
Write-Host "3. Creating SQL script..." -ForegroundColor Cyan
$sqlContent = "ALTER USER 'root'@'localhost' IDENTIFIED BY '123456'; FLUSH PRIVILEGES;"
Set-Content -Path $InitSqlPath -Value $sqlContent -Encoding Ascii

# 4. 启动 MySQL 并应用密码
Write-Host "4. Starting MySQL with reset script..." -ForegroundColor Cyan

# 关键修改：使用单字符串传递参数，并显式添加引号以处理路径空格
$Arguments = "--defaults-file=`"$IniPath`" --init-file=`"$InitSqlPath`" --console"

Write-Host "   Command: $ExePath $Arguments" -ForegroundColor DarkGray

# 启动进程
$proc = Start-Process -FilePath $ExePath -ArgumentList $Arguments -PassThru -NoNewWindow

Write-Host "   Waiting 15 seconds..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

# 5. 停止进程
Write-Host "5. Stopping temporary MySQL process..." -ForegroundColor Cyan
if (!$proc.HasExited) {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
}
# 双重保险
Get-Process mysqld -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# 6. 清理
Write-Host "6. Cleaning up..." -ForegroundColor Cyan
Remove-Item -Path $InitSqlPath -Force -ErrorAction SilentlyContinue

# 7. 重启服务
Write-Host "7. Restarting service..." -ForegroundColor Cyan
try {
    Start-Service -Name $ServiceName
    Write-Host "SUCCESS! Password reset to: 123456" -ForegroundColor Green
} catch {
    Write-Error "Failed to start service. Please start it manually."
}
