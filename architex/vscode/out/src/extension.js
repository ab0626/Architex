"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = exports.ArchitexExtension = void 0;
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
const ws_1 = __importDefault(require("ws"));
class ArchitexExtension {
    constructor(context) {
        this.websocket = null;
        this.architexProcess = null;
        this.currentAnalysis = null;
        this.metrics = [];
        this.recommendations = [];
        this.liveAnalysisActive = false;
        this.context = context;
        this.statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 100);
        this.statusBarItem.command = 'architex.showDashboard';
        this.updateStatusBar('Architex: Ready');
        this.statusBarItem.show();
    }
    activate() {
        this.registerCommands();
        this.registerViews();
        this.setupWebSocket();
        // Auto-analyze if enabled
        const config = vscode.workspace.getConfiguration('architex');
        if (config.get('autoAnalyze') && vscode.workspace.workspaceFolders) {
            this.analyzeWorkspace();
        }
    }
    deactivate() {
        this.cleanup();
    }
    registerCommands() {
        const commands = [
            vscode.commands.registerCommand('architex.analyze', () => this.analyzeWorkspace()),
            vscode.commands.registerCommand('architex.analyzeFile', () => this.analyzeCurrentFile()),
            vscode.commands.registerCommand('architex.showDashboard', () => this.showDashboard()),
            vscode.commands.registerCommand('architex.showMetrics', () => this.showMetrics()),
            vscode.commands.registerCommand('architex.showRecommendations', () => this.showRecommendations()),
            vscode.commands.registerCommand('architex.startLiveAnalysis', () => this.startLiveAnalysis()),
            vscode.commands.registerCommand('architex.stopLiveAnalysis', () => this.stopLiveAnalysis()),
            vscode.commands.registerCommand('architex.exportDiagram', () => this.exportDiagram()),
            vscode.commands.registerCommand('architex.exportSummary', () => this.exportSummary())
        ];
        commands.forEach(cmd => this.context.subscriptions.push(cmd));
    }
    registerViews() {
        // Architecture view provider
        const architectureProvider = new ArchitectureViewProvider(this.context.extensionUri);
        vscode.window.registerWebviewViewProvider('architex.architectureView', architectureProvider);
        // Metrics view provider
        const metricsProvider = new MetricsViewProvider(this.context.extensionUri);
        vscode.window.registerWebviewViewProvider('architex.metricsView', metricsProvider);
        // Recommendations view provider
        const recommendationsProvider = new RecommendationsViewProvider(this.context.extensionUri);
        vscode.window.registerWebviewViewProvider('architex.recommendationsView', recommendationsProvider);
        // Live analysis view provider
        const liveAnalysisProvider = new LiveAnalysisViewProvider(this.context.extensionUri);
        vscode.window.registerWebviewViewProvider('architex.liveAnalysisView', liveAnalysisProvider);
    }
    async analyzeWorkspace() {
        if (!vscode.workspace.workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }
        const workspacePath = vscode.workspace.workspaceFolders[0].uri.fsPath;
        await this.runAnalysis(workspacePath);
    }
    async analyzeCurrentFile() {
        const activeEditor = vscode.window.activeTextEditor;
        if (!activeEditor) {
            vscode.window.showErrorMessage('No active file');
            return;
        }
        const filePath = activeEditor.document.uri.fsPath;
        const workspacePath = vscode.workspace.getWorkspaceFolder(activeEditor.document.uri)?.uri.fsPath;
        if (!workspacePath) {
            vscode.window.showErrorMessage('File not in workspace');
            return;
        }
        await this.runAnalysis(workspacePath, filePath);
    }
    async runAnalysis(workspacePath, filePath) {
        this.updateStatusBar('Architex: Analyzing...');
        try {
            const config = vscode.workspace.getConfiguration('architex');
            const aiFeatures = config.get('aiFeatures', true);
            const args = ['analyze', workspacePath];
            if (aiFeatures) {
                args.push('--ai-labels', '--ai-summaries');
            }
            if (filePath) {
                args.push('--file', filePath);
            }
            const result = await this.runArchitexCommand(args);
            if (result.success) {
                this.currentAnalysis = this.parseAnalysisResult(result.output);
                this.updateStatusBar(`Architex: ${this.currentAnalysis.elements_count} elements`);
                vscode.window.showInformationMessage(`Analysis complete: ${this.currentAnalysis.elements_count} elements found`);
                // Update context for view visibility
                vscode.commands.executeCommand('setContext', 'architex.hasAnalysis', true);
            }
            else {
                vscode.window.showErrorMessage(`Analysis failed: ${result.error}`);
                this.updateStatusBar('Architex: Analysis failed');
            }
        }
        catch (error) {
            vscode.window.showErrorMessage(`Analysis error: ${error}`);
            this.updateStatusBar('Architex: Error');
        }
    }
    async runArchitexCommand(args) {
        return new Promise((resolve) => {
            const architexPath = this.getArchitexPath();
            const process = (0, child_process_1.spawn)(architexPath, args, { cwd: vscode.workspace.workspaceFolders?.[0].uri.fsPath });
            let output = '';
            let error = '';
            process.stdout.on('data', (data) => {
                output += data.toString();
            });
            process.stderr.on('data', (data) => {
                error += data.toString();
            });
            process.on('close', (code) => {
                resolve({
                    success: code === 0,
                    output,
                    error
                });
            });
        });
    }
    getArchitexPath() {
        const config = vscode.workspace.getConfiguration('architex');
        const customPath = config.get('architexPath');
        if (typeof customPath === 'string' && customPath.length > 0) {
            return customPath;
        }
        return 'python';
    }
    parseAnalysisResult(output) {
        // Parse the CLI output to extract analysis results
        // This is a simplified parser - in practice, you'd want more robust parsing
        const lines = output.split('\n');
        const result = {
            elements_count: 0,
            relationships_count: 0,
            metrics_count: 0,
            recommendations_count: 0,
            labels_count: 0,
            summaries_count: 0
        };
        for (const line of lines) {
            if (line.includes('Code Elements:')) {
                result.elements_count = parseInt(line.split(':')[1].trim()) || 0;
            }
            else if (line.includes('Relationships:')) {
                result.relationships_count = parseInt(line.split(':')[1].trim()) || 0;
            }
            else if (line.includes('AI Labels:')) {
                result.labels_count = parseInt(line.split(':')[1].trim()) || 0;
            }
            else if (line.includes('AI Summaries:')) {
                result.summaries_count = parseInt(line.split(':')[1].trim()) || 0;
            }
        }
        return result;
    }
    async showDashboard() {
        const panel = vscode.window.createWebviewPanel('architexDashboard', 'Architex Dashboard', vscode.ViewColumn.One, {
            enableScripts: true,
            retainContextWhenHidden: true
        });
        const config = vscode.workspace.getConfiguration('architex');
        const dashboardPort = config.get('dashboardPort', 8000);
        panel.webview.html = this.getDashboardHtml(dashboardPort);
    }
    getDashboardHtml(port) {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Architex Dashboard</title>
          <style>
            body { margin: 0; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
            iframe { width: 100%; height: calc(100vh - 40px); border: none; }
          </style>
        </head>
        <body>
          <iframe src="http://localhost:${port}" title="Architex Dashboard"></iframe>
        </body>
      </html>
    `;
    }
    async showMetrics() {
        if (!this.currentAnalysis) {
            vscode.window.showInformationMessage('No analysis available. Run analysis first.');
            return;
        }
        const panel = vscode.window.createWebviewPanel('architexMetrics', 'Architex Metrics', vscode.ViewColumn.One, { enableScripts: true });
        panel.webview.html = this.getMetricsHtml();
    }
    getMetricsHtml() {
        const metricsHtml = this.metrics.map(metric => `
      <div class="metric ${metric.severity}">
        <h3>${metric.name}</h3>
        <p>${metric.value} ${metric.unit}</p>
        <span class="severity">${metric.severity}</span>
      </div>
    `).join('');
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Architex Metrics</title>
          <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; }
            .metric { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .metric.info { border-left: 4px solid #10b981; }
            .metric.warning { border-left: 4px solid #f59e0b; }
            .metric.error { border-left: 4px solid #ef4444; }
            .metric.critical { border-left: 4px solid #dc2626; }
            .severity { font-size: 12px; padding: 2px 8px; border-radius: 3px; color: white; }
            .severity.info { background: #10b981; }
            .severity.warning { background: #f59e0b; }
            .severity.error { background: #ef4444; }
            .severity.critical { background: #dc2626; }
          </style>
        </head>
        <body>
          <h1>Architex Metrics</h1>
          ${metricsHtml}
        </body>
      </html>
    `;
    }
    async showRecommendations() {
        if (!this.currentAnalysis) {
            vscode.window.showInformationMessage('No analysis available. Run analysis first.');
            return;
        }
        const panel = vscode.window.createWebviewPanel('architexRecommendations', 'Architex AI Recommendations', vscode.ViewColumn.One, { enableScripts: true });
        panel.webview.html = this.getRecommendationsHtml();
    }
    getRecommendationsHtml() {
        const recommendationsHtml = this.recommendations.map(rec => `
      <div class="recommendation ${rec.priority}">
        <h3>${rec.title}</h3>
        <p>${rec.description}</p>
        <div class="meta">
          <span class="priority">${rec.priority}</span>
          <span class="impact">${rec.impact}</span>
          <span class="confidence">${Math.round(rec.confidence * 100)}% confidence</span>
        </div>
      </div>
    `).join('');
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Architex AI Recommendations</title>
          <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; }
            .recommendation { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .recommendation.critical { border-left: 4px solid #dc2626; background: #fef2f2; }
            .recommendation.high { border-left: 4px solid #ef4444; background: #fef2f2; }
            .recommendation.medium { border-left: 4px solid #f59e0b; background: #fffbeb; }
            .recommendation.low { border-left: 4px solid #10b981; background: #f0fdf4; }
            .meta { margin-top: 10px; }
            .meta span { margin-right: 15px; font-size: 12px; padding: 2px 8px; border-radius: 3px; }
            .priority { background: #3b82f6; color: white; }
            .impact { background: #6b7280; color: white; }
            .confidence { background: #10b981; color: white; }
          </style>
        </head>
        <body>
          <h1>AI-Powered Recommendations</h1>
          ${recommendationsHtml}
        </body>
      </html>
    `;
    }
    async startLiveAnalysis() {
        if (!vscode.workspace.workspaceFolders) {
            vscode.window.showErrorMessage('No workspace folder found');
            return;
        }
        const workspacePath = vscode.workspace.workspaceFolders[0].uri.fsPath;
        const config = vscode.workspace.getConfiguration('architex');
        const websocketPort = config.get('websocketPort', 8765);
        try {
            this.architexProcess = (0, child_process_1.spawn)(this.getArchitexPath(), ['watch', workspacePath, '--port', websocketPort.toString()], {
                cwd: workspacePath
            });
            this.liveAnalysisActive = true;
            vscode.commands.executeCommand('setContext', 'architex.liveAnalysisActive', true);
            this.updateStatusBar('Architex: Live Analysis Active');
            vscode.window.showInformationMessage('Live analysis started');
            this.architexProcess.on('close', () => {
                this.liveAnalysisActive = false;
                vscode.commands.executeCommand('setContext', 'architex.liveAnalysisActive', false);
                this.updateStatusBar('Architex: Ready');
            });
        }
        catch (error) {
            vscode.window.showErrorMessage(`Failed to start live analysis: ${error}`);
        }
    }
    async stopLiveAnalysis() {
        if (this.architexProcess) {
            this.architexProcess.kill();
            this.architexProcess = null;
        }
        this.liveAnalysisActive = false;
        vscode.commands.executeCommand('setContext', 'architex.liveAnalysisActive', false);
        this.updateStatusBar('Architex: Ready');
        vscode.window.showInformationMessage('Live analysis stopped');
    }
    async exportDiagram() {
        if (!this.currentAnalysis) {
            vscode.window.showInformationMessage('No analysis available. Run analysis first.');
            return;
        }
        const config = vscode.workspace.getConfiguration('architex');
        const format = config.get('exportFormat', 'mermaid');
        const uri = await vscode.window.showSaveDialog({
            filters: {
                'Diagram Files': format === 'mermaid' ? ['md'] : format === 'plantuml' ? ['puml'] : ['dot']
            }
        });
        if (uri) {
            try {
                const workspacePath = vscode.workspace.workspaceFolders[0].uri.fsPath;
                const result = await this.runArchitexCommand(['analyze', workspacePath, '--format', format, '--output', uri.fsPath]);
                if (result.success) {
                    vscode.window.showInformationMessage(`Diagram exported to ${uri.fsPath}`);
                }
                else {
                    vscode.window.showErrorMessage(`Export failed: ${result.error}`);
                }
            }
            catch (error) {
                vscode.window.showErrorMessage(`Export error: ${error}`);
            }
        }
    }
    async exportSummary() {
        if (!this.currentAnalysis) {
            vscode.window.showInformationMessage('No analysis available. Run analysis first.');
            return;
        }
        const config = vscode.workspace.getConfiguration('architex');
        const format = config.get('summaryFormat', 'markdown');
        const uri = await vscode.window.showSaveDialog({
            filters: {
                'Summary Files': format === 'markdown' ? ['md'] : ['json']
            }
        });
        if (uri) {
            try {
                const workspacePath = vscode.workspace.workspaceFolders[0].uri.fsPath;
                const result = await this.runArchitexCommand(['analyze', workspacePath, '--export-summary', format, '--output', uri.fsPath]);
                if (result.success) {
                    vscode.window.showInformationMessage(`Summary exported to ${uri.fsPath}`);
                }
                else {
                    vscode.window.showErrorMessage(`Export failed: ${result.error}`);
                }
            }
            catch (error) {
                vscode.window.showErrorMessage(`Export error: ${error}`);
            }
        }
    }
    setupWebSocket() {
        const config = vscode.workspace.getConfiguration('architex');
        const websocketPort = config.get('websocketPort', 8765);
        this.websocket = new ws_1.default(`ws://localhost:${websocketPort}`);
        this.websocket.on('open', () => {
            console.log('WebSocket connected');
        });
        this.websocket.on('message', (data) => {
            try {
                const message = JSON.parse(data.toString());
                this.handleWebSocketMessage(message);
            }
            catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        });
        this.websocket.on('error', (error) => {
            console.error('WebSocket error:', error);
        });
        this.websocket.on('close', () => {
            console.log('WebSocket disconnected');
        });
    }
    handleWebSocketMessage(message) {
        switch (message.type) {
            case 'analysis_update':
                this.currentAnalysis = message.data;
                if (this.currentAnalysis && typeof this.currentAnalysis.elements_count === 'number') {
                    this.updateStatusBar(`Architex: ${this.currentAnalysis.elements_count} elements`);
                }
                else {
                    this.updateStatusBar('Architex: Analysis complete');
                }
                break;
            case 'metrics_update':
                this.metrics = message.data.metrics;
                break;
            case 'recommendations_update':
                this.recommendations = message.data.recommendations;
                break;
        }
    }
    updateStatusBar(text) {
        this.statusBarItem.text = text;
    }
    cleanup() {
        if (this.websocket) {
            this.websocket.close();
        }
        if (this.architexProcess) {
            this.architexProcess.kill();
        }
        this.statusBarItem.dispose();
    }
    dispose() {
        this.statusBarItem.dispose();
        if (this.architexProcess) {
            this.architexProcess.kill();
        }
        if (this.websocket) {
            this.websocket.close();
        }
    }
}
exports.ArchitexExtension = ArchitexExtension;
// View Providers
class ArchitectureViewProvider {
    constructor(_extensionUri) {
        this._extensionUri = _extensionUri;
    }
    resolveWebviewView(webviewView, context, _token) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);
    }
    getHtmlForWebview(webview) {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Architecture View</title>
        </head>
        <body>
          <h2>🏗️ Architecture Overview</h2>
          <p>View your system architecture here.</p>
          <button onclick="showArchitecture()">Show Architecture</button>
        </body>
      </html>
    `;
    }
}
class MetricsViewProvider {
    constructor(_extensionUri) {
        this._extensionUri = _extensionUri;
    }
    resolveWebviewView(webviewView, context, _token) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);
    }
    getHtmlForWebview(webview) {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Metrics View</title>
        </head>
        <body>
          <h2>📊 Code Metrics</h2>
          <p>View code quality metrics here.</p>
          <button onclick="showMetrics()">Show Metrics</button>
        </body>
      </html>
    `;
    }
}
class RecommendationsViewProvider {
    constructor(_extensionUri) {
        this._extensionUri = _extensionUri;
    }
    resolveWebviewView(webviewView, context, _token) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);
    }
    getHtmlForWebview(webview) {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Recommendations View</title>
        </head>
        <body>
          <h2>🎯 AI Recommendations</h2>
          <p>View AI-powered recommendations here.</p>
          <button onclick="showRecommendations()">Show Recommendations</button>
        </body>
      </html>
    `;
    }
}
class LiveAnalysisViewProvider {
    constructor(_extensionUri) {
        this._extensionUri = _extensionUri;
    }
    resolveWebviewView(webviewView, context, _token) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);
    }
    getHtmlForWebview(webview) {
        return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Live Analysis View</title>
        </head>
        <body>
          <h2>🔄 Live Analysis</h2>
          <p>Monitor live analysis updates here.</p>
          <button onclick="startLiveAnalysis()">Start Live Analysis</button>
        </body>
      </html>
    `;
    }
}
function activate(context) {
    const extension = new ArchitexExtension(context);
    extension.activate();
    context.subscriptions.push(extension);
}
exports.activate = activate;
function deactivate() {
    // Cleanup is handled by the extension class
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map