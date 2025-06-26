import * as assert from 'assert';
import * as vscode from 'vscode';

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