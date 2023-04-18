# Android Screen Capture Tool

這是一個使用 PyQt6 和 adb 工具開發的 Android 螢幕擷取工具。這個工具允許您連接到 Android 設備，擷取螢幕截圖，並在圖形用戶界面中進行裁剪。

## 功能

- 自動檢測連接的 Android 設備
- 擷取 Android 設備的螢幕截圖
- 在應用程序中顯示截圖
- 使用滑鼠選擇裁剪範圍並另存為新文件
- 調整截圖大小以適應用戶界面
- 支持多個 Android 設備

## 安裝

1. 確保您已安裝 Python 3.6 或更高版本。可以在 [Python 官方網站](https://www.python.org/downloads/) 下載。

2. 安裝 PyQt6。在終端中執行以下命令：

 ```bash
 pip install PyQt6
 ```
3. 確保您已安裝 Android Debug Bridge (adb) 工具。可以在 [Android 開發者網站](https://developer.android.com/studio/command-line/adb) 上找到有關如何安裝和使用 adb 的說明。

## 使用

1. 將您的 Android 設備連接到電腦。

2. 啟動 Android 設備的 USB 偵錯模式。詳細信息可以在 [Android 開發者網站](https://developer.android.com/studio/debug/dev-options) 上找到。

3. 運行螢幕擷取工具。在終端中執行以下命令：

 ```bash
 python main.py
 ```

4. 在應用程序中，按下 "Refresh Devices" 按鈕以顯示連接的 Android 設備。

5. 選擇您要擷取螢幕的設備，然後按下 "Capture Screen" 按鈕。

6. 在顯示的截圖上，使用滑鼠選擇要裁剪的區域。

7. 按下 "Crop Image" 按鈕以裁剪選擇的區域並另存為新文件。

## 許可證

此項目使用 [MIT 許可證](https://opensource.org/licenses/MIT)。

請隨意修改、分發和使用這個螢幕擷取工具。如有任何疑問