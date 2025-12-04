# MySQL Root Password Reset Script V3 (Empty Password Strategy)
# 此脚本尝试将 root 密码清空，以便无密码登录
$ErrorActionPreference = "Stop"

# 配置部分
$ServiceName = "MySQL84"
$ProcessName = "mysqld"
$MysqldPath = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe"
$DefaultsFile = "C:\ProgramData\MySQL\MySQL Server 8.4\my.ini"
$TempSqlFile = "$env:TEMP\reset_root_empty.sql"

# 1. 停止服务
Write-Host "1. Stopping service $ServiceName..." -ForegroundColor Cyan
try {
    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
} catch {
    Write-Host "Service stop failed or service not running. Continuing..." -ForegroundColor Yellow
}

# 2. 确保进程已杀掉
Write-Host "2. Ensuring all mysqld processes are stopped..." -ForegroundColor Cyan
$processes = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
if ($processes) {
    Stop-Process -Name $ProcessName -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# 3. 创建 SQL 脚本 (仅清空密码)
Write-Host "3. Creating SQL script (CLEAR PASSWORD ONLY)..." -ForegroundColor Cyan
$sqlContent = @"
-- 仅清空密码，避开密码策略限制
UPDATE mysql.user SET authentication_string=null WHERE User='root';
FLUSH PRIVILEGES;
"@
Set-Content -Path $TempSqlFile -Value $sqlContent -Encoding Ascii

# 4. 启动 MySQL 并应用重置
Write-Host "4. Starting MySQL with init-file to clear password..." -ForegroundColor Cyan
# 注意：这里需要处理路径中的空格，使用引号包裹
$argList = "--defaults-file=`"$DefaultsFile`" --init-file=`"$TempSqlFile`" --console"
Write-Host "Command: $MysqldPath $argList" -ForegroundColor DarkGray

$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = $MysqldPath
$pinfo.Arguments = $argList
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $true
$pinfo.RedirectStandardOutput = $true
$pinfo.RedirectStandardError = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $pinfo
$process.Start() | Out-Null

Write-Host "Waiting 20 seconds for script to execute..." -ForegroundColor Cyan
Start-Sleep -Seconds 20

# 5. 停止临时进程
Write-Host "5. Stopping temporary MySQL process..." -ForegroundColor Cyan
try {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
} catch {
    # 如果进程已经退出或无法通过ID停止，尝试按名称停止
    Stop-Process -Name $ProcessName -Force -ErrorAction SilentlyContinue
}

# 6. 清理
Write-Host "6. Cleaning up..." -ForegroundColor Cyan
Remove-Item -Path $TempSqlFile -Force -ErrorAction SilentlyContinue

# 7. 重启正常服务
Write-Host "7. Restarting service..." -ForegroundColor Cyan
try {
    Start-Service -Name $ServiceName
    Write-Host "SUCCESS! Password CLEARED." -ForegroundColor Green
    Write-Host "PLEASE TRY LOGGING IN WITHOUT A PASSWORD (JUST PRESS ENTER)." -ForegroundColor Yellow
} catch {
    Write-Host "Failed to start service. Please start it manually: Start-Service $ServiceName" -ForegroundColor Red
}
