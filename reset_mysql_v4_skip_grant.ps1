# MySQL Root Password Reset Script V4 (Skip-Grant-Tables Strategy)
# 此脚本使用 --skip-grant-tables 模式启动 MySQL，这是官方推荐的忘记密码恢复方法。
$ErrorActionPreference = "Stop"

# 配置路径
$ServiceName = "MySQL84"
$MysqldPath = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe"
$MysqlClientPath = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
$DefaultsFile = "C:\ProgramData\MySQL\MySQL Server 8.4\my.ini"

# 1. 停止服务
Write-Host "1. Stopping service $ServiceName..." -ForegroundColor Cyan
try {
    Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue
} catch {
    Write-Host "Service stop failed or service not running. Continuing..." -ForegroundColor Yellow
}

# 2. 确保所有 mysqld 进程已停止
Write-Host "2. Killing any remaining mysqld processes..." -ForegroundColor Cyan
Stop-Process -Name "mysqld" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 3. 在后台启动 mysqld (Skip Grant Tables 模式)
Write-Host "3. Starting mysqld in --skip-grant-tables mode..." -ForegroundColor Cyan
# 使用 Start-Process 启动后台进程
# 添加 --skip-grant-tables 和 --shared-memory (允许Windows本地连接)
$argList = "--defaults-file=`"$DefaultsFile`" --skip-grant-tables --shared-memory"
$pinfo = New-Object System.Diagnostics.ProcessStartInfo
$pinfo.FileName = $MysqldPath
$pinfo.Arguments = $argList
$pinfo.UseShellExecute = $false
$pinfo.CreateNoWindow = $true # 隐藏窗口
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $pinfo
$process.Start() | Out-Null

Write-Host "Waiting 15 seconds for MySQL to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 15

# 4. 执行重置命令 (通过 mysql 客户端)
Write-Host "4. Connecting and resetting password..." -ForegroundColor Cyan
try {
    # 关键步骤：
    # 1. FLUSH PRIVILEGES (加载权限表，否则无法运行 ALTER USER)
    # 2. ALTER USER 重置密码
    # 注意：在 skip-grant-tables 模式下，必须先 FLUSH PRIVILEGES 才能修改密码
    $sqlCmd = "FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED BY '123456'; FLUSH PRIVILEGES;"
    
    # 尝试执行
    $output = & $MysqlClientPath -u root --protocol=memory -e $sqlCmd 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Password reset command executed successfully." -ForegroundColor Green
    } else {
        Write-Host "ERROR: SQL execution failed." -ForegroundColor Red
        Write-Host $output
        
        # 尝试备用方案：先清空再设置
        Write-Host "Retrying with UPDATE strategy..." -ForegroundColor Yellow
        $sqlCmd2 = "FLUSH PRIVILEGES; UPDATE mysql.user SET authentication_string='' WHERE User='root'; FLUSH PRIVILEGES; ALTER USER 'root'@'localhost' IDENTIFIED BY '123456'; FLUSH PRIVILEGES;"
        & $MysqlClientPath -u root --protocol=memory -e $sqlCmd2
    }
} catch {
    Write-Host "Exception during SQL execution: $_" -ForegroundColor Red
}

# 5. 停止临时进程
Write-Host "5. Stopping temporary MySQL process..." -ForegroundColor Cyan
try {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
} catch {
    Stop-Process -Name "mysqld" -Force -ErrorAction SilentlyContinue
}

# 6. 重启服务
Write-Host "6. Restarting normal service..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
try {
    Start-Service -Name $ServiceName
    Write-Host "Service started." -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "DONE! Please try logging in with password: 123456" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
} catch {
    Write-Host "Failed to start service. Please check manually." -ForegroundColor Red
}
