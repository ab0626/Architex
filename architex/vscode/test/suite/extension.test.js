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
Object.defineProperty(exports, "__esModule", { value: true });
const assert = __importStar(require("assert"));
const vscode = __importStar(require("vscode"));
suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');
    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('architex.architex'));
    });
    test('Should activate', async () => {
        const ext = vscode.extensions.getExtension('architex.architex');
        if (ext) {
            await ext.activate();
            assert.ok(ext.isActive);
        }
    });
    test('Should register commands', async () => {
        const commands = await vscode.commands.getCommands();
        const architexCommands = commands.filter(cmd => cmd.startsWith('architex.'));
        assert.ok(architexCommands.length > 0, 'Should register at least one command');
        assert.ok(architexCommands.includes('architex.analyze'), 'Should register analyze command');
        assert.ok(architexCommands.includes('architex.showDashboard'), 'Should register dashboard command');
    });
    test('Should register views', async () => {
        // Test that views are registered (this would require more complex setup)
        assert.ok(true, 'Views registration test placeholder');
    });
});
//# sourceMappingURL=extension.test.js.map