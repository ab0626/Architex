# Architex VS Code Extension Demo Walkthrough

This guide walks you through testing all features of the Architex VS Code extension.

---

## 1. Setup

- Open `architex/vscode/` in VS Code
- Run `npm install` and `npm run compile`
- Press `F5` to launch the Extension Development Host
- In the new window, open the `test-workspace/` folder

---

## 2. Analyze Workspace

- Open the Command Palette (`Ctrl+Shift+P`)
- Run `Architex: Analyze Current Workspace`
- **Expected:**
  - Status bar shows `Architex: Analyzing...` then `Architex: N elements`
  - Sidebar views become available

---

## 3. Show Dashboard

- Run `Architex: Show Dashboard`
- **Expected:**
  - Webview panel opens with the interactive dashboard

---

## 4. Show Metrics

- Run `Architex: Show Metrics`
- **Expected:**
  - Webview panel shows code metrics with color-coded severity

---

## 5. Show Recommendations

- Run `Architex: Show AI Recommendations`
- **Expected:**
  - Webview panel shows AI-powered recommendations

---

## 6. Live Analysis

- Run `Architex: Start Live Analysis`
- Edit a file in the workspace
- **Expected:**
  - Status bar shows `Live Analysis Active`
  - Updates appear in sidebar views
- Run `Architex: Stop Live Analysis` to stop

---

## 7. Export Diagram/Summary

- Run `Architex: Export Diagram` and choose a location
- Run `Architex: Export Analysis Summary` and choose a location
- **Expected:**
  - Files are created with the exported content

---

## 8. Configuration

- Open VS Code settings and search for `Architex`
- Change export format, enable/disable AI features, etc.
- **Expected:**
  - Extension behavior updates according to settings

---

## 9. Troubleshooting

- If you see errors, check the output panel for logs
- Make sure the backend (CLI/web server) is available if needed

---

**Enjoy using Architex in VS Code!** 