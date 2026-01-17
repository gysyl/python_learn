# 从 npm 迁移到 pnpm 系统性指南

本指南详细说明了将项目从 npm 迁移到 pnpm 的标准流程，适用于 Windows、WSL 和 Linux 环境。

## 1. 环境准备阶段

- 在每个操作系统环境（Windows原生、WSL子系统、Linux虚拟机）中全局安装 pnpm：
  ```bash
  npm install -g pnpm
  ```
- 确保所有环境的 pnpm 版本一致（建议使用最新稳定版）。

## 2. 项目迁移步骤（对每个项目单独执行）

1.  **清理旧依赖**：
    删除现有 `node_modules` 目录和 `package-lock.json` 文件。
    ```bash
    rm -rf node_modules package-lock.json
    # Windows CMD: rmdir /s /q node_modules & del package-lock.json
    ```

2.  **转换锁文件**：
    在项目根目录执行 `import` 命令，自动转换 npm 的依赖结构。
    ```bash
    pnpm import
    ```

3.  **安装依赖**：
    运行安装命令生成新的 `pnpm-lock.yaml` 文件。
    ```bash
    pnpm install
    ```

4.  **修正脚本**：
    检查 `package.json` 中的 npm 特定命令（如 `preinstall`/`postinstall`），修改为 pnpm 兼容的语法（通常 pnpm 会自动处理，但需检查显式调用的 `npm run`）。

## 3. 多环境同步配置

1.  **创建配置文件**：
    在项目根目录创建 `.npmrc` 文件统一配置，以兼容部分依赖结构（提升依赖）：
    ```ini
    shamefully-hoist=true
    ```

2.  **工作区支持**：
    考虑使用 pnpm workspace 功能管理跨项目的公共依赖（如果在 monorepo 中）。

3.  **CI/CD 更新**：
    更新 CI/CD 流程中的包管理器调用命令，将 `npm` 替换为 `pnpm`。

## 4. 验证与测试

- 执行测试确保功能正常：
  ```bash
  pnpm test
  ```
- 检查运行时行为是否与 npm 版本一致。
- 对比磁盘空间占用，确认 `node_modules` 体积显著减少。

## 5. 后续优化

- 将项目中的 `npm` 脚本命令逐步替换为 `pnpm` 原生命令。
- 利用 `pnpm why <package>` 分析依赖关系，优化项目依赖结构。
- 考虑启用 pnpm 的严格模式（如在 `.npmrc` 中设置 `node-linker=isolated`）获得更好的隔离性。

## 注意事项

- 保留各环境的操作系统路径差异（特别是 WSL 和 Linux 的路径处理）。
- 建议使用 pnpm 的 `--store-dir` 参数或在配置中指定统一的虚拟存储位置，以便更好地管理缓存。
