# Publishing Architex to VS Code Marketplace

This guide will walk you through the process of publishing the Architex extension to the VS Code Marketplace.

## Prerequisites

1. **Microsoft Account**: You need a Microsoft account to access the Visual Studio Marketplace
2. **Publisher Account**: Create a publisher account on the Visual Studio Marketplace
3. **Node.js**: Ensure you have Node.js installed (version 14 or higher)
4. **vsce**: Install the Visual Studio Code Extension Manager

## Step 1: Install vsce

```bash
npm install -g @vscode/vsce
```

## Step 2: Create Publisher Account

1. Go to [Visual Studio Marketplace](https://marketplace.visualstudio.com/)
2. Click "Sign in" and use your Microsoft account
3. Click "Publish extensions"
4. Create a new publisher account:
   - Choose a unique publisher name (e.g., "architex-dev" or "adithya-bellamkonda")
   - Add your display name
   - Upload a profile picture (optional)
   - Accept the terms

## Step 3: Update package.json

Update the `publisher` field in `package.json` with your publisher name:

```json
{
  "publisher": "your-publisher-name",
  "name": "architex",
  "displayName": "Architex - AI-Powered Architecture Analysis",
  "description": "Automatically generate system design diagrams and architectural insights from your codebase using AI",
  "version": "1.0.0",
  // ... rest of the configuration
}
```

## Step 4: Create Personal Access Token

1. Go to [Azure DevOps](https://dev.azure.com/)
2. Sign in with your Microsoft account
3. Create a new organization (if you don't have one)
4. Go to User Settings → Personal Access Tokens
5. Create a new token:
   - Name: "VS Code Extension Publishing"
   - Organization: All accessible organizations
   - Expiration: 1 year (or as needed)
   - Scopes: Custom defined → Marketplace (Publish)
6. Copy the token (you'll need it for publishing)

## Step 5: Package the Extension

```bash
# Navigate to the extension directory
cd architex/vscode

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package the extension
vsce package
```

This will create a `.vsix` file that you can use for publishing.

## Step 6: Publish the Extension

### Option A: Using vsce (Recommended)

```bash
# Login with your Personal Access Token
vsce login your-publisher-name

# Publish the extension
vsce publish
```

### Option B: Using the Marketplace Website

1. Go to [Visual Studio Marketplace](https://marketplace.visualstudio.com/)
2. Sign in and go to "Publish extensions"
3. Click "New extension" → "Visual Studio Code"
4. Upload the `.vsix` file
5. Fill in the extension details

## Step 7: Extension Details

When publishing, you'll need to provide:

### Basic Information
- **Extension Name**: Architex
- **Display Name**: Architex - AI-Powered Architecture Analysis
- **Description**: Automatically generate high-level system design diagrams and architectural insights from your codebase using AI
- **Version**: 1.0.0

### Categories
- Other
- Visualization
- AI

### Tags
- architecture
- diagrams
- ai
- system-design
- code-analysis
- visualization
- python
- javascript
- typescript
- java

### Screenshots
Create screenshots showing:
1. Extension sidebar with architecture view
2. Dashboard webview
3. Command palette integration
4. Context menu options

### README
The README.md file will be automatically used as the extension description.

## Step 8: Update and Maintenance

### Updating the Extension

1. Update the version in `package.json`
2. Make your changes
3. Compile and package:
   ```bash
   npm run compile
   vsce package
   ```
4. Publish the update:
   ```bash
   vsce publish
   ```

### Versioning Guidelines

- **Major version** (1.0.0): Breaking changes
- **Minor version** (1.1.0): New features
- **Patch version** (1.0.1): Bug fixes

## Step 9: Post-Publishing

### Marketing
1. Share on social media
2. Post on Reddit (r/vscode, r/programming)
3. Write a blog post
4. Share in relevant Discord/Slack communities

### Support
1. Monitor GitHub issues
2. Respond to user feedback
3. Update documentation
4. Fix bugs promptly

## Troubleshooting

### Common Issues

1. **Publisher Name Already Taken**
   - Try variations like "architex-dev", "architex-tool", etc.

2. **Token Issues**
   - Ensure the token has the correct permissions
   - Check if the token has expired

3. **Package Errors**
   - Verify all dependencies are installed
   - Check TypeScript compilation
   - Ensure icon files exist

4. **Publishing Errors**
   - Check internet connection
   - Verify publisher name matches
   - Ensure version number is unique

### Getting Help

- [VS Code Extension API Documentation](https://code.visualstudio.com/api)
- [Marketplace Publishing Guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [vsce Documentation](https://github.com/microsoft/vscode-vsce)

## Success Metrics

Track these metrics after publishing:
- Downloads per day/week
- User ratings and reviews
- GitHub stars and issues
- Social media mentions

## Next Steps

After successful publishing:
1. Set up GitHub Actions for automated publishing
2. Create a development roadmap
3. Plan feature updates
4. Build a community around the extension

---

**Good luck with publishing Architex! 🚀** 