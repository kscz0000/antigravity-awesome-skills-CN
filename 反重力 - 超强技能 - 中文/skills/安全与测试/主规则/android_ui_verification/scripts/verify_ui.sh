#!/bin/bash

# Android UI 验证技能辅助脚本
# 用法: ./verify_ui.sh [截图名称]

ARTIFACTS_DIR="./artifacts"
SCREENSHOT_NAME="${1:-latest_screen}"

echo "🚀 启动 UI 验证..."

# 1. 创建 artifacts 目录（如不存在）
mkdir -p "$ARTIFACTS_DIR"

# 2. 获取分辨率
echo "📏 校准显示屏..."
adb shell wm size

# 3. 导出 UI XML
echo "📋 导出 UI 层级结构..."
adb shell uiautomator dump /sdcard/view.xml
adb pull /sdcard/view.xml "$ARTIFACTS_DIR/view.xml"

# 4. 捕获截图
echo "📸 捕获截图: $SCREENSHOT_NAME.png"
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png "$ARTIFACTS_DIR/$SCREENSHOT_NAME.png"

# 5. 获取最近的 JS 日志
echo "📜 获取最近的 JS 日志..."
adb logcat -d | grep "ReactNativeJS" | tail -n 20 > "$ARTIFACTS_DIR/js_logs.txt"

echo "✅ 完成。产物已保存至 $ARTIFACTS_DIR"
